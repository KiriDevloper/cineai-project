from pymongo import MongoClient

from config import Config

client = MongoClient(Config.MONGO_URI)

db = client["movie_ai"]

users_collection = db["users"]

reviews_collection = db["reviews"]