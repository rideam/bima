from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist

import src.queries.strike_events as crud
from src.schemas.strike_events import StrikeEventOutSchema, StrikeEventInSchema

router = APIRouter()


@router.post(
    "/strike_event",
    response_model=StrikeEventOutSchema,
    tags=["StrikeEvent"]
)
async def create_strike_event(strike_event: StrikeEventInSchema) -> StrikeEventOutSchema:
    return await crud.create_strike_event(strike_event)


@router.get(
    "/strike_event/{strike_event_id}",
    response_model=StrikeEventOutSchema,
    tags=["StrikeEvent"]
)
async def get_strike_event(strike_event_id: str) -> StrikeEventOutSchema:
    try:
        return await crud.get_strike_event(strike_event_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="StrikeEvent data does not exist",
        )
