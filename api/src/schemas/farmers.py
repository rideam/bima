from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Farmers

FarmerInSchema = pydantic_model_creator(
    Farmers,
    name="FarmerIn",
    exclude=["user_id"],
    exclude_readonly=True
)

FarmerOutSchema = pydantic_model_creator(
    Farmers,
    name="FarmerOut",
    exclude=[
        "created_at",
        "modified_at",
        "user.password",
        "user.created_at",
        "user.modified_at",
        "policies.crop.weather",
        "policies.strike_events",
        "farms.weather",
    ]
)


class UpdateFarmer(BaseModel):
    wallet: Optional[str]
    address: Optional[str]
