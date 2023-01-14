from fastapi import HTTPException
from src.schemas.token import Status
from src.database.models import Regions
from src.schemas.regions import RegionOutSchema


def is_allowed(user):
    allowed = ["admin", "super_admin"]
    if user.access_level.type in allowed:
        return True
    return False


async def create_region(data, current_user) -> RegionOutSchema:
    if is_allowed(current_user):
        region_dict = data.dict(exclude_unset=True)
        region_obj = await Regions.create(**region_dict)
        return await RegionOutSchema.from_tortoise_orm(region_obj)
    raise HTTPException(status_code=403, detail=f"Not authorized")


async def get_region(region_id) -> RegionOutSchema:
    return await RegionOutSchema.from_queryset_single(Regions.get(id=region_id))


async def delete_region(region_id, current_user) -> Status:
    if is_allowed(current_user):
        deleted_count = await Regions.filter(id=region_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
        return Status(message=f"Deleted region {region_id}")
    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
