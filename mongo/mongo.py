from pymongo import MongoClient

# client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.quic_simulator
manager_collection = db.manager
tracker_collection = db.tracker
