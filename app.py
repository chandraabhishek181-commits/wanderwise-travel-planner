import streamlit as st
import datetime
import random
import requests
import urllib.parse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# UTILITY FUNCTIONS & API INTEGRATIONS
# ============================================================================

def get_api_keys() -> Dict[str, str]:
    """
    Securely retrieve API keys from Streamlit secrets.
    Never expose keys in code or UI.
    """
    return {
        "aviation_key": st.secrets.get("aviation_api_key", ""),
        "weather_key": st.secrets.get("openweathermap_api_key", ""),
        "amadeus_key": st.secrets.get("amadeus_api_key", ""),
    }


@st.cache_data(ttl=3600)
def fetch_flights(
    origin: str,
    destination: str,
    departure_date: datetime.date,
    return_date: Optional[datetime.date] = None,
    is_roundtrip: bool = False
) -> List[Dict]:
    """
    Fetch real flight data from Amadeus API.
    Cached for 1 hour to minimize API calls.
    
    Args:
        origin: 3-letter IATA code (e.g., 'DEL')
        destination: 3-letter IATA code (e.g., 'BOM')
        departure_date: Flight departure date
        return_date: Return date for round trips
        is_roundtrip: Whether this is a round trip
    
    Returns:
        List of flight dictionaries with price, airline, duration
    """
    api_keys = get_api_keys()
    amadeus_key = api_keys["amadeus_key"]
    
    if not amadeus_key:
        logger.warning("Amadeus API key not configured. Using mock data.")
        return get_mock_flights(origin, destination)
    
    try:
        # Amadeus Flight Offers Search
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date.isoformat(),
            "adults": 1,
            "max": 5
        }
        
        if is_roundtrip and return_date:
            params["returnDate"] = return_date.isoformat()
        
        headers = {
            "Authorization": f"Bearer {amadeus_key}"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        flights = []
        
        for offer in data.get("data", [])[:5]:
            flight_info = {
                "airline": offer["validatingAirlineCodes"][0],
                "price": offer["price"]["total"],
                "currency": offer["price"]["currency"],
                "duration": offer["itineraries"][0]["duration"],
                "segments": len(offer["itineraries"][0]["segments"])
            }
            flights.append(flight_info)
        
        return flights
    
    except requests.exceptions.Timeout:
        st.error("⏱️ Flight API request timed out. Using mock data.")
        return get_mock_flights(origin, destination)
    except requests.exceptions.HTTPError as e:
        logger.error(f"Flight API error: {e}")
        st.warning(f"⚠️ Could not fetch real flights: {e.response.status_code}")
        return get_mock_flights(origin, destination)
    except Exception as e:
        logger.error(f"Unexpected error fetching flights: {e}")
        st.error(f"❌ Error fetching flights: {str(e)}")
        return get_mock_flights(origin, destination)


def get_mock_flights(origin: str, destination: str) -> List[Dict]:
    """
    Return mock flight data for testing/fallback.
    """
    airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "GoAir"]
    return [
        {
            "airline": random.choice(airlines),
            "price": str(random.randint(3000, 15000)),
            "currency": "INR",
            "duration": "PT2H30M",
            "segments": 1
        }
        for _ in range(5)
    ]


@st.cache_data(ttl=1800)
def fetch_weather(city: str, lat: Optional[float] = None, lon: Optional[float] = None) -> Optional[Dict]:
    """
    Fetch weather forecast for destination.
    """
    api_keys = get_api_keys()
    weather_key = api_keys["weather_key"]
    
    if not weather_key:
        logger.warning("OpenWeatherMap API key not configured.")
        return None
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": weather_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return None


def generate_travel_plan(
    destination: str,
    trip_type: str,
    days: int,
    budget: str,
    travelers: int,
    origin: str,
    start_date: datetime.date
) -> Dict:
    """
    Generate a comprehensive travel plan with itinerary and costs.
    
    Args:
        destination: Destination city/region
        trip_type: Type of trip (Adventure, Relaxation, etc.)
        days: Duration in days
        budget: Budget category
        travelers: Number of travelers
        origin: Origin city
        start_date: Start date of trip
    
    Returns:
        Dictionary with itinerary, costs, and metadata
    """
    # Activity mapping by trip type
    activities_map = {
        "Adventure": ["Rock Climbing", "Trekking", "Water Sports", "Zip-lining", "Paragliding"],
        "Relaxation": ["Spa Treatment", "Beach Day", "Wellness Yoga", "Resort Relaxation", "Meditation"],
        "Cultural": ["Museum Visit", "Historical Tour", "Local Festival", "Temple Exploration", "Art Gallery"],
        "Romantic": ["Sunset Dinner", "Couples Spa", "Wine Tasting", "Scenic Cruise", "Candlelit Beach Walk"],
        "Family": ["Theme Park", "Zoo Visit", "Beach Day", "Adventure Park", "Local Markets"],
        "Solo": ["Self-Guided Tour", "Hostel Socializing", "Photography Walk", "Cooking Class", "Hiking"]
    }
    
    # Cost ranges by budget
    cost_ranges = {
        "Low (₹50k or less)": (40000, 50000),
        "Medium (₹50k-2L)": (100000, 200000),
        "Luxury (₹2L+)": (250000, 500000)
    }
    
    activities = activities_map.get(trip_type, activities_map["Relaxation"])
    cost_min, cost_max = cost_ranges.get(budget, cost_ranges["Medium (₹50k-2L)"])
    total_cost = random.randint(cost_min, cost_max)
    
    # Generate day-by-day itinerary
    itinerary = {}
    for day in range(1, days + 1):
        activity = random.choice(activities)
        itinerary[day] = f"{activity} in {destination}"
    
    return {
        "destination": destination,
        "origin": origin,
        "trip_type": trip_type,
        "start_date": start_date,
        "duration": days,
        "travelers": travelers,
        "itinerary": itinerary,
        "total_cost": total_cost,
        "per_person": total_cost // travelers,
        "budget_category": budget
    }


