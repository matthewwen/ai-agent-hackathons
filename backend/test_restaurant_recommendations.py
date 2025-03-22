import json
from restaurant_recommendations import get_restaurant_recommendations, test_with_analysis_file

def main():
    print("Testing restaurant recommendations...")
    
    # Test with analysis file
    print("\nTesting with analysis file:")
    recommendations = test_with_analysis_file("analysis_output.json")
    
    # Display the results
    if recommendations:
        print(f"\nFound {len(recommendations)} restaurant recommendations")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec.get('restaurant_name')} ({rec.get('restaurant_location')})")
            print(f"   {rec.get('restaurant_description')}")
    else:
        print("No recommendations found or an error occurred.")

if __name__ == "__main__":
    main()
