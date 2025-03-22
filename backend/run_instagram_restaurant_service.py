#!/usr/bin/env python3
"""
Command-line interface for the Instagram Restaurant Recommendation service.
This script provides a simple way to run the full service from the terminal.
"""
import argparse
import json
from instagram_restaurant_service import get_recommendations_from_instagram

def main():
    """
    Main entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description='Get restaurant recommendations based on Instagram profile analysis'
    )
    parser.add_argument(
        'username', 
        type=str, 
        help='Instagram username to analyze'
    )
    parser.add_argument(
        '--no-save', 
        action='store_true', 
        help='Do not save output files'
    )
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='outputs', 
        help='Directory to save output files'
    )
    parser.add_argument(
        '--json-only', 
        action='store_true', 
        help='Output only the JSON result without pretty printing'
    )
    
    args = parser.parse_args()
    
    try:
        # Run the integrated service
        recommendations, output_files = get_recommendations_from_instagram(
            username=args.username,
            save_outputs=not args.no_save,
            output_dir=args.output_dir
        )
        
        if args.json_only:
            # Output only the JSON result
            result = {
                "username": args.username,
                "recommendations": recommendations,
                "output_files": output_files if not args.no_save else {}
            }
            print(json.dumps(result, indent=2))
        else:
            # Pretty print the results
            print(f"\nRestaurant Recommendations for Instagram user: @{args.username}")
            print("=" * 70)
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n{i}. {rec.get('restaurant_name')} ({rec.get('restaurant_location')})")
                    print(f"   {rec.get('restaurant_description')}")
            else:
                print("\nNo recommendations were generated.")
            
            if output_files and not args.no_save:
                print("\nOutput files:")
                for key, path in output_files.items():
                    print(f"{key}: {path}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
