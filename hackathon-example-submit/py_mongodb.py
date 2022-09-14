from http import client
from config import *
from pymongo import MongoClient
import pymongo

def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://cyouisme:{PASS_MDB}@review-analytics.w9y5hbz.mongodb.net/test"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['review-analytics']

def insert_db(collection_name, data):
    ins = reviews.insert_one(data)
    
# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":    
    
# Get the database
dbname = get_database()
reviews = dbname["reviews"]
