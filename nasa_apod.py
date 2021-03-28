import requests
import os


params = {

    'api_key': str(os.getenv('NASA_API'))

}


def get_apod():
    resp = requests.get(url='https://api.nasa.gov/planetary/apod', params=params)
    resp = (resp.json())
    return {'title': resp['title'], 'url': resp['url'], 'explanation': resp['explanation']}