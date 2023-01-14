from fastapi import HTTPException
from src.schemas.token import Status
from src.database.models import Crops
from src.schemas.crops import CropOutSchema

def is_allowed(user):
    allowed = ["admin", "super_admin", "farmer"]
    if user.access_level.type in allowed:
        return True
    return False


async def create_crop(data, current_user ) -> CropOutSchema:
    if is_allowed(current_user):
        crop_dict = data.dict(exclude_unset=True)
        crop_obj = await Crops.create(**crop_dict)
        return await CropOutSchema.from_tortoise_orm(crop_obj)
    raise HTTPException(status_code=403, detail=f"Not authorized")


async def get_crop(crop_id) -> CropOutSchema:
    return await CropOutSchema.from_queryset_single(Crops.get(id=crop_id))


async def delete_crop(crop_id, current_user) -> Status:
    if is_allowed(current_user):
        deleted_count = await Crops.filter(id=crop_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Crop {crop_id} not found")
        return Status(message=f"Deleted crop {crop_id}")
    raise HTTPException(status_code=403, detail=f"Not authorized to delete")

