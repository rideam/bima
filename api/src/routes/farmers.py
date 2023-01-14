from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist

import src.queries.farmers as crud
from src.schemas.farmers import FarmerOutSchema, FarmerInSchema

from src.auth.jwthandler import (
    get_current_user,
)

router = APIRouter()


@router.post(
    "/farmer",
    response_model=FarmerOutSchema,
    dependencies=[Depends(get_current_user)],
    tags=["User"]
)
async def create_farmer(farmer: FarmerInSchema) -> FarmerOutSchema:
    return await crud.create_farmer(farmer)


@router.get(
    "/farmer/{farmer_id}",
    response_model=FarmerOutSchema,
    dependencies=[Depends(get_current_user)],
    tags=["User"]
)
async def get_farmer(farmer_id: str) -> FarmerOutSchema:
    try:
        return await crud.get_farmer(farmer_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Farmer data does not exist",
        )
