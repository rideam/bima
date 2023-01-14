from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

import uuid

from src.database.models import Users
from src.database.models import AccessLevels
from src.schemas.token import Status
from src.schemas.users import UserOutSchema
from src.schemas.access_levels import AccessLevelOutSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)
    user_dict = user.dict(exclude_unset=True)

    try:
        db_access_level = await AccessLevelOutSchema.from_queryset_single(AccessLevels.get(type="basic"))
        user_dict["access_level_id"] = db_access_level.id
    except DoesNotExist:
        try:
            access_level_obj = await AccessLevels.create(id=uuid.uuid4(), type='basic', menu={})
            user_dict["access_level_id"] = access_level_obj.id
        except IntegrityError:
            raise HTTPException(status_code=401, detail=f"Could not assign access level")

    try:
        user_obj = await Users.create(**user_dict)
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
