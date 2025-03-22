# Instagram Analysis with Gemini Vision API

This service analyzes Instagram posts using Google's Gemini Vision API to provide insights about Instagram users based on their posts and captions.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Gemini API key:
   - Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a `.env` file in the backend directory based on `.env.example`
   - Add your Gemini API key to the `.env` file:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

## Usage

### Testing with Sample Data

To test the analysis with the sample data in `ig_test_data.json`:

```bash
cd backend
python instagram_analysis.py
```

Or use the FastAPI endpoint:

```bash
cd backend
uvicorn main:app --reload
```

Then make a POST request to `http://localhost:8000/instagram/analyze-test-data`

### Analyzing Real Instagram Users

To analyze a real Instagram user's posts, start the FastAPI server and make a GET request to:

```
http://localhost:8000/instagram/{username}/analysis
```

Replace `{username}` with the Instagram username you want to analyze.

## How It Works

1. The service fetches Instagram posts using the Apify API
2. It extracts images (from displayUrl) and captions from each post
3. Images are downloaded and encoded to base64
4. The images and captions are sent to Gemini Vision API with a prompt
5. Gemini analyzes the content and returns insights about the Instagram user

## API Endpoints

- `GET /instagram/{username}` - Get raw Instagram data for a username
- `GET /instagram/{username}/analysis` - Get Gemini analysis of Instagram posts
- `POST /instagram/analyze-test-data` - Test analysis with sample data from ig_test_data.json
