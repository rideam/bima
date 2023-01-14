from src.database.models import StrikeEvents
from src.schemas.strike_events import StrikeEventOutSchema


async def get_strike_event(strike_event_id) -> StrikeEventOutSchema:
    return await StrikeEventOutSchema.from_queryset_single(StrikeEvents.get(id=strike_event_id))


async def create_strike_event(data) -> StrikeEventOutSchema:
    strike_event_dict = data.dict(exclude_unset=True)
    strike_event_obj = await StrikeEvents.create(**strike_event_dict)
    return await StrikeEventOutSchema.from_tortoise_orm(strike_event_obj)