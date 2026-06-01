# 🔧 WanderWise Setup Guide

## Step-by-Step Setup Instructions

### Step 1: Get Your API Keys

#### Amadeus API (Required for real flights)
1. Go to https://www.amadeus.com/en/development
2. Click "Register" or login if you have an account
3. Create a new app in the dashboard
4. Copy your **API Key** and **API Secret**
5. The test API uses `test.api.amadeus.com` (perfect for development)
6. Free tier: 2 requests/second, unlimited monthly calls

#### OpenWeatherMap API (Optional for weather)
1. Go to https://openweathermap.org/api
2. Click "Sign Up" and create an account
3. Go to "API Keys" tab
4. Copy your default API key
5. Free tier allows 1,000 calls/day
6. Activation takes a few minutes

### Step 2: Configure Local Environment

```bash
# Create the .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create secrets.toml file
cat > .streamlit/secrets.toml << EOF
amadeus_api_key = "your_amadeus_api_key_here"
openweathermap_api_key = "your_openweathermap_key_here"
aviertavion_api_key = "your_aviationstack_key_here_optional"
EOF
```

⚠️ **IMPORTANT**: Never commit `.streamlit/secrets.toml` to git!

### Step 3: Install & Run

```bash
# Clone repository
git clone https://github.com/chandraabhishek181-commits/wanderwise-travel-planner.git
cd wanderwise-travel-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Step 4: Test the Application

1. Open http://localhost:8501 in your browser
2. Login with any username (e.g., "Test User")
3. Fill in the form:
   - **Origin**: `DEL` (Delhi)
   - **Destination**: `BOM` (Mumbai)
   - **Trip Type**: Adventure
   - **Duration**: 7 days
   - **Budget**: Medium
   - **Start Date**: 30 days from today
4. Click "🚀 Generate Plan"
5. You should see real flight data from Amadeus!

## 🚀 Deployment Options

### Deploy to Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Login with GitHub
4. Click "New app"
5. Select your repository: `wanderwise-travel-planner`
6. Select app file: `app.py`
7. In app settings → Secrets, add:
   ```toml
   amadeus_api_key = "your_key_here"
   openweathermap_api_key = "your_key_here"
   ```
8. Deploy! 🎉

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Create Heroku app
heroku create wanderwise-planner

# Set environment variables
heroku config:set amadeus_api_key="your_key"
heroku config:set openweathermap_api_key="your_key"

# Deploy
git push heroku main
```

### Deploy to AWS Lambda

1. Use AWS Elastic Beanstalk
2. Configure environment variables in `.ebextensions/python.config`
3. Deploy using EB CLI

## 🔍 Troubleshooting

### Issue: "API key not configured"
**Solution**: 
- Make sure `.streamlit/secrets.toml` exists
- Check file is in correct location: `./`.streamlit/secrets.toml`
- Restart the Streamlit app after adding keys

### Issue: "Connection timeout"
**Solution**: 
- Check your internet connection
- Verify API rate limits haven't been exceeded
- Try again in a few moments

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: 
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### Issue: "Port 8501 is already in use"
**Solution**: 
```bash
streamlit run app.py --server.port 8502
```

### Issue: "Invalid API key"
**Solution**:
- Verify you copied the key correctly from the API dashboard
- For Amadeus, make sure you're using the **API Key** (not Client ID)
- Check that the key hasn't expired
- Generate a new key if needed

### Issue: "Weather data unavailable"
**Solution**:
- OpenWeatherMap API may take a few minutes to activate
- Wait 5-10 minutes after creating the API key
- Try again with a different city name
- Check your API rate limits (1,000/day free)

## 📊 Testing Tips

### Valid IATA Codes to Test
- **DEL** - Delhi (India)
- **BOM** - Mumbai (India)
- **BLR** - Bangalore (India)
- **NYC** - New York (USA)
- **LON** - London (UK)
- **DXB** - Dubai (UAE)

### Common Test Scenarios
1. **Short Trip**: 3 days, Low budget
2. **Weekend Getaway**: 2-3 days, Medium budget
3. **Vacation**: 7 days, Luxury budget
4. **Group Travel**: 10 people, Multiple activities

## 🔐 Security Checklist

- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] Never hardcoded API keys in `app.py`
- [ ] Verified API keys are valid
- [ ] Tested error handling (invalid inputs, API failures)
- [ ] Reviewed error messages (no sensitive data exposed)
- [ ] Checked that secrets aren't logged

## 📈 Performance Optimization

- Flight data is cached for 1 hour (reduces API calls)
- Weather data is cached for 30 minutes
- Use `st.cache_data` decorator for expensive operations
- Monitor API usage via dashboard

## 📚 Additional Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Amadeus API Docs](https://developers.amadeus.com/api-catalog)
- [OpenWeatherMap Docs](https://openweathermap.org/api)
- [Python Best Practices](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)
- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-cloud/get-started)

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages carefully
3. Check API documentation for rate limits
4. Open an issue on GitHub with:
   - Your Python version: `python --version`
   - Exact error message
   - Steps to reproduce
   - Your OS and browser
   - Streamlit version: `streamlit --version`

## 🎉 You're Ready!

Your WanderWise travel planner is now ready to use. Start planning amazing trips! ✈️🌍

---

**Happy travels! 🌍✈️🏖️**
