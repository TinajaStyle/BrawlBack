import requests
from decouple import config

token = config("TEST_TOKEN") 
endpoint = config("API_URL") + "track/"
tag = ""

def test_start_track():
    full_url = f"{endpoint}start_track/{tag}"
    response = requests.post(url=full_url, headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 201 or response.status_code == 204 #in case there are no battles to show

def test_get_all_tracked():
    full_url = f"{endpoint}get_all_tracked"
    response = requests.get(url=full_url, headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_delete_track():
    full_url = f"{endpoint}delete_track/{tag}"
    response = requests.delete(url=full_url, headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 204