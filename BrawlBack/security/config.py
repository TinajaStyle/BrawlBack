from decouple import config

json = config("BRAWL_API_TOKEN")
url = config("BRAWL_API_URL")

header = {
    "Authorization" : f"Bearer {json}",
    "Content-Type": "application/json"
}