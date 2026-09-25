from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.doctor import SearchResponse
from app.services.doctor_search import search_doctors

router = APIRouter()


@router.get("/doctors/search", response_model=SearchResponse)
def get_doctors(q: str = Query(...), db: Session = Depends(get_db)):
    query = q.strip()
    if not query:
        return JSONResponse(
            status_code=400,
            content={"error": "invalid_request", "message": "Search query is required"},
        )
    if len(query) > 200:
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_request",
                "message": "Search terms must be 200 characters or fewer",
            },
        )

    results = search_doctors(db, query)
    count = len(results)
    message = (
        f"Found {count} matching doctor(s)."
        if count
        else "No doctors found matching your search."
    )
    return {"results": results, "count": count, "message": message}
