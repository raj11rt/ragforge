from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import PDFService

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    saved_path = PDFService.save_pdf(file)
    result = PDFService.extract_text(saved_path)

    return {
        "filename": file.filename,
        "saved_path": str(saved_path),
        "pages": result["num_pages"],
        "characters": result["num_characters"],
        "status": "uploaded successfully"
    }