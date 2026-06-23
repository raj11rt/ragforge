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
    result = PDFService.extract_and_chunk(
        saved_path,
        chunk_size=512,
        chunk_overlap=50,
    )

    return {
        "document_id": result["document_id"],
        "filename": file.filename,
        "saved_path": str(saved_path),
        "pages": result["num_pages"],
        "characters": result["num_characters"],
        "status": "uploaded successfully",
        "chunks_created": result["num_chunks"]
    }