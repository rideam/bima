from fastapi import APIRouter, Depends, HTTPException, Query
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist
from uuid import UUID

import src.queries.regions as crud
from src.schemas.regions import RegionOutSchema, RegionInSchema
from src.schemas.users import UserOutSchema
from src.schemas.token import Status
from src.auth.jwthandler import get_current_user

router = APIRouter()


@router.post(
    "/region",
    response_model=RegionOutSchema,
    tags=["Region"],
    dependencies=[Depends(get_current_user)]
)
async def create_region(
        region: RegionInSchema,
        current_user: UserOutSchema = Depends(get_current_user)
) -> RegionOutSchema:
    return await crud.create_region(region, current_user)


@router.get(
    "/region/{region_id}",
    response_model=RegionOutSchema,
    tags=["Region"]
)
async def get_region(region_id: UUID = Query(None, description="Arg1", example='3fa85f64-5717-4562-b3fc-2c963f66afa6')) -> RegionOutSchema:
    try:
        return await crud.get_region(region_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Region data does not exist",
        )


@router.delete(
    "/region/{region_id}",
    response_model=Status,
    responses={
        404: {"model": HTTPNotFoundError},
    },
    dependencies=[Depends(get_current_user)],
    tags=["Region"]
)
async def delete_region(
        region_id: UUID, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_region(region_id, current_user)
