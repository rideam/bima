from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist

import src.queries.policies as crud
from src.schemas.policies import PolicyOutSchema, PolicyInSchema

router = APIRouter()


@router.post(
    "/policy",
    response_model=PolicyOutSchema,
    tags=["Policy"]
)
async def create_policy(policy: PolicyInSchema) -> PolicyOutSchema:
    return await crud.create_policy(policy)


@router.get(
    "/policy/{policy_id}",
    response_model=PolicyOutSchema,
    tags=["Policy"]
)
async def get_policy(policy_id: str) -> PolicyOutSchema:
    try:
        return await crud.get_policy(policy_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Policy data does not exist",
        )
