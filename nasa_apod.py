import requests
import os
from dotenv import load_dotenv # Don't forget this import

load_dotenv()

api_key = os.getenv('NASA_API')

if not api_key:
    print("Warning: NASA_API environment variable not set. APOD command will not work.")
    def get_apod():
        return {'title': 'Error: NASA API Key Missing', 'url': '', 'explanation': 'Please set the NASA_API environment variable.'}
else:
    params = {
        'api_key': api_key
    }

    def get_apod():
        try:
            resp = requests.get(url='https://api.nasa.gov/planetary/apod', params=params)
            resp.raise_for_status()
            resp = resp.json()
            return {'title': resp['title'], 'url': resp['url'], 'explanation': resp['explanation']}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching NASA APOD: {e}")
            return {'title': 'Error', 'url': '', 'explanation': 'Failed to fetch the Astronomy Picture of the Day.'}
        except (KeyError) as e:
            print(f"Error parsing NASA APOD response: {e}")
            return {'title': 'Error', 'url': '', 'explanation': 'Failed to parse the API response from NASA.'}

if __name__ == "__main__":
    print("--- Testing NASA APOD function ---")
    apod_data = get_apod()

    print("\nTitle:", apod_data['title'])
    print("URL:", apod_data['url'])
    print("Explanation:", apod_data['explanation'])
    print("\n--- Test complete ---")
