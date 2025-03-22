from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
from apify_client import ApifyClient
from typing import Dict, Any, List
from instagram_analysis import analyze_instagram_posts

app = FastAPI()

ALLOWED_IP = "10.214.209.4"
@app.middleware("http")
async def check_ip_address(request: Request, call_next):
    client_ip = request.client.host
    is_production  = os.getenv("PRODUCTION", "false") == "true"
    print(client_ip, is_production)

    #if is_production and client_ip != ALLOWED_IP:
        #raise HTTPException(status_code=403, detail="Forbidden: Access denied")

    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    # Hardcoded test to display Instagram data for kyliejenner
    return get_instagram_data("kyliejenner")

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/instagram/{username}")
def get_instagram_data(username: str):
    """
    Retrieve Instagram data for a given username using Apify API.
    
    Args:
        username: Instagram username to fetch data for
        
    Returns:
        JSON response with Instagram profile data
    """
    try:
        # Initialize the ApifyClient with API token
        client = ApifyClient("apify_api_NijTGDp3Pvbbd0dydzaDP9g4O78tnG3EHHSN")
        
        # Prepare the Actor input
        run_input = {
            "directUrls": [f"https://www.instagram.com/{username}"],
            "resultsType": "posts",
            "resultsLimit": 5,
            "searchType": "hashtag",
            "searchLimit": 1,
            "addParentData": False,
        }
        
        # Run the Actor and wait for it to finish
        run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)
        
        # Fetch Actor results from the run's dataset
        results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        return {"username": username, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Instagram data: {str(e)}")


@app.get("/instagram/{username}/analysis")
def analyze_instagram_user(username: str):
    """
    Analyze Instagram user posts using Gemini Vision API.
    
    Args:
        username: Instagram username to analyze
        
    Returns:
        JSON response with analysis results
    """
    try:
        # First get the Instagram data
        instagram_data = get_instagram_data(username)
        
        # Analyze the posts using Gemini
        analysis_result = analyze_instagram_posts(instagram_data)
        
        return {
            "username": username,
            "analysis": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing Instagram data: {str(e)}")


@app.post("/instagram/analyze-test-data")
def analyze_test_data(output_file: str = "analysis_output.json"):
    """
    Analyze test Instagram data from ig_test_data.json using Gemini Vision API.
    
    Args:
        output_file: Path to save the analysis output as JSON
    
    Returns:
        JSON response with analysis results
    """
    try:
        import json
        
        # Load test data
        with open("ig_test_data.json", "r") as f:
            test_data = json.load(f)
        
        # Analyze the posts using Gemini and save to file
        analysis_result = analyze_instagram_posts(test_data, save_to_file=True, output_file=output_file)
        
        return {
            "analysis": analysis_result,
            "output_file": output_file
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing test data: {str(e)}")