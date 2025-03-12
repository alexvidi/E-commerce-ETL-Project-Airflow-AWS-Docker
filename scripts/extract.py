import requests
import json
import sys
import os

# Ensure the root directory is included in sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import configuration variables
from config.settings import FAKE_STORE_API, RAW_DATA_FILE

def extract_data():
    """
    Extracts product data from the Fake Store API and saves it as a JSON file.

    Returns:
        str: Path to the saved JSON file.
    
    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the response data is in an unexpected format.
        Exception: For any other unexpected errors during extraction.
    """
    try:
        print(f"Sending request to {FAKE_STORE_API}")
        response = requests.get(FAKE_STORE_API, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"Extraction successful: {len(data)} products retrieved")
        
        # Validate the response data format
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Unexpected data format or empty response")
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(RAW_DATA_FILE), exist_ok=True)

        # Save the extracted data to a JSON file
        with open(RAW_DATA_FILE, 'w') as f:
            json.dump(data, f)
        
        print(f"Data successfully saved to {RAW_DATA_FILE}")
        return RAW_DATA_FILE
    
    except requests.RequestException as e:
        print(f"API request error: {str(e)}")
        raise
    except Exception as e:
        print(f"Data validation error: {str(e)}")
        raise

if __name__ == "__main__":
    file_path = extract_data()
    print(f" File generated at: {file_path}")