from app.db.database import SessionLocal
from app.db.models import DocumentDB


class DocumentRepository:
    @classmethod
    def load_text(cls, document_id: str) -> str:
        db = SessionLocal()
        try:
            doc = db.query(DocumentDB).filter(DocumentDB.id == document_id).first()
            if not doc:
                raise FileNotFoundError(
                    f"Document {document_id} not found in database"
                )
            return doc.full_text
        finally:
            db.close()