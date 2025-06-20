import json
import uuid
from hashlib import md5
from pathlib import Path
from typing import List, Optional, Generator, Tuple, Dict
from hashlib import md5
from dataclasses import dataclass

from agno.document.base import Document
from agno.document.document_v2 import DocumentV2
from agno.document.document_store import DocumentStore
from agno.utils.log import log_debug, log_error, log_info


@dataclass
class LocalDocumentStore(DocumentStore):
    """
    Simple local filesystem implementation of DocumentStore.
    Documents are stored as JSON files in the specified directory.
    """
    
    storage_path: str = None

    def __post_init__(self):
        """Initialize storage path after dataclass initialization."""
        if self.storage_path is None:
            raise ValueError("storage_path is required")
        
        self._storage_path = Path(self.storage_path)
        self._storage_path.mkdir(parents=True, exist_ok=True)

    def _get_document_file_path(self, document_id: str) -> Path:
        """Get the file path for a document by ID."""
        return self._storage_path / f"{document_id}.json"

    def _generate_document_hash(self, document: Document) -> str:
        """Generate a hash of the document content to be used as the document ID."""
        cleaned_content = document.content.replace("\x00", "\ufffd")
        content_hash = md5(cleaned_content.encode()).hexdigest()
        return content_hash

    def add_document(self, document: DocumentV2) -> str:
        """Add a document to the store. Returns the document ID."""

        print(f"Adding document: {document}")
        # document.id = f"{document.name}.{document.extension}"
        # if document.id is None:
        #     document.id = self._generate_document_hash(document)
        
        # # Check if document already exists
      
        # file_path = self._get_document_file_path(document.id)
        # if file_path.exists():
        #     log_debug(f"Document already exists: {document.id}")
        #     return document.id
        # # Convert document to dict and save as JSON
        # document_dict = document.to_dict()
        # document_dict["id"] = document.id  # Ensure ID is included
        
        # with open(file_path, 'w', encoding='utf-8') as f:
        #     json.dump(document_dict, f, indent=2, ensure_ascii=False)
        
        # return document.id
        return "123456"

    def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID. Returns True if successful."""
        file_path = self._get_document_file_path(document_id)

        if file_path.exists():
            try:
                file_path.unlink()
                return True
            except OSError:
                return False
        return False

    def delete_all_documents(self) -> bool:
        """Delete all documents from the store. Returns True if successful."""
        try:
            for file_path in self._storage_path.glob("*.json"):
                file_path.unlink()
            return True
        except OSError:
            return False

    def get_all_documents(self) -> Generator[Tuple[bytes, Dict], None, None]:
        """Get all documents from the store."""
        for file_path in self._storage_path.glob("**/*"):
            if file_path.is_file() and file_path.suffix == '.pdf':
                pdf_bytes = file_path.read_bytes()
                metadata = {
                    "name": file_path.name,
                    "file_path": str(file_path),
                    "file_type": file_path.suffix,
                    "source": self.name,
                }
                yield pdf_bytes, metadata

    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        """Get a document by its ID."""
        file_path = self._get_document_file_path(document_id)

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                document_dict = json.load(f)
                return Document.from_dict(document_dict)
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    def get_document_by_name(self, name: str) -> Optional[Document]:
        """Get a document by its name."""
        for document in self.get_all_documents():
            if document.name == name:
                return document
        return None

    def enhance_document(self, document_id: str, **kwargs) -> bool:
        pass