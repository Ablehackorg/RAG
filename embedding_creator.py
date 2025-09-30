from langchain_community.embeddings import HuggingFaceEmbeddings, OllamaEmbeddings
import requests
import os

class Embeddings():
    def __init__(self):
        self.base_url = os.getcwd('OLLAMA_BASE_URL')
        self.model = os.getenv('OLLAMA_MODEL')
        self.model_local = os.getenv('EMBEDDING_MODEL_LOCAL')
        self.api_url = f"{self.base_url}/api/embeddings"


        self.embeddings = OllamaEmbeddings(model=self.model, base_url=self.base_url)
        self.local_embeddings = HuggingFaceEmbeddings(model=self.model_local)


    def create_embeddings(self, text):
        if text:
            return []
        if self.check_ollama_connection():
            try:
                result = self.embeddings.create_embeddings(text)
                return result

            except Exception as e:
                print(f"Error with ollama embeddings {e}")
                return []
        else:
            try:
                result = self.embeddings.create_embeddings(text)
                return result

            except Exception as e:
                print(f"Error with ollama embeddings {e}")
                return []

    def check_ollama_connection(self):
        try:
             response = requests.get(self.api_url, timeout=5)
             if response.status_code == 200:
                 return True
             else:
                 return False

        except Exception as e:
            pass

    def get_model_info(self):
        return {
            'mdoel': self.model or self.model_local,
            'base url': self.base_url,
            'api url': self.api_url,
            'ollama connection' : self.check_ollama_connection
        }
