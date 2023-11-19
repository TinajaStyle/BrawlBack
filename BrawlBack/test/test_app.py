from urllib.parse import urlencode
from decouple import config
import requests

username = ""
password = ""
endpoint = config("API_URL") + "app/"

data={"username": username, "password":password}
encoded=urlencode(data)

def test_login():
    full_url = f"{endpoint}login"
    response = requests.post(url=full_url, data=encoded, 
                           headers={"content-type":"application/x-www-form-urlencoded"})
    assert response.status_code == 200