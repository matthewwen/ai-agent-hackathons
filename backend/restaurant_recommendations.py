import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables from .env file if it exists
load_dotenv()

# Configure the Gemini API with your API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

def get_restaurant_recommendations(analysis: str) -> List[Dict[str, str]]:
    """
    Generate restaurant recommendations based on customer profile analysis.
    
    Args:
        analysis: String containing the customer profile analysis
        
    Returns:
        List of restaurant recommendations as dictionaries with name, location, and description
    """
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Prepare prompt for Gemini
    prompt = f"""Given I have a customer with this profile-   "analysis": "{analysis}",
Generate a list of best restaurant recommendations. Please output this as JSON with this schema- {{restaurant_name : string, restaurant_location  : string, restaurant_description : string }}[]. Generate this JSON array and this JSON only."""
    
    try:
        # Generate content using Gemini
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Sometimes the response might include markdown code blocks, so we need to extract the JSON
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_str = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            json_str = response_text[json_start:json_end].strip()
        else:
            json_str = response_text.strip()
        
        # Parse the JSON string into a Python object
        recommendations = json.loads(json_str)
        return recommendations
    except Exception as e:
        error_msg = f"Error generating restaurant recommendations: {str(e)}"
        print(error_msg)
        return []

def test_with_analysis_file(analysis_file: str = "analysis_output.json", save_to_file: bool = False, output_file: str = "restaurant_recommendations.json") -> List[Dict[str, str]]:
    """
    Test the restaurant recommendations function with analysis from a file
    
    Args:
        analysis_file: Path to the analysis JSON file
        save_to_file: Whether to save the output to a JSON file
        output_file: Path to the output JSON file
        
    Returns:
        List of restaurant recommendations
    """
    try:
        with open(analysis_file, "r") as f:
            data = json.load(f)
        
        analysis = data.get("analysis", "")
        recommendations = get_restaurant_recommendations(analysis)
        
        # Save to JSON file if requested
        if save_to_file and recommendations:
            from datetime import datetime
            
            # Create a dictionary with the recommendations and metadata
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "recommendations": recommendations,
                "analysis_file": analysis_file
            }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
                print(f"Recommendations saved to {output_file}")
        
        # Print recommendations for testing
        print(json.dumps(recommendations, indent=2))
        
        return recommendations
    except Exception as e:
        error_msg = f"Error testing with analysis file: {str(e)}"
        print(error_msg)
        
        # Save error to JSON file if requested
        if save_to_file:
            from datetime import datetime
            
            # Create a dictionary with the error message
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "error": error_msg,
                "analysis_file": analysis_file
            }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
                print(f"Error saved to {output_file}")
        
        return []

if __name__ == "__main__":
    test_with_analysis_file()
