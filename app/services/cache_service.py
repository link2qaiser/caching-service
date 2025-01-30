from typing import List, Tuple, Optional
from sqlmodel import Session, select
from ..models import CacheEntry
from .transformer import generate_hash, transform_string, interleave_lists


class CacheService:
    def __init__(self, session: Session):
        self.session = session

    async def get_or_create_payload(
        self, list_1: List[str], list_2: List[str]
    ) -> Tuple[str, bool]:
        """Get cached payload or create new one if not exists."""
        input_hash = generate_hash(list_1, list_2)

        # Check cache
        cache_entry = self.session.exec(
            select(CacheEntry).where(CacheEntry.input_hash == input_hash)
        ).first()

        if cache_entry:
            return cache_entry.transformed_data, cache_entry.id

        # Transform and cache if not found
        transformed_1 = [transform_string(s) for s in list_1]
        transformed_2 = [transform_string(s) for s in list_2]
        result = interleave_lists(transformed_1, transformed_2)

        cache_entry = CacheEntry(input_hash=input_hash, transformed_data=result)
        self.session.add(cache_entry)
        self.session.commit()
        self.session.refresh(cache_entry)

        return result, cache_entry.id

    async def get_payload(self, payload_id: int) -> Optional[str]:
        """Retrieve a cached payload by ID."""
        cache_entry = self.session.exec(
            select(CacheEntry).where(CacheEntry.id == payload_id)
        ).first()
        return cache_entry.transformed_data if cache_entry else None
