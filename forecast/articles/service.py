from httpx import AsyncClient, Response

from forecast.articles.enums import WHO_UV_INDEX_MAPPING, WMO_CODES_MAPPING
from forecast.articles.schemas import (
    DailyForecastData,
    DailyForecastDataRaw,
    LocationData,
)
from forecast.config import CONFIG


async def geocode_location(httpx_client: AsyncClient, location: str) -> LocationData:
    response = await httpx_client.get(
        url=CONFIG.geoapify_geocode_api_url,
        params={
            "text": location,
            "apiKey": CONFIG.geoapify_api_key.get_secret_value(),
        },
        headers={"Accept": "application/json"},
    )
    # do some error handling
    # response.raise_for_status()

    geocode_body = response.json()
    highest_probability_result = geocode_body["features"][0]["properties"]

    return LocationData(
        formatted=highest_probability_result["formatted"],
        longitude=highest_probability_result["lon"],
        latitude=highest_probability_result["lat"],
    )


def preprocess_wind_direction(value: int) -> str:
    compass_directions = (
        "North",
        "North-East",
        "East",
        "South-East",
        "South",
        "South-West",
        "West",
        "North-West",
    )
    section = 360 / len(compass_directions)
    index = round(value / section) % len(compass_directions)
    return compass_directions[index]


def preprocess_weather_code(value: int) -> str:
    return WMO_CODES_MAPPING.get(value, "")


def get_uv_action_by_index(value: float) -> str:
    for (lower, upper), action in WHO_UV_INDEX_MAPPING.items():
        if lower <= value <= upper:
            return action.format(value)

    return ""


def seconds_to_hours_and_minutes(value: int) -> str:
    hours = value // 60
    minutes = value % 60
    return f"{hours}hours {minutes}minutes"


def parse_forecast_response(response: Response) -> DailyForecastData:
    flat_response = {}
    json_response = response.json()
    for key, value in json_response["daily"].items():
        flat_response[key] = value[0]
    raw_data = DailyForecastDataRaw(**flat_response)
    raw_data_dump = raw_data.model_dump()

    raw_data_dump.pop("uv_index_max")
    raw_data_dump.pop("uv_index_clear_sky_max")
    raw_data_dump.pop("wind_direction_10m_dominant")
    raw_data_dump.pop("weather_code")
    raw_data_dump.pop("daylight_duration")

    return DailyForecastData(
        **raw_data_dump,
        uv_index_max=get_uv_action_by_index(raw_data.uv_index_max),
        uv_index_clear_sky_max=get_uv_action_by_index(raw_data.uv_index_clear_sky_max),
        wind_direction_10m_dominant=preprocess_wind_direction(
            raw_data.wind_direction_10m_dominant
        ),
        daylight_duration=seconds_to_hours_and_minutes(
            round(raw_data.daylight_duration)
        ),
        weather_code=preprocess_weather_code(raw_data.weather_code),
    )


async def weather_forecast_data(
    httpx_client: AsyncClient, date: str, location: LocationData
) -> DailyForecastData:
    response = await httpx_client.get(
        url=CONFIG.forecast_api_url,
        params={
            "latitude": location.latitude,
            "longitude": location.longitude,
            "start_date": date,
            "end_date": date,
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "sunrise",
                "sunset",
                "daylight_duration",
                "uv_index_max",
                "uv_index_clear_sky_max",
                "precipitation_sum",
                "rain_sum",
                "showers_sum",
                "snowfall_sum",
                "precipitation_hours",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "wind_direction_10m_dominant",
            ],
        },
        headers={"Accept": "application/json"},
    )

    # do some error handling
    # response.raise_for_status()

    return parse_forecast_response(response)
