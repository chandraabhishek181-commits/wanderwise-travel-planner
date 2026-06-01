# 🌍 WanderWise: Smart Travel Planner

A modern, full-featured travel planning web application built with **Streamlit** that helps you create personalized itineraries, compare flights, book accommodations, and export travel plans as PDFs.

## ✨ Features

- 🔐 **User Authentication** - Simple login system with session management
- 🛫 **Real Flight Search** - Integrated with Amadeus API for live flight data
- 🚂 **Train Bookings** - Direct links to IRCTC train search
- 🏨 **Hotel Bookings** - Integration with MakeMyTrip for accommodations
- 📅 **Smart Itinerary** - AI-generated day-by-day activities based on trip type
- 💰 **Budget Calculator** - Personalized cost breakdown by traveler
- 🌤️ **Weather Forecast** - Real-time weather for your destination
- 📄 **PDF Export** - Download complete travel plans as professional PDFs
- 💾 **Save Plans** - Store and revisit your travel plans anytime
- 🎫 **Multiple Trip Types** - Adventure, Relaxation, Cultural, Romantic, Family, Solo

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chandraabhishek181-commits/wanderwise-travel-planner.git
   cd wanderwise-travel-planner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Create `.streamlit/secrets.toml` with your API keys:
   ```toml
   amadeus_api_key = "your_amadeus_key_here"
   openweathermap_api_key = "your_openweathermap_key_here"
   aviation_api_key = "your_aviationstack_key_here"
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

## 🔑 API Keys Required

### Amadeus API (Flight Search) - FREE ✅
- Sign up at: https://www.amadeus.com/en/development
- Free tier includes flight search capabilities
- Get your API key from the dashboard
- Documentation: https://developers.amadeus.com/api-catalog

### OpenWeatherMap API (Weather) - FREE ✅
- Sign up at: https://openweathermap.org/api
- Free tier provides current weather and 5-day forecasts
- API key available immediately after registration
- 1,000 requests/day free limit

### AviationStack API (Optional)
- Sign up at: https://aviationstack.com
- Real-time flight data (optional enhancement)

## 📁 Project Structure

```
wanderwise-travel-planner/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # API keys (not committed)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── SETUP.md              # Setup guide
├── manifest.json         # PWA manifest
└── config/
    └── config.py         # Configuration constants
```

## 🛠️ Code Structure

### Key Functions

#### API Integration
- `get_api_keys()` - Securely retrieve API keys from Streamlit secrets
- `fetch_flights()` - Get real flight data from Amadeus API with caching
- `fetch_weather()` - Retrieve weather forecast for destination
- `get_mock_flights()` - Fallback mock data for testing

#### Travel Planning
- `generate_travel_plan()` - Create personalized itineraries
- `validate_inputs()` - Input validation before API calls
- `create_pdf_plan()` - Generate PDF travel documents

#### Security
- All API keys stored in `.streamlit/secrets.toml` (not in code)
- Input validation prevents injection attacks
- Error handling with user-friendly messages

## 🔒 Security Best Practices

✅ **Implemented:**
- API keys in `secrets.toml` (never committed to git)
- Input validation for all user inputs
- Error handling without exposing sensitive data
- HTTPS-only API calls
- Session-based user state management
- Graceful fallbacks for API failures

✅ **Never:**
- Hardcode API keys in source code
- Expose keys in error messages
- Log sensitive user data
- Accept unsanitized user input

## ⚡ Caching Strategy

- **Flights**: Cached for 1 hour (`@st.cache_data(ttl=3600)`)
- **Weather**: Cached for 30 minutes (`@st.cache_data(ttl=1800)`)
- Reduces API calls and improves performance
- Caches automatically clear after TTL

## 🎨 UI/UX Features

- Responsive layout with sidebar for easy navigation
- Color-coded sections (flights, hotels, budget)
- Progress spinners during API calls
- Download buttons for PDF export
- Saved plans persistent in session
- Emoji-rich interface for better UX
- Mobile-friendly responsive design

## 🐛 Error Handling

The app gracefully handles:
- Missing/invalid API keys → Falls back to mock data
- API timeouts → User-friendly error message
- Network errors → Retry logic with fallbacks
- Invalid inputs → Input validation before processing
- HTTP errors → Specific error messages

## 🚀 Future Enhancements

- [ ] User database for persistent plan storage
- [ ] Real-time price comparison across multiple APIs
- [ ] Google Maps integration for route planning
- [ ] Multi-language support (Hindi, Spanish, etc.)
- [ ] Expense tracking during trip
- [ ] Integration with payment gateways
- [ ] Mobile app version
- [ ] Social sharing of travel plans
- [ ] Email notifications for flight deals
- [ ] Travel insurance recommendations

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check SETUP.md for troubleshooting
- Contact: chandraabhishek181@gmail.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) - Amazing web framework
- [Amadeus](https://amadeus.com) - Flight data API
- [OpenWeatherMap](https://openweathermap.org) - Weather API
- [ReportLab](https://www.reportlab.com) - PDF generation library
- [Python Requests](https://requests.readthedocs.io) - HTTP library

---

**Made with ❤️ by WanderWise Team**

Give us a ⭐ if you find this helpful!
