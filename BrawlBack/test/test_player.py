import requests
from decouple import config

token = config("TEST_TOKEN") 
endpoint = config("API_URL") + "player/"
player = ""
tag = ""

def test_profile():
    full_url = endpoint + tag
    response = requests.get(url=full_url, headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == player


def test_battlelog():
    full_url = f"{endpoint}battlelog/{tag}"
    response = requests.get(url=full_url, headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 200 or response.status_code == 204