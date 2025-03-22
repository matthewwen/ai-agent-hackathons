#!/usr/bin/env python3
"""
Test script for the integrated Instagram restaurant recommendation service.
"""
from instagram_restaurant_service import get_recommendations_from_instagram

def test_service():
    """
    Test the integrated service with a sample Instagram username.
    """
    # You can change this to any Instagram username you want to test with
    test_username = "kyliejenner"
    
    print(f"Testing integrated service with username: {test_username}")
    print("-" * 50)
    
    # Call the integrated service
    recommendations, output_files = get_recommendations_from_instagram(
        username=test_username,
        save_outputs=True,
        output_dir="test_outputs"
    )
    
    # Display results
    if recommendations:
        print("\nRestaurant Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec.get('restaurant_name')} ({rec.get('restaurant_location')})")
            print(f"   {rec.get('restaurant_description')}")
    else:
        print("\nNo recommendations were generated.")
    
    if output_files:
        print("\nOutput files:")
        for key, path in output_files.items():
            print(f"{key}: {path}")

if __name__ == "__main__":
    test_service()
