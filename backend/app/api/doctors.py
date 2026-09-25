from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.doctor import DoctorSearchResponse
from app.services.search import search_doctors

router = APIRouter()


@router.get("/doctors/search", response_model=DoctorSearchResponse)
def search_doctors_endpoint(q: str, db: Session = Depends(get_db)) -> DoctorSearchResponse:
    query = q.strip()
    if not query:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_request", "message": "Search query cannot be empty"},
        )
    if len(query) > 200:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_request", "message": "Search query must be 200 characters or fewer"},
        )

    try:
        results = search_doctors(db, query)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_server_error", "message": "Unable to search doctors"},
        ) from exc

    count = len(results)
    message = (
        f"Found {count} matching doctor" + ("s" if count != 1 else "")
        if count
        else "No results found. Try a different search term."
    )
    return DoctorSearchResponse(results=results, count=count, message=message)
