from src.database.models import Weather
from src.schemas.weather import WeatherOutSchema


async def get_weather_data(weather_id) -> WeatherOutSchema:
    return await WeatherOutSchema.from_queryset_single(Weather.get(id=weather_id))


async def create_weather_data(data) -> WeatherOutSchema:
    weather_dict = data.dict(exclude_unset=True)
    weather_obj = await Weather.create(**weather_dict)
    return await WeatherOutSchema.from_tortoise_orm(weather_obj)
