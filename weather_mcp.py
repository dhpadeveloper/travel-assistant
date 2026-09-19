from datetime import date, timedelta
import logging
import requests
import sys
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="mcp.log",
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "Weather Server",
    instructions=(
        "This MCP server provides weather-related tools. "
        "Use get_weather to fetch current weather data for those coordinates."
    ),
)

SINGAPORE_LATITUDE = 1.3521
SINGAPORE_LONGITUDE = 103.8198


@mcp.tool(
    description="Get the current or forecast weather for Singapore. "
    "Use this tool when the user asks about Singapore's weather, "
    "temperature, rain, or forecast."
)
def get_singapore_weather(
    start_date: str = "",
    days: int = 3,
) -> dict:
    """Get the current/forecast weather for Singapore."""

    if not start_date:

        start = date.today()

    else:

        start = date.fromisoformat(start_date)

    end = start + timedelta(days=days - 1)
    
    logger.info(
            "[WEATHER MCP] get_singapore_weather called | start_date=%s, end_date=%s",
            start,
            end,
        )

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": SINGAPORE_LATITUDE,
        "longitude": SINGAPORE_LONGITUDE,
        "daily": (
            "weather_code,"
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "rain_sum"
        ),
        "timezone": "Asia/Singapore",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
    }

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    daily = data.get("daily", {})

    forecast = []

    for i, day in enumerate(daily.get("time", [])):

        forecast.append(
            {
                "date": day,
                "temperature_max_c": (daily["temperature_2m_max"][i]),
                "temperature_min_c": (daily["temperature_2m_min"][i]),
                "rain_probability_percent": (daily["precipitation_probability_max"][i]),
                "rain_mm": (daily["rain_sum"][i]),
                "weather_code": (daily["weather_code"][i]),
            }
        )

    return {
        "location": "Singapore",
        "source": "Open-Meteo",
        "forecast": forecast,
    }


if __name__ == "__main__":

    mcp.run(transport="stdio")
