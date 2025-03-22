from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
from apify_client import ApifyClient
from typing import Dict, Any, List

app = FastAPI()

ALLOWED_IP = "10.214.209.4"
@app.middleware("http")
async def check_ip_address(request: Request, call_next):
    client_ip = request.client.host
    is_production  = os.getenv("PRODUCTION", "false") == "true"

    if is_production and client_ip != ALLOWED_IP:
        raise HTTPException(status_code=403, detail="Forbidden: Access denied")

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