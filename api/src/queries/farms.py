from src.database.models import Farms
from src.schemas.farms import FarmOutSchema


async def get_farm(farm_id) -> FarmOutSchema:
    return await FarmOutSchema.from_queryset_single(Farms.get(id=farm_id))


async def create_farm(data) -> FarmOutSchema:
    farm_dict = data.dict(exclude_unset=True)
    farm_obj = await Farms.create(**farm_dict)
    return await FarmOutSchema.from_tortoise_orm(farm_obj)