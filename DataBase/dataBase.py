import json

import pymongo
from bson.objectid import ObjectId
import pandas as pd
from datetime import datetime
pd.set_option("display.max_columns", None)

class DataBase:

    def __init__(self):
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny."
                                            "mongodb.net/myFirstDatabase?retryWrites=true&w=majority", 
                                            ssl=True, ssl_cert_reqs='CERT_NONE')
            self.db = self.conn["database_teste"]
            self.users = self.db["users"]
        except:
            raise Exception("Falha ao conectar ao banco de dados!")

    def create_user(self, user_values: dict):
        todays_date = datetime.today()
        user_values['created_at'] = todays_date
        user_values['uploaded_at'] = todays_date
        try:
            user_added = self.db.users.insert_one(user_values).inserted_id
        except:
            return "Error: Could not create user", 400
        return str(user_added), 200

    def get_all_users(self):
        try:
            response = pd.DataFrame(self.db.users.find())
        except:
            return "Error: Could not get_all_users() in database", 400
        return str(response), 200

    def get_user_by_email(self, email):
        try:
            response = self.db.users.find_one({"email": email})
        except:
            return "Error: Could not get_user_by_email() in database", 400
        if response:
            response["_id"] = str(response["_id"])
        return response, 200

    def get_user_by_id(self, id):
        try:
            response = self.db.users.find_one({"_id": id})
        except:
            return "Error: Could not get_user_by_id() in database", 400
        if response:
            response["_id"] = str(response["_id"])
        return response, 200

    def id_creation(self, id):
        return ObjectId(id)
