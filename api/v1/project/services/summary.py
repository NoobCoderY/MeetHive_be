import threading
from django.utils.translation import gettext_lazy as _
from api.v1.project.models import Project, Transcription,Summary
from api.v1.user.constants.choices import AuditLogTaskChoices
from api.v1.user.models.audit_log import AuditLog
from justagile_be.exceptions import BusinessException
from django.db import transaction
from django.conf import settings
from utils import extract_speech_content
import re
from .text_summarizer import summarization_model_wrapper
from django.db.models.functions import Coalesce




class SummaryService:
    
    @staticmethod
    
    def preprocess_text(text):
        """
        Removes non-alphanumeric characters, reduces multiple spaces to one,
        and trims leading/trailing whitespace from the input text.
        Args:
        text (str): The input text to be cleaned.

        Returns:
        str: The cleaned version of the input text.
        """
        cleaned_text = re.sub(r'[@#$%^&*()_+=\[{\]};:\'"<>/\\|`~]', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = cleaned_text.strip()
        return cleaned_text
    
    @staticmethod
    def list_summary(project: Project,search_query=None):
        """
        Service function to list all the summary by project ID

        Attributes:
            - project : (str) - ID of the project
        """

        summary = Summary.objects.list_by_project(project).annotate(
                        updated_or_created=Coalesce('updated_at', 'created_at')
                        ).order_by('-updated_or_created')
        if search_query:
            summary = summary.filter(title__icontains=search_query)
        return summary
    
    @staticmethod
    def generate_and_update_summary(summary, transcription_text):
        """
        Generate summary and update the Summary object.

        Attributes:
            - summary : Summary
                - The Summary object to be updated
            - transcription_text : str
                - The transcription text to summarize
        """
        try:
            cleaned_text = SummaryService.preprocess_text(transcription_text)
            summary_text = summarization_model_wrapper.summarize_on_separate_thread(cleaned_text)
            summary.summary = summary_text
            summary.status = 'completed' 
            summary.save()

        except Exception as e:
            summary.status = 'failed'
            summary.save()
      
    @staticmethod
    def create_summary(data,project, project_user):
        """
        Service function to create new summary

        Attributes:
            - data : (CreateSummarySerializer)
                - Transcription request data
            - project_user : (ProjectUser)
                - Project user object representing the creator
        """
        
        transcription=Transcription.objects.get_by_id(data.get("transcription"))
        if not transcription:
            raise BusinessException(
                "TRANSCRIPTION_NOT_FOUND", _("Transcription does not exist")
            )   
        transcription_text=transcription.text.get('content', [])
        summary_text=extract_speech_content(transcription_text)
        
        data={
            "title":transcription.title,
            "summary":None,
            "transcription":transcription,
            "status":"pending"
        }

        summary = Summary.objects.create_summary(data, project, project_user)
        threading.Thread(target=SummaryService.generate_and_update_summary, args=(summary, summary_text)).start()
        return summary

       
    @staticmethod
    def get_summary_by_id(id: str, project):
        """
        Service function to get transcription by ID

        Attributes:
            - id : (str)
                - Summary ID
            - project : (Project)
                - Project data model 
        """

        summary = Summary.objects.get_by_id(id)
        if not summary:
            raise BusinessException(
                "SUMMARY_NOT_FOUND", _("summary does not exist")
            )

        if summary.project.id != project.id:
            raise BusinessException(
                "ACCESS_DENIED_FOR_SUMMARY",
                _("The summary you are trying to access is not available in the project")
            )

        return summary
       
    def update_summary(id: str, data, project, updated_by):
        """
        Service function to update summary

        Attributes:
            - id : (str)
                - Summary ID
            - data : (UpdateSummarySerializer)
                - The summary data to update
            - project : (Project)
                - Project data model
        """

        with transaction.atomic():
            updated_summary = Summary.objects.get_by_id(id)

            if not  updated_summary:
                raise BusinessException(
                    "SUMMARY_NOT_FOUND",
                    _("Summary does not exist")
                )

            if  updated_summary.project.id != project.id:
                raise BusinessException(
                    "ACCESS_DENIED_FOR_SUMMARY",
                    _("The summary you are trying to update is not available in the project")
                )
            updated_summary.title=data.get('title')
            updated_summary.summary = data.get('summary')
            updated_summary.is_editable=data.get('is_editable')
            updated_summary.updated_by = updated_by
            updated_summary.save()

            AuditLog.objects.add_log(
                user=updated_by.user.user.get_name(),
                company=updated_summary.updated_by.user.company.name,
                project=project.name,
                task=AuditLogTaskChoices.UPDATE_SUMMARY,
                extra_fields={
                    'id': f"{updated_summary.id}",
                    'name': updated_summary.title
                }
            )

            return updated_summary
    
    
    def delete_summary(id:str,project,user):
        
        """
        Service function to delete summary

        Attributes:
            - id : (str)
                - Summary ID
            - project : (Project)
                - Project data model
        """
        
        with transaction.atomic():    
            summary=Summary.objects.get_by_id(id)
            
            if not summary:
                raise BusinessException(
                    "SUMMARY_NOT_FOUND",
                    _("Summary does not exist")
                )
        
            if summary.project.id!=project.id:
                raise BusinessException(
                    "ACCESS_DENIED_FOR_SUMMARY",
                    _("The summary you are trying to delete is not available in the project")
                )
            
            summary.is_deleted=True
            summary.save()
            AuditLog.objects.add_log(
                user=user,
                company=summary.updated_by.user.company.name,
                project=project.name,
                task=AuditLogTaskChoices.DELETE_SUMMARY,
                extra_fields={
                    'id': f"{summary.id}",
                    'name': summary.title
                }
            )

            return True
            