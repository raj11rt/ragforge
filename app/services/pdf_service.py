from pathlib import Path
from pypdf import PdfReader
from uuid import uuid4


class PDFService:
    @staticmethod
    def save_pdf(file, upload_dir: str = "app/storage/uploads") -> Path:
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)

        extension = Path(file.filename).suffix
        unique_filename = f"{uuid4()}{extension}"
        file_path = upload_path / unique_filename

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return file_path

    @staticmethod
    def extract_text(file_path: Path):
        reader = PdfReader(str(file_path))

        pages_text = []
        total_chars = 0

        for page in reader.pages:
            text = page.extract_text() or ""
            pages_text.append(text)
            total_chars += len(text)

        return {
            "text": "\n".join(pages_text),
            "num_pages": len(reader.pages),
            "num_characters": total_chars,
        }