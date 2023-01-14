from src.database.models import Policies
from src.schemas.policies import PolicyOutSchema


async def get_policy(policy_id) -> PolicyOutSchema:
    return await PolicyOutSchema.from_queryset_single(Policies.get(id=policy_id))


async def create_policy(data) -> PolicyOutSchema:
    policy_dict = data.dict(exclude_unset=True)
    policy_obj = await Policies.create(**policy_dict)
    return await PolicyOutSchema.from_tortoise_orm(policy_obj)