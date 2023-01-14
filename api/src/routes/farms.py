from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist

import src.queries.farms as crud
from src.schemas.farms import FarmOutSchema, FarmInSchema

router = APIRouter()


@router.post(
    "/farm",
    response_model=FarmOutSchema,
    tags=["Farm"]
)
async def create_farm(farm: FarmInSchema) -> FarmOutSchema:
    return await crud.create_farm(farm)


@router.get(
    "/farm/{farm_id}",
    response_model=FarmOutSchema,
    tags=["Farm"]
)
async def get_farm(farm_id: str) -> FarmOutSchema:
    try:
        return await crud.get_farm(farm_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Farm data does not exist",
        )
