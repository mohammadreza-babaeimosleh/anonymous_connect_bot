from http import client
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.anonymous_bot
