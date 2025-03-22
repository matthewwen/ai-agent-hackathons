import google.generativeai as genai
import base64
import requests
import io
from PIL import Image
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configure the Gemini API with your API key
# You should set this in an environment variable for security
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

def download_image(url: str) -> bytes:
    """
    Download an image from a URL and return it as bytes.
    
    Args:
        url: URL of the image to download
        
    Returns:
        Image as bytes
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")
        return None

def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string.
    
    Args:
        image_bytes: Image as bytes
        
    Returns:
        Base64 encoded string
    """
    if not image_bytes:
        return None
    return base64.b64encode(image_bytes).decode('utf-8')

def analyze_instagram_posts(user_data: Dict[str, Any], save_to_file: bool = False, output_file: str = "analysis_output.json") -> str:
    """
    Analyze Instagram posts using Gemini Vision API.
    
    Args:
        user_data: Instagram user data containing posts
        save_to_file: Whether to save the output to a JSON file
        output_file: Path to the output JSON file
        
    Returns:
        Analysis results from Gemini
    """
    # Initialize Gemini model for multimodal input
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Extract posts from user data
    posts = user_data.get("data", []) if isinstance(user_data, dict) else user_data
    
    if not posts or len(posts) == 0:
        return "No posts found in the provided data."
    
    # Prepare content parts for Gemini
    content_parts = [
        "Assume I am a business. I want to gain detailed insights about this potential customer (Instagram user) based on their latest post images and corresponding captions. Please examine these post images and captions and return relevant insights about this customer."
    ]
    
    # Add post information to content parts
    for i, post in enumerate(posts[:5]):  # Limit to 5 posts to be mindful of context
        # Get display URL and caption
        display_url = post.get("displayUrl")
        caption = post.get("caption", "")
        
        if display_url:
            # Download and encode image
            image_bytes = download_image(display_url)
            if image_bytes:
                # Add image to content parts
                content_parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": encode_image_to_base64(image_bytes)
                    }
                })
                
                # Add caption information
                content_parts.append(f"Post {i+1} Caption: {caption}")
    
    # If no images were successfully processed
    if len(content_parts) <= 1:
        return "Could not process any images from the provided posts."
    
    try:
        # Generate content using Gemini
        response = model.generate_content(content_parts)
        result = response.text
        
        # Save to JSON file if requested
        if save_to_file:
            import json
            from datetime import datetime
            
            # Create a dictionary with the analysis result and metadata
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "analysis": result,
                "post_count": min(len(posts), 5)  # Number of posts analyzed
            }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
                print(f"Analysis saved to {output_file}")
        
        return result
    except Exception as e:
        error_msg = f"Error analyzing posts with Gemini: {str(e)}"
        
        # Save error to JSON file if requested
        if save_to_file:
            import json
            from datetime import datetime
            
            # Create a dictionary with the error message
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "error": error_msg
            }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
                print(f"Error saved to {output_file}")
        
        return error_msg

def test_with_sample_data(save_to_file: bool = True, output_file: str = "analysis_output.json"):
    """
    Test the analysis function with sample data from ig_test_data.json
    
    Args:
        save_to_file: Whether to save the output to a JSON file
        output_file: Path to the output JSON file
    """
    import json
    
    try:
        with open("ig_test_data.json", "r") as f:
            sample_data = json.load(f)
        
        result = analyze_instagram_posts(sample_data, save_to_file=save_to_file, output_file=output_file)
        print(result)
        return result
    except Exception as e:
        print(f"Error testing with sample data: {str(e)}")
        return None

if __name__ == "__main__":
    test_with_sample_data()
