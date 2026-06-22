from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def documents_home():
    return {
        "message": "Documents API is working"
    }