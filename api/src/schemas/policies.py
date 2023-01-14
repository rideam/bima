from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Policies

PolicyInSchema = pydantic_model_creator(
    Policies,
    name="PolicyIn",
    exclude_readonly=True
)

PolicyOutSchema = pydantic_model_creator(
    Policies,
    name="PolicyOut",
    exclude=[
        "created_at",
        "modified_at",
    ]
)

PolicyDatabaseSchema = pydantic_model_creator(
    Policies,
    name="Policy",
    exclude=[
        "created_at",
        "modified_at"
    ]
)
