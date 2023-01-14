from fastapi import APIRouter, Depends, HTTPException, Query
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist
from uuid import UUID

import src.queries.crops as crud
from src.schemas.crops import CropOutSchema, CropInSchema
from src.schemas.users import UserOutSchema
from src.schemas.token import Status
from src.auth.jwthandler import get_current_user

router = APIRouter()


@router.post(
    "/crop",
    response_model=CropOutSchema,
    tags=["Crop"]
)
async def create_crop(crop: CropInSchema) -> CropOutSchema:
    return await crud.create_crop(crop)


@router.get(
    "/crop/{crop_id}",
    response_model=CropOutSchema,
    tags=["Crop"]
)
async def get_crop(crop_id: UUID) -> CropOutSchema:
    try:
        return await crud.get_crop(crop_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Crop data does not exist",
        )


@router.delete(
    "/crop/{crop_id}",
    response_model=Status,
    responses={
        404: {"model": HTTPNotFoundError},
    },
    dependencies=[Depends(get_current_user)],
    tags=["Crop"]
)
async def delete_crop(
        crop_id: UUID, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_crop(crop_id, current_user)