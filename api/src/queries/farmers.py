from src.database.models import Farmers
from src.schemas.farmers import FarmerOutSchema


async def get_farmer(farmer_id) -> FarmerOutSchema:
    return await FarmerOutSchema.from_queryset_single(Farmers.get(id=farmer_id))


async def create_farmer(data) -> FarmerOutSchema:
    farmer_dict = data.dict(exclude_unset=True)
    farmer_obj = await Farmers.create(**farmer_dict)
    return await FarmerOutSchema.from_tortoise_orm(farmer_obj)