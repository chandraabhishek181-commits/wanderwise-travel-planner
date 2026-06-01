"""Configuration constants for WanderWise application."""

# Application Metadata
APP_NAME = "WanderWise"
APP_VERSION = "1.0.0"
APP_ICON = "✈️"

# API Configuration
AMADEUS_BASE_URL = "https://test.api.amadeus.com"
WEATHER_BASE_URL = "https://api.openweathermap.org"

# Default Values
DEFAULT_DURATION_DAYS = 7
DEFAULT_TRAVELERS = 2
DEFAULT_BUDGET = "Medium (₹50k-2L)"

# Budget Ranges (in INR)
BUDGET_RANGES = {
    "Low (₹50k or less)": (40000, 50000),
    "Medium (₹50k-2L)": (100000, 200000),
    "Luxury (₹2L+)": (250000, 500000)
}

# Activity Types by Trip Category
ACTIVITIES = {
    "Adventure": ["Rock Climbing", "Trekking", "Water Sports", "Zip-lining", "Paragliding"],
    "Relaxation": ["Spa Treatment", "Beach Day", "Wellness Yoga", "Resort Relaxation", "Meditation"],
    "Cultural": ["Museum Visit", "Historical Tour", "Local Festival", "Temple Exploration", "Art Gallery"],
    "Romantic": ["Sunset Dinner", "Couples Spa", "Wine Tasting", "Scenic Cruise", "Candlelit Beach Walk"],
    "Family": ["Theme Park", "Zoo Visit", "Beach Day", "Adventure Park", "Local Markets"],
    "Solo": ["Self-Guided Tour", "Hostel Socializing", "Photography Walk", "Cooking Class", "Hiking"]
}

# Caching TTL (Time To Live) in seconds
CACHE_TTL_FLIGHTS = 3600  # 1 hour
CACHE_TTL_WEATHER = 1800  # 30 minutes

# Popular Indian Cities
POPULAR_DESTINATIONS = {
    "Delhi": "DEL",
    "Mumbai": "BOM",
    "Bangalore": "BLR",
    "Hyderabad": "HYD",
    "Kolkata": "CCU",
    "Chennai": "MAA",
    "Kochi": "COK",
    "Goa": "GOI",
    "Jaipur": "JAI",
    "Pune": "PNQ"
}

# API Rate Limits (requests per minute)
AMADEUS_RATE_LIMIT = 20
WEATHER_RATE_LIMIT = 60

# Session timeout (minutes)
SESSION_TIMEOUT = 30
