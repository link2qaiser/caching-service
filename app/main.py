from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from .database import get_session, create_db_and_tables
from .models import PayloadRequest, PayloadResponse
from .services.cache_service import CacheService

app = FastAPI(title="Caching Service")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/payload")
async def create_payload(
    payload: PayloadRequest, session: Session = Depends(get_session)
) -> dict:
    if len(payload.list_1) != len(payload.list_2):
        raise HTTPException(status_code=400, detail="Lists must have equal length")

    cache_service = CacheService(session)
    result, payload_id = await cache_service.get_or_create_payload(
        payload.list_1, payload.list_2
    )

    return {"message": "Payload created", "id": payload_id}


@app.get("/payload/{payload_id}")
async def get_payload(
    payload_id: int, session: Session = Depends(get_session)
) -> PayloadResponse:
    cache_service = CacheService(session)
    result = await cache_service.get_payload(payload_id)

    if not result:
        raise HTTPException(status_code=404, detail="Payload not found")

    return PayloadResponse(output=result)