def create_pdf_plan(
    plan: Dict,
    destination: str,
    origin: str,
    duration: int,
    travelers: int,
    start_date: datetime.date
) -> io.BytesIO:
    """
    Generate a PDF travel plan document.
    
    Args:
        plan: Travel plan dictionary
        destination: Destination name
        origin: Origin name
        duration: Number of days
        travelers: Number of travelers
        start_date: Trip start date
    
    Returns:
        BytesIO object containing PDF data
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 60, "🌍 WanderWise Travel Plan")
    
    # Header info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 100, f"{destination} — {duration} Days")
    
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 125, f"From: {origin} → {destination}")
    c.drawString(50, height - 145, f"Duration: {duration} days | Travelers: {travelers}")
    c.drawString(50, height - 165, f"Start Date: {start_date.strftime('%B %d, %Y')}")
    c.drawString(50, height - 185, f"Trip Type: {plan.get('trip_type', 'N/A')}")
    
    # Itinerary
    y = height - 220
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "📅 Day-by-Day Itinerary:")
    y -= 25
    
    c.setFont("Helvetica", 10)
    for day, activity in plan['itinerary'].items():
        if y < 100:
            c.showPage()
            y = height - 50
        c.drawString(70, y, f"Day {day}: {activity}")
        y -= 20
    
    # Cost breakdown
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "💰 Budget Breakdown:")
    y -= 20
    
    c.setFont("Helvetica", 10)
    c.drawString(70, y, f"Total Budget: ₹{plan['total_cost']:,}")
    y -= 15
    c.drawString(70, y, f"Per Person: ₹{plan['per_person']:,}")
    y -= 15
    c.drawString(70, y, f"Budget Category: {plan.get('budget_category', 'N/A')}")
    
    # Footer
    y -= 30
    c.setFont("Helvetica-Italic", 9)
    c.drawString(50, y, "Book via MakeMyTrip | IRCTC | Amadeus Flight Search")
    c.drawString(50, y - 15, "Generated by WanderWise Travel Planner")
    
    c.save()
    buffer.seek(0)
    return buffer


def validate_inputs(origin: str, destination: str, start_date: datetime.date, duration: int) -> tuple[bool, str]:
    """
    Validate user inputs before making API calls.
    
    Returns:
        (is_valid: bool, error_message: str)
    """
    if not origin or len(origin.strip()) == 0:
        return False, "❌ Origin cannot be empty"
    
    if not destination or len(destination.strip()) == 0:
        return False, "❌ Destination cannot be empty"
    
    if start_date < datetime.date.today():
        return False, "❌ Start date must be in the future"
    
    if duration < 1 or duration > 90:
        return False, "❌ Duration must be between 1 and 90 days"
    
    return True, ""


# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(
    page_title="WanderWise",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="manifest" href="manifest.json">
""", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.saved_plans = {}

# Authentication
if not st.session_state.logged_in:
    st.sidebar.header("🔐 Login")
    username = st.sidebar.text_input("Username", placeholder="Enter your name")
    if st.sidebar.button("Login", use_container_width=True):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.sidebar.error("Please enter a username")
