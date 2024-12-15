from enum import StrEnum


class ArticleLanguageEnum(StrEnum):
    SLOVAK = "sk"
    ENGLISH = "en"


class ArticleStyleEnum(StrEnum):
    FACTUAL = "factual"
    TABLOID = "tabloid"


WMO_CODES_MAPPING = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Violent intensity",
    85: "Snow showers: slight intensity",
    86: "Snow showers: heavy intensity",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# WHO_UV_INDEX_MAPPING: dict[tuple[int, int], str] = {
#     (
#         0,
#         2,
#     ): "Low risk of harm - Wear sunglasses on bright days. If you burn easily, cover up and use broad spectrum SPF 15+ sunscreen. Bright surfaces, sand, water, and snow, will increase UV exposure.",
#     (
#         3,
#         5,
#     ): "Moderate risk of harm - Stay in shade near midday when the sun is strongest. If outdoors, wear sun-protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 50+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.",
#     (
#         6,
#         7,
#     ): "High risk of harm - Reduce time in the sun between 10 a.m. and 4 p.m. If outdoors, seek shade and wear sun-protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 50+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.",
#     (
#         8,
#         10,
#     ): "Very high risk of harm - Minimize sun exposure between 10 a.m. and 4 p.m. If outdoors, seek shade and wear sun-protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 50+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.",
#     (
#         11,
#         100,
#     ): "Extreme risk of harm - Try to avoid sun exposure between 10 a.m. and 4 p.m. If outdoors, seek shade and wear sun-protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 50+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.",
# }

WHO_UV_INDEX_MAPPING: dict[tuple[int, int], str] = {
    (0, 2): "UV index {} - You can safely enjoy being outside!",
    (
        3,
        7,
    ): "UV index {} - Seek shade during midday hours! Slip on a shirt, slop on sunscreen and slap on hat!",
    (
        8,
        20,
    ): "UV index {} - Avoid being outside during midday hours! Make sure you seek shade! Shirt, sunscreen and hat are a must!",
}

ARTICLE_STYLE_MAP = {
    ArticleStyleEnum.TABLOID: "Write a dramatic and attention-grabbing article with vivid language and an emotional tone, but ensure it stays grounded by accurately using the user-supplied data.",
    ArticleStyleEnum.FACTUAL: "Write a clear, objective, and fact-based article that presents the information accurately while keeping it engaging and interesting.",
}
