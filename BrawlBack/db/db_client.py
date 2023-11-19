import motor.motor_asyncio
import redis
from decouple import config

url = config("DB_URL")


client = motor.motor_asyncio.AsyncIOMotorClient(f"{url}&timeoutMS=20000",
                                                serverSelectionTimeoutMS=5000,
                                                socketTimeoutMS=1500)
db = client.app

users = db.users

tracked = db.tracked

battles = db.battles


r = redis.StrictRedis()