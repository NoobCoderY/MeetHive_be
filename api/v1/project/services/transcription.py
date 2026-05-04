import json
import threading
import time
import uuid
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from api.v1.project.models import Project, Transcription
from justagile_be.exceptions import BusinessException
from api.v1.user.models import AuditLog
from api.v1.user.constants import AuditLogTaskChoices
import boto3
from botocore.config import Config
from django.conf import settings
from utils import extract_s3_info,refactor_transcription_data
import requests
from django.db.models.functions import Coalesce


my_config = Config(
    region_name = settings.AWS_S3_REGION,
    signature_version = 's3v4'  
)




class TranscriptionService:
    @staticmethod
    def list_transcriptions(project: Project,search_query=None,date_from=None):
        """
        Service function to list all the transcriptions by project ID

        Attributes:
            - project_id : (str) - ID of the project
            - page : (int) - Page number for pagination
            - page_size : (int) - Number of items per page
        """        
        transcriptions=Transcription.objects.filter(project=project).annotate(
                        updated_or_created=Coalesce('updated_at', 'created_at')
                        ).order_by('-updated_or_created')
        
        if date_from:
            
            transcriptions = transcriptions.filter(created_at__gte=date_from)
            
        if search_query:
            transcriptions = transcriptions.filter(title__icontains=search_query)
            return transcriptions
        
        return transcriptions
        

    @staticmethod
    def create_transcription(data, audio, project, project_user):
        """
        Service function to create new transcription

        Attributes:
            - data : (CreateTranscriptionSerializer)
                - Transcription request data
            - project_user : (ProjectUser)
                - Project user object representing the creator
        """

        with transaction.atomic():
            transcription = Transcription.objects.create_transcription(
                data, project, project_user, audio
            )

            return transcription

    @staticmethod
    def get_transcription_by_id(id: str, project):
        """
        Service function to get transcription by ID

        Attributes:
            - id : (str)
                - Transcription ID
            - project : (Project)
                - Project data model 
        """

        transcription = Transcription.objects.get_by_id(id)
        if not transcription:
            raise BusinessException(
                "TRANSCRIPTION_NOT_FOUND", _("Transcription does not exist")
            )

        if transcription.project.id != project.id:
            raise BusinessException(
                "ACCESS_DENIED_FOR_TRANSCRIPTION",
                _("The Transcription you are trying to access is not available in the project")
            )

        return transcription

    def update_transcription(id: str, data, project, updated_by):
        """
        Service function to update transcription

        Attributes:
            - id : (str)
                - Transcription ID
            - data : (UpdateTranscriptionSerializer)
                - The transcription data to update
            - project : (Project)
                - Project data model
        """

        with transaction.atomic():
            transcription = Transcription.objects.get_by_id(id)

            if not transcription:
                raise BusinessException(
                    "TRANSCRIPTION_NOT_FOUND",
                    _("Transcription does not exist")
                )

            if transcription.project.id != project.id:
                raise BusinessException(
                    "ACCESS_DENIED_FOR_TRANSCRIPTION",
                    _("The Transcription you are trying to update is not available in the project")
                )

            transcription.title = data.get('title')
            transcription.description = data.get('description')
            transcription.text = data.get('text')
            transcription.updated_by = updated_by
            transcription.save()

            AuditLog.objects.add_log(
                user=updated_by.user.user.get_name(),
                company=transcription.updated_by.user.company.name,
                project=project.name,
                task=AuditLogTaskChoices.UPDATE_TRANSCRIPTION,
                extra_fields={
                    'id': f"{transcription.id}",
                    'name': transcription.title
                }
            )

            return transcription

    @staticmethod
    def delete_transcription(id: str, project, user=''):
        
        """
        Service function to delete transcription

        Attributes:
            - id : (str)
                - Transcription ID
            - project : (Project)
                - Project data model
        """
        with transaction.atomic():
            transcription = Transcription.objects.get_by_id(id)

            if not transcription:
                raise BusinessException(
                    "TRANSCRIPTION_NOT_FOUND",
                    _("Transcription does not exist")
                )

            if transcription.project.id != project.id:
                raise BusinessException(
                    "ACCESS_DENIED_FOR_TRANSCRIPTION",
                    _("The Transcription you are trying to deleted is not available in the project")
                )
            # TODO: Doing soft delete here.  But need to handle this in base model
            transcription.is_deleted = True
            transcription.save()

            AuditLog.objects.add_log(
                user=user,
                company=transcription.updated_by.user.company.name,
                project=project.name,
                task=AuditLogTaskChoices.DELETE_TRANSCRIPTION,
                extra_fields={
                    'id': f"{transcription.id}",
                    'name': transcription.title
                }
            )

            return True

    @staticmethod
    def generate_signed_url(user_id,file_name, file_type):
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,config=my_config)
        unique_id = str(uuid.uuid4())
        # file_key = f"{user_id}/{file_name.replace(' ', '_')}_{unique_id}.{file_type.split('/')[-1]}" 
        file_key = f"{user_id}/{unique_id}-{file_name}"
        try:
            signed_url = s3_client.generate_presigned_url('put_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_key,"ContentType": file_type},
                ExpiresIn=3600) 
            return signed_url
        except Exception as e:
            raise BusinessException(
                "SIGNED_URL_GENERATION_FAILED",
                _("Failed to generate signed URL")
            )
    
    @staticmethod
    def run_aws_transcribe(transcription, audio_url):
        """
        Function to run AWS Transcribe in a separate thread
        and update transcription status upon completion.
        """

      
        transcribe_client = boto3.client(
            'transcribe',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION
        )

        job_name = f"transcription_job_{transcription.id}_{int(time.time())}"
        s3_info = extract_s3_info(audio_url)
        file_type=s3_info.get('file_type')
        file_key=s3_info.get('file_key')
        job_uri=f'https://s3-{settings.AWS_S3_REGION}.amazonaws.com/{settings.AWS_STORAGE_BUCKET_NAME}/{file_key}'
        try:
          
            response = transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat=file_type,  
                LanguageCode='en-US', 
                Settings={
                    'ShowSpeakerLabels': True,
                    'MaxSpeakerLabels': 10 
                }
            )         
            while True:
                status = transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(15)  

            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
              
                transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                transcript_response = requests.get(transcript_url)
                transcript_json = transcript_response.json()
                audio_segments = transcript_json['results']['audio_segments']
                refactor_transcription=refactor_transcription_data(audio_segments)
                
                TranscriptionService.complete_transcription(
                    transcription, refactor_transcription
                )

        except Exception as e:
            transcription.status = 'failed'
            transcription.save()

    @staticmethod
    def complete_transcription(transcription, text):
        """
        Function to mark transcription as completed and update the status and text.
        """
        with transaction.atomic():
            transcription.text = text
            transcription.status = 'completed'
            transcription.save()
            

        
    @staticmethod
    def create_upload_recording_transcription(data, audio, project, project_user):
        """
        Service function to create new upload recordiing transcription

        Attributes:
            - data : (CreateUploadRecordingTranscriptionSerializer)
                - Transcription request data
            - project_user : (ProjectUser)
                - Project user object representing the creator
        """
        
      
        with transaction.atomic():
            # here provide the value of audio and also implement when we get that audio user gets transcription along with that audio
            transcription = Transcription.objects.create_transcription(
                data, project, project_user, audio, status='pending'
            )
            # Start AWS Transcribe process in a separate thread
            thread = threading.Thread(
                target=TranscriptionService.run_aws_transcribe,
                args=(transcription, data.get('audio_url'),)
            )
            thread.start()

            return transcription