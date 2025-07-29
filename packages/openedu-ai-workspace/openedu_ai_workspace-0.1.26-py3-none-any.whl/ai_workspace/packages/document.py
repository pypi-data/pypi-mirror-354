from ai_workspace.schemas import DocumentSchema
from ai_workspace.database import MongoDB
from ai_workspace.packages.shared import IDGenerator
from .base import BaseDocument
from typing import ClassVar
from ai_workspace.exceptions import handle_exceptions


class Document(BaseDocument):
    mongodb: MongoDB
    id_generator: ClassVar[IDGenerator] = IDGenerator()
    document_collection: str = "documents"

    @property
    def collection(self):
        """Get the collection client for the document collection."""
        return self.mongodb.get_db().get_collection(self.document_collection)

    @handle_exceptions
    def upload_document(self, document_data: DocumentSchema):
        """Upload a document to the database.
        Args:
            document_data (DocumentSchema): The document data to upload.

        Returns:
            str: The ID of the uploaded document.
        """
        document_data.document_id = (
            str(next(self.id_generator))
            if not document_data.document_id
            else document_data.document_id
        )
        documents_dict = document_data.model_dump(exclude_unset=True)
        self.collection.insert_one(documents_dict)
        return document_data.document_id

    @handle_exceptions
    def get_document(self, document_id: str) -> DocumentSchema | None:
        """Retrieve a document by its ID."""
        document = self.collection.find_one({"document_id": document_id})
        return DocumentSchema(**document) if document else None

    @handle_exceptions
    def delete_document(self, document_id: str) -> bool:
        """Delete a document by its ID."""
        result = self.collection.delete_one({"document_id": document_id})
        return result.deleted_count > 0

    @handle_exceptions
    def list_documents(self, workspace_id: str) -> list[DocumentSchema]:
        """List all documents in a workspace."""
        documents = self.collection.find({"workspace_id": workspace_id})
        return [DocumentSchema(**doc) for doc in documents]
