
# ----------------------------mistal_ai-------------------------------

import threading
from django.conf import settings
from mistralai import Mistral


class SummarizationModel:
    """A class that encapsulates the summarization model for text summarization using mistral_ai API.

    Attributes:
        api_url: The URL for the Mistral AI API.
        headers: The headers required for authorization.
    """
    def __init__(self, model_name, api_key):
        
        self.client=Mistral(api_key=api_key)
        self.model_name = model_name
        


    def summarize(self, text):
        """Generates a summary for the provided text using the Mistral AI API.

        Args:
            text (str): The input text to summarize.

        Returns:
             str: The generated summary.
        """
        
       
         
        prompt = f"""
            Sie sind ein Assistent, der die Aufgabe hat, Besprechungsprotokolle in prägnanten Zusammenfassungen zusammenzufassen. 
            Bitte fassen Sie die folgende Besprechungstranskription aus der Perspektive einer dritten Person zusammen. 
            Beziehen Sie alle besprochenen Kernpunkte mit ein und nennen Sie die in der Transkription des Meetings genannten Personen ordnungsgemäß. 
            und gliedern Sie die Zusammenfassung in klare und zusammenhängende Absätze.
            
            Transcription:
            {text}
            
            Summary:
            """
        
        

        try:
            response = self.client.chat.complete(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
         
     
            return  response.choices[0].message.content.strip()
        except Exception as e:
            print(e)
                

                
    def summarize_chunks(self, text, chunk_size=20000, context_buffer=500):
        """Summarizes the provided text in chunks with overlapping to maintain context.

        Args:
            text (str): The input text to summarize.
            chunk_size (int): The size of each chunk.
            context_buffer (int, optional): The size of the overlapping portion. Defaults to 500.

        Returns:
            str: The concatenated summaries of all chunks.
        """
        
        chunks = []
        for start in range(0, len(text), chunk_size - context_buffer):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)

        summaries = []
        for chunk in chunks:
            summary = self.summarize(chunk)
            summaries.append(summary)
        
        return " ".join(summaries)

class SummarizationModelWrapper:
    """A wrapper class for the SummarizationModel to provide thread-safe summarization.

    Attributes:
        model: An instance of the SummarizationModel.
        lock: A threading lock to ensure thread safety during summarization.
    """
    def __init__(self, model_name,api_key):
        self.model = SummarizationModel(model_name,api_key)
        self.lock = threading.Lock()

    def summarize_on_separate_thread(self, text):
        """Summarizes text on a separate thread to avoid blocking the main thread.

        Args:
            text (str): The input text to summarize.

        Returns:
            str: The generated summary.
        """
        result = []

        def summarize_thread():
            with self.lock:
                summary = self.model.summarize_chunks(text)
                result.append(summary)

        thread = threading.Thread(target=summarize_thread)
        thread.start()
        thread.join()

        if result:
            return result[0]


summarization_model_wrapper = SummarizationModelWrapper(model_name="mistral-large-latest", api_key=settings.MISTRAL_API_KEY)

