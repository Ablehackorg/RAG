from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
import os

class DocumentHandler():
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

    def process_document(self, file_path, filename):
        file_extension = filename.split('.')[-1]
        if file_extension == 'pdf':
            return self.process_pdf(file_path)
        elif file_extension == 'txt':
            return self.process_txt(file_path)
        elif file_extension == 'csv':
            return self.process_csv(file_path)
        else:
            raise ValueError(f"Unsuppoted file format {file_extension}")


    def process_pdf(self, file_path):
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            cleaned_docs = []
            for doc in docs:
                if doc.page_content:
                    cleaned_content = self.clean_pdf_text(doc)
                    doc.page_content = cleaned_content
                    cleaned_docs.append(doc)
            splitted_docs = self.text_splitter.split_documents(cleaned_docs)
            return splitted_docs


        except Exception as e:
            print(f"Error with loading pdf file {e}")
            return []

    def clean_pdf_text(self, text):
        if text:
            text = text.encode(encoding='utf-8', errors='ignore').decode

            return text
        else:
            return ''

    def process_txt(self, file_path):
        try:
            loader = TextLoader(file_path)
            docs = loader.load()
            cleaned_docs = []
            for doc in docs:
                if doc.page_content:
                    cleaned_content = self.clean_pdf_text(doc)
                    doc.page_content = cleaned_content
                    cleaned_docs.append(doc)
            splitted_docs = self.text_splitter.split_documents(docs)
            return splitted_docs

        except Exception as e:
            print(f"Error with loading txt file {e}")
            return []

    def process_csv(self, file_path):
        try:
            loader = CSVLoader(file_path)
            docs = loader.load()
            cleaned_docs = []
            for doc in docs:
                if doc.page_content:
                    cleaned_docs.append(doc)
            splitted_ = self.text_splitter.split_documents(cleaned_docs)
            return splitted_docs


        except Exception as e:
            print(f"Error with loading csv file {e}")
            return []

    def get_file_info(self, file_name):
        try:
            file_size = os.path.getsize(file_name)
            file_name = os.path.basename(file_name)
            file_extension = file_name.split('.')[-1]
            return {
                'file_name': file_name,
                'file_sizez (kb)' : round(file_size * 1024),
                'file_extension' : file_extension
            }

        except Exception as e:
            print(f"Error with loading file info {e}")
            return {}