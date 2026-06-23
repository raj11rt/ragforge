from fastapi import APIRouter

from app.db.database import SessionLocal
from app.db.models import BenchmarkResultDB
from app.services.leaderboard_service import (
    LeaderboardService,
)

router = APIRouter()


@router.get("/")
def get_leaderboard():

    db = SessionLocal()

    results = (
        db.query(BenchmarkResultDB)
        .all()
    )

    db.close()

    return LeaderboardService.build(results)