from pathlib import Path


class DocumentRepository:
    STORAGE_DIR = Path("app/storage/extracted")

    @classmethod
    def load_text(cls, document_id: str) -> str:
        file_path = cls.STORAGE_DIR / f"{document_id}.txt"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Document {document_id} not found"
            )

        return file_path.read_text(encoding="utf-8")