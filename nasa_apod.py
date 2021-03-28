import requests
import os


params = {

    'api_key': str(os.getenv('NASA_API'))

}


def get_apod():
    print(params)
    resp = requests.get(url='https://api.nasa.gov/planetary/apod', params=params)
    resp = (resp.json())
    print(resp)
    return {'title': resp['title'], 'url': resp['url'], 'explanation': resp['explanation']}