else:
    st.sidebar.success(f"👋 Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

if st.session_state.logged_in:
    st.title("🌍 WanderWise: Smart Travel Planner")
    st.markdown("### Flights • Trains • Hotels • PDF Export")
    
    # Sidebar - Trip Planner
    st.sidebar.header("📝 Plan Your Trip")
    
    with st.sidebar.form("trip_form"):
        origin = st.text_input("Origin (IATA Code)", "DEL", help="e.g., DEL, BOM, COK")
        destination = st.text_input("Destination", "BOM", help="City or IATA code")
        trip_type = st.selectbox(
            "Trip Type",
            ["Adventure", "Relaxation", "Cultural", "Romantic", "Family", "Solo"]
        )
        duration = st.slider("Duration (days)", 1, 90, 7)
        budget = st.selectbox(
            "Budget",
            ["Low (₹50k or less)", "Medium (₹50k-2L)", "Luxury (₹2L+)"]
        )
        travelers = st.number_input("Number of Travelers", 1, 20, 2)
        start_date = st.date_input(
            "Start Date",
            datetime.date.today() + datetime.timedelta(days=30)
        )
        is_roundtrip = st.checkbox("Round Trip", value=True)
        
        if is_roundtrip:
            return_date = st.date_input(
                "Return Date",
                datetime.date.today() + datetime.timedelta(days=37)
            )
        else:
            return_date = None
        
        submitted = st.form_submit_button("🚀 Generate Plan", use_container_width=True)
    
    if submitted:
        # Validate inputs
        is_valid, error_msg = validate_inputs(origin, destination, start_date, duration)
        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("✨ Creating your personalized travel plan..."):
                plan = generate_travel_plan(
                    destination, trip_type, duration, budget, travelers, origin, start_date
                )
                
                st.session_state.current_plan = plan
                st.success("✅ Plan Generated Successfully!")
    
    # Display current plan if available
    if "current_plan" in st.session_state:
        plan = st.session_state.current_plan
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.header(f"{plan['destination']} — {plan['duration']} Days")
            
            # Flights & Trains
            st.subheader("🛫 Flights & Trains")
            
            with st.spinner("Fetching flight options..."):
                flights = fetch_flights(
                    plan['origin'][:3].upper(),
                    plan['destination'][:3].upper() if len(plan['destination']) >= 3 else "DEL",
                    plan['start_date'],
                    is_roundtrip=plan.get('is_roundtrip', False)
                )
            
            if flights:
                flight_col1, flight_col2, flight_col3 = st.columns(3)
                with flight_col1:
                    st.metric("✈️ Airline", flights[0].get('airline', 'N/A'))
                with flight_col2:
                    st.metric("💰 Price", f"₹{flights[0].get('price', 0)}")
                with flight_col3:
                    st.metric("⏱️ Duration", flights[0].get('duration', 'N/A'))
            
            # Train option
            irctc_url = f"https://www.irctc.co.in/nget/train-search?from={plan['origin'][:3].upper()}&to={plan['destination'][:3].upper()}"
            st.link_button("🚂 Book Trains on IRCTC", irctc_url, use_container_width=True)
            
            # Itinerary
            st.subheader("📅 Day-by-Day Itinerary")
            for day, activity in plan['itinerary'].items():
                st.write(f"**Day {day}**: {activity}")
            
            # Weather forecast
            st.subheader("🌤️ Weather Forecast")
            weather = fetch_weather(plan['destination'])
            if weather:
                temp = weather.get('main', {}).get('temp', 'N/A')
                description = weather.get('weather', [{}])[0].get('description', 'N/A')
                st.info(f"Temperature: {temp}°C | Conditions: {description.title()}")
            else:
                st.info("Weather data unavailable at this time")
        
        with col2:
            st.subheader("🏨 Accommodations")
            st.link_button(
                "🏩 Browse Hotels",
                f"https://www.makemytrip.com/hotels/{plan['destination'].lower()}-hotels.html",
                use_container_width=True
            )
            st.link_button(
                "🚗 Book Cabs",
                "https://www.makemytrip.com/cabs/",
                use_container_width=True
            )
            
            st.subheader("💰 Cost Breakdown")
            st.metric("💵 Total Budget", f"₹{plan['total_cost']:,}")
            st.metric("👤 Per Person", f"₹{plan['per_person']:,}")
            st.metric("👥 Travelers", plan['travelers'])
            st.metric("📅 Duration", f"{plan['duration']} days")
            
            # Action buttons
            st.subheader("📮 Actions")
            
            col_pdf, col_save = st.columns(2)
            
            with col_pdf:
                if st.button("📄 Download PDF", use_container_width=True):
                    pdf_buffer = create_pdf_plan(
                        plan,
                        plan['destination'],
                        plan['origin'],
                        plan['duration'],
                        plan['travelers'],
                        plan['start_date']
                    )
                    st.download_button(
                        label="⬇️ Get PDF",
                        data=pdf_buffer,
                        file_name=f"WanderWise_{plan['destination']}_{plan['start_date']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            
            with col_save:
                if st.button("💾 Save Plan", use_container_width=True):
                    plan_id = f"{plan['destination']}_{datetime.date.today()}"
                    st.session_state.saved_plans[plan_id] = plan
                    st.success("✅ Plan saved!")
    
    # Show saved plans
    if st.session_state.saved_plans:
        st.sidebar.subheader("💾 Your Saved Plans")
        for plan_id, saved_plan in st.session_state.saved_plans.items():
            if st.sidebar.button(f"📋 {plan_id}"):
                st.session_state.current_plan = saved_plan
                st.rerun()
else:
    st.info("👉 Please login to start planning your trip!")
