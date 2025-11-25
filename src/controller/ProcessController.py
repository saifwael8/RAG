from .DataController import DataController
from .ProjectController import ProjectController
from .BaseController import BaseController
from src.schemas import ProcessRequest
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.model import FileExtEnums
import os
from typing import List, Dict, Optional
from langchain.schema import Document



class ProcessController(BaseController):
    def _init__(self):
        super().__init__()

    def get_file_extension(self, file_id: str):
        file_extension = os.path.splitext(file_id)[1]
        return file_extension

    def chunk_file(self, project_id: str, process_request: ProcessRequest):
        file_id = process_request.file_id

        project_path = ProjectController().get_project_dir_path(project_id) 
        file_path = os.path.join(
            project_path,
            file_id
        )

        file_extension = self.get_file_extension(file_id)

        chunks = []
        loader = None

        if file_extension == FileExtEnums.PDF.value:
           loader = PyMuPDFLoader(file_path)
        elif file_extension == FileExtEnums.TXT.value:
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            return None
        

        file = loader.load()

        file_content_texts = [
            rec.page_content
            for rec in file
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file
        ]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=process_request.chunk_size,       # max characters per chunk
            chunk_overlap=process_request.overlap_size,     # overlap between chunks to preserve context
            )

        chunks = text_splitter.split_documents(file)
        chunks_serializable = [
            {"text": doc.page_content, "metadata": doc.metadata} 
            for doc in chunks
        ]
        return chunks_serializable