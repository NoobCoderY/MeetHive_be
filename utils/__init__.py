from rest_framework.response import Response
from django.conf import settings
import jwt
import string
import random
import urllib.parse
from rest_framework.pagination import PageNumberPagination


def get_response(status, data, error_code=None, error=None):
    """
    Returns a Response object containing the data provided

    Attributes:
    - status : (int)
        - Status code of the response
    - data : (JSON)
        - json response data if the API is successful
    - error_code : (str)
        - Code for error message if the API failed
    - error : (str)
        - Error message explaining about the API failure

    Returns: 
    - response : (Response)
        - The response object with the status and data provided
    """
    response = {
        'status': status,
        'data': data,
        'error_code': error_code,
        'error': error
    }

    response = Response(
        response, status=status, headers={'Access-Control-Allow-Origin': '*'}
    )
    return response


def get_jwt_token(payload, expiry):
    """
    Returns JWT string encoded with payload and expiry provided.

    Attributes:
    - payload : (json) 
        - The json data to encode
    - expiry : (datetime) 
        - Expiry date time for the token

    Returns:
    - token : (str)
        - The encoded JWT string
    """
    return jwt.encode({'data': payload, 'exp': expiry},
                      settings.SECRET_KEY, settings.JWT_ALGORITHM)


def generate_token(length: int = 30):
    """
    Returns a random generated token string with given length

    Attributes:
    - length : (int)
        - Length of the string to generate

    Returns:
    - token : (str)
        - Random string with given length
    """

    return ''.join(random.choices(string.ascii_uppercase +
                                  string.ascii_lowercase + string.digits, k=length))


def extract_speech_content(content):
    """
    Extracts and combines non-empty 'speech' fields from a list of transcription segments,
    adding a period only at the end of the combined speech.

    Args:
        content (list): List of dictionaries, each containing a 'speech' field.

    Returns:
        str: Combined speech segments as a single sentence ending with a period.
    """

    sentences = []

    
    for entry in content:
        speech = entry.get("speech", "").strip()
        if speech:
            speech = speech[0].upper() + speech[1:] if len(speech) > 1 else speech.upper()
            
            if not speech.endswith(('.', '!', '?', ',')):
                speech += "."

            sentences.append(speech)
    
    return " ".join(sentences)



def extract_s3_info(public_url):
    """
    Extracts the S3 file key, file type, and S3 URI from a public S3 URL.

    Args:
        public_url (str): The public S3 URL.

    Returns:
        dict: A dictionary containing the file key, file type.
    """

    parsed_url = urllib.parse.urlparse(public_url)

    bucket_name = parsed_url.netloc.split('.')[0]  
    file_key = parsed_url.path.lstrip('/')  


    file_type = file_key.split('.')[-1] if '.' in file_key else None  


    return {
        'file_key': file_key,
        'file_type': file_type,
    }

def format_time(seconds):
    """
    Convert time in seconds to a human-readable format like '1h Xm YY.00s'.

    Args:
        - seconds: (float or int) Time in seconds.

    Returns:
        - str: Time formatted as 'Xh Ym ZZ.00s'
    """

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60
    
    remaining_seconds = seconds % 60
    
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {remaining_seconds:.2f}s"
    elif minutes > 0:
        return f"{int(minutes)}m {remaining_seconds:.2f}s"
    else:
        return f"{remaining_seconds:.2f}s"



def refactor_transcription_data(transcription_items):
    """
    Refactor the transcription data into the desired format.

    Attributes:
        - transcription_items: (list) List of transcription data from AWS Transcribe.
        
    Returns:
        - dict: Refactored transcription data.
    """
    last_speaker = None
    last_entry = None
    content = []

    for item in transcription_items:
     
        speaker_number = item["speaker_label"].split("_")[1]  
        speaker_name = f"Speaker {speaker_number}"  
        start_time_rounded = round(float(item['start_time']))
        formatted_time = format_time(start_time_rounded)
       
        if last_speaker == speaker_name:

            last_entry["speech"] += " " + item["transcript"]
        else:
            speech_entry = {
                "speech": item["transcript"],
                "speaker": speaker_name,
                "startTime": formatted_time
            }
            content.append(speech_entry)

            last_entry = speech_entry
            last_speaker = speaker_name

    return {"content": content}




class GenericPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10

