from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist

import src.queries.weather as crud
from src.schemas.weather import WeatherOutSchema, WeatherInSchema

router = APIRouter()


@router.post(
    "/weather",
    response_model=WeatherOutSchema,
    tags=["Weather"]
)
async def create_weather_data(weatherinfo: WeatherInSchema) -> WeatherOutSchema:
    return await crud.create_weatherinfo(weatherinfo)


@router.get(
    "/weather/{weather_id}",
    response_model=WeatherOutSchema,
    tags=["Weather"]
)
async def get_weather_data(weather_id: str) -> WeatherOutSchema:
    try:
        return await crud.get_weather_data(weather_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Weather data does not exist",
        )
