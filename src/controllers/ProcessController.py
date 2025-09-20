from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain.document_loaders import PyMuPDFLoader ,TextLoader
from models import ProcessingEnum
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import os
from langchain.schema import Document
from fastapi import HTTPException




class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id) 

    def get_file_extension(self, filename: str) -> str:
        return filename.split('.')[-1].lower()
    

    # def get_file_loader(self, file_id: str):
    #     file_ext = self.get_file_extension(file_id)

    #     if file_ext == ProcessingEnum.PDF.value:
    #         return PyMuPDFLoader(os.path.join(self.project_path, file_id))

    #     elif file_ext == ProcessingEnum.TXT.value:
    #         return TextLoader(os.path.join(self.project_path, file_id), encoding='utf8')
        
    #     return None
    def get_file_loader(self, file_id: str):
        file_path = os.path.join(self.project_path, file_id)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None
            
        file_ext = self.get_file_extension(file_id)

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding='utf8')
        
        print(f"Error: Unsupported file extension: {file_ext}")
        return None
    
    def get_file_content (self,file_id: str):
        loader = self.get_file_loader(file_id)
        return loader.load() if loader else None

    def process_file_content(self, file_content: list, file_id: str, chunk_size=100, chunk_overlap=20):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

        file_content_texts =[rec.page_content for rec in file_content]
        file_content_metadatas =[rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadatas
        )
        return chunks
    


