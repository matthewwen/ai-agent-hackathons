import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from apify_client import ApifyClient

# Import services
from instagram_analysis import analyze_instagram_posts
from restaurant_recommendations import get_restaurant_recommendations

def get_instagram_data(username: str) -> Dict[str, Any]:
    """
    Retrieve Instagram data for a given username using Apify API.
    This is a copy of the function from main.py to avoid circular imports.
    
    Args:
        username: Instagram username to fetch data for
        
    Returns:
        Dictionary with Instagram profile data
    """
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


def get_recommendations_from_instagram(
    username: str, 
    save_outputs: bool = True,
    output_dir: str = "outputs"
) -> Tuple[List[Dict[str, str]], Dict[str, str]]:
    """
    Main function that connects all services to get restaurant recommendations
    based on Instagram user analysis.
    
    Args:
        username: Instagram username to analyze
        save_outputs: Whether to save intermediate and final outputs to files
        output_dir: Directory to save output files
        
    Returns:
        Tuple containing:
        - List of restaurant recommendations
        - Dictionary with paths to all generated output files
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_files = {}
    
    # Create output directory if it doesn't exist and save_outputs is True
    if save_outputs:
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Get Instagram data
        print(f"Fetching Instagram data for user: {username}")
        instagram_data = get_instagram_data(username)
        
        if save_outputs:
            instagram_data_file = f"{output_dir}/{username}_instagram_data_{timestamp}.json"
            with open(instagram_data_file, 'w', encoding='utf-8') as f:
                json.dump(instagram_data, f, indent=2)
            output_files["instagram_data"] = instagram_data_file
            print(f"Instagram data saved to {instagram_data_file}")
        
        # Step 2: Analyze Instagram posts
        print(f"Analyzing Instagram posts for user: {username}")
        analysis_result = analyze_instagram_posts(instagram_data)
        
        if save_outputs:
            analysis_file = f"{output_dir}/{username}_analysis_{timestamp}.json"
            analysis_data = {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "analysis": analysis_result
            }
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2)
            output_files["analysis"] = analysis_file
            print(f"Analysis saved to {analysis_file}")
        
        # Step 3: Generate restaurant recommendations
        print(f"Generating restaurant recommendations based on analysis")
        recommendations = get_restaurant_recommendations(analysis_result)
        
        if save_outputs:
            recommendations_file = f"{output_dir}/{username}_recommendations_{timestamp}.json"
            recommendations_data = {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "recommendations": recommendations
            }
            with open(recommendations_file, 'w', encoding='utf-8') as f:
                json.dump(recommendations_data, f, indent=2)
            output_files["recommendations"] = recommendations_file
            print(f"Recommendations saved to {recommendations_file}")
        
        return recommendations, output_files
    
    except Exception as e:
        error_msg = f"Error in get_recommendations_from_instagram: {str(e)}"
        print(error_msg)
        
        if save_outputs:
            error_file = f"{output_dir}/{username}_error_{timestamp}.json"
            error_data = {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "error": error_msg
            }
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_data, f, indent=2)
            output_files["error"] = error_file
            print(f"Error saved to {error_file}")
        
        return [], output_files

def main():
    """
    Main entry point for the Instagram Restaurant Recommendation service.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Get restaurant recommendations based on Instagram profile analysis')
    parser.add_argument('username', type=str, help='Instagram username to analyze')
    parser.add_argument('--no-save', action='store_true', help='Do not save output files')
    parser.add_argument('--output-dir', type=str, default='outputs', help='Directory to save output files')
    
    args = parser.parse_args()
    
    recommendations, output_files = get_recommendations_from_instagram(
        username=args.username,
        save_outputs=not args.no_save,
        output_dir=args.output_dir
    )
    
    if recommendations:
        print("\nRestaurant Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec.get('restaurant_name')} ({rec.get('restaurant_location')})")
            print(f"   {rec.get('restaurant_description')}")
    else:
        print("\nNo recommendations were generated.")
    
    if output_files and not args.no_save:
        print("\nOutput files:")
        for key, path in output_files.items():
            print(f"{key}: {path}")

if __name__ == "__main__":
    main()
