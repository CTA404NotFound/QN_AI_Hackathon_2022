""" Created by Cyouisme """
# 08/20/2022
# -*-encoding:utf-8-*-

from config import *
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
PASS_MDB = os.getenv('PASS')

def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://cyouisme:{PASS_MDB}@review-analytics.w9y5hbz.mongodb.net/test"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['review-analytics']

def insert_data(collection_name,data):
    if collection_name.find_one(data) == None:
        collection_name.insert_one(data)
    
def remove_data(collection_name,id):
    myquery = {"_id": ObjectId(id)}
    collection_name.delete_one(myquery)
   
# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":    
    
# Get the database
dbname = get_database()
reviews = dbname["reviews"]
wrong_reviews = dbname["wrong_reviews"]