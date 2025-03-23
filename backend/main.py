from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from apify_client import ApifyClient
from typing import Dict, Any, List
from instagram_analysis import analyze_instagram_posts
from restaurant_recommendations import get_restaurant_recommendations
import google.generativeai as genai

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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


@app.get("/instagram/{username}/restaurant-recommendations")
def get_restaurant_recommendations_for_user(username: str):
    """
    Generate restaurant recommendations based on Instagram user analysis.
    
    Args:
        username: Instagram username to analyze
        
    Returns:
        JSON response with restaurant recommendations
    """
    try:
        # First get the Instagram analysis
        analysis_response = analyze_instagram_user(username)
        analysis = analysis_response.get("analysis", "")
        
        # Generate restaurant recommendations based on the analysis
        recommendations = get_restaurant_recommendations(analysis)
        
        return {
            "username": username,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating restaurant recommendations: {str(e)}")


@app.post("/restaurant-recommendations")
def get_recommendations_from_analysis(analysis: str):
    """
    Generate restaurant recommendations based on provided customer profile analysis.
    
    Args:
        analysis: Customer profile analysis string
        
    Returns:
        JSON response with restaurant recommendations
    """
    try:
        # Generate restaurant recommendations based on the analysis
        recommendations = get_restaurant_recommendations(analysis)
        
        return {
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating restaurant recommendations: {str(e)}")


@app.post("/restaurant-recommendations/from-file")
def get_recommendations_from_file(analysis_file: str = "analysis_output.json"):
    """
    Generate restaurant recommendations based on analysis from a file.
    
    Args:
        analysis_file: Path to the analysis JSON file
        
    Returns:
        JSON response with restaurant recommendations
    """
    try:
        import json
        
        # Load analysis from file
        with open(analysis_file, "r") as f:
            data = json.load(f)
        
        analysis = data.get("analysis", "")
        
        # Generate restaurant recommendations based on the analysis
        recommendations = get_restaurant_recommendations(analysis)
        
        return {
            "recommendations": recommendations,
            "analysis_file": analysis_file
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating restaurant recommendations from file: {str(e)}")


@app.get("/instagram/{username}/full-service")
def full_service_recommendations(username: str, save_outputs: bool = True, output_dir: str = "outputs"):
    """
    Complete service that fetches Instagram data, analyzes it, and generates restaurant recommendations.
    All in one endpoint that connects all services.
    
    Args:
        username: Instagram username to analyze
        save_outputs: Whether to save intermediate and final outputs to files
        output_dir: Directory to save output files
        
    Returns:
        JSON response with restaurant recommendations and paths to output files
    """
    try:
        # Import here to avoid circular imports
        from instagram_restaurant_service import get_recommendations_from_instagram
        
        # Use the integrated service to get recommendations
        recommendations, output_files = get_recommendations_from_instagram(
            username=username,
            save_outputs=save_outputs,
            output_dir=output_dir
        )
        
        return {
            "username": username,
            "recommendations": recommendations,
            "output_files": output_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in full service recommendations: {str(e)}")


@app.post("/rewrite")
async def rewrite_prompt(data: Dict[str, Any]):
    """
    Generate a new prompt based on user feedback on recommendations.
    
    Args:
        data: JSON data containing username, recommendations with preferences, and output files
        
    Returns:
        JSON response with the new prompt
    """
    try:
        # Configure Gemini API
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Get the current prompt used for analysis
        current_prompt = "Assume I am a business. I want to gain detailed insights about this potential customer (Instagram user) based on their latest post images and corresponding captions. Please examine these post images and captions and return relevant insights about this customer."
        
        # Load the analysis data if available
        analysis_data = ""
        if "output_files" in data and "analysis" in data["output_files"]:
            try:
                import json
                analysis_file = data["output_files"]["analysis"]
                print(f"Attempting to load analysis file: {analysis_file}")
                
                # Check if file exists
                if os.path.exists(analysis_file):
                    with open(analysis_file, "r") as f:
                        analysis_json = json.load(f)
                        analysis_data = analysis_json.get("analysis", "")
                else:
                    print(f"Analysis file does not exist: {analysis_file}")
            except Exception as e:
                print(f"Error loading analysis file: {str(e)}")
        
        # Format the recommendations with preferences for the prompt
        recommendations_with_preferences = []
        
        # Log the data structure for debugging
        print(f"Data structure received: {data.keys()}")
        if "recommendations" in data:
            print(f"Found {len(data['recommendations'])} recommendations")
        
        for rec in data.get("recommendations", []):
            print(f"Processing recommendation: {rec}")
            if "preference" in rec:
                rec_with_pref = {
                    "restaurant_name": rec.get("restaurant_name", ""),
                    "restaurant_location": rec.get("restaurant_location", ""),
                    "restaurant_description": rec.get("restaurant_description", ""),
                    "correct": rec.get("preference") == "like"
                }
                recommendations_with_preferences.append(rec_with_pref)
        
        # Create the input for Gemini
        # If we don't have any recommendations with preferences, use a sample for testing
        if not recommendations_with_preferences:
            print("No recommendations with preferences found, using sample data")
            recommendations_with_preferences = [
                {
                    "restaurant_name": "Sample Restaurant 1",
                    "restaurant_location": "Sample Location 1",
                    "restaurant_description": "Sample description 1",
                    "correct": True
                },
                {
                    "restaurant_name": "Sample Restaurant 2",
                    "restaurant_location": "Sample Location 2",
                    "restaurant_description": "Sample description 2",
                    "correct": False
                }
            ]
        
        input_text = f"""
        Assume I have this recommended customer data and a list of recommendations that have been validated to be either a correct or incorrect recommendation (see correct property for each)-
        {{
          username: '{data.get("username", "")}',
          recommendations: {recommendations_with_preferences}
        }}

        In order to generate these recommendations, I used the prompt-  \"{current_prompt}\". 

        Which generated this customer profile-
        {{
          \"analysis\": \"{analysis_data}\"
        }}.

        Please generate a new prompt that takes into account the recommendation validations that I were provided in the recommendations data, the current prompt, and the customer profile. Generate this prompt string and this prompt string only.
        """
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate the new prompt
        response = model.generate_content(input_text)
        new_prompt = response.text.strip()
        
        return {
            "current_prompt": current_prompt,
            "response": new_prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rewriting prompt: {str(e)}")