import pymongo
from bson.objectid import ObjectId
import pandas as pd
from datetime import datetime
pd.set_option("display.max_columns", None)


class DataBase:

    def __init__(self):
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny."
                                            "mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            self.db = self.conn["database_teste"]
            self.users = self.db["users"]
        except:
            raise Exception("Failed to connect with the DataBase, check your string connection!!")

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
            if response:
                response["_id"] = str(response["_id"])
            if response == None:
                return f"The following email: {email} does not exist", 400
        except:
            return "Error: Could not get_user_by_email() in database", 400
        return response, 200

    def get_user_by_id(self, id):
        try:
            response = self.db.users.find_one({"_id": id})
            if response:
                response["_id"] = str(response["_id"])
            if response == None:
                return f"The informed id: {id}, does not exist! Try again!", 400
        except:
            return "Error: Could not get_user_by_id() in database", 400
        return response, 200

    def update_user_by_id(self, id, new_values):
        try:
            todays_date = datetime.today()
            new_values['updated_at'] = todays_date
            response = self.db.users.update_one({"_id": id}, {"$set": new_values}).modified_count
            if response > 0:
                return f"Id: {id} was updated with success!", 200
            if response == 0:
                return f"Error: No updated changes were made at id: {id}, try again!", 400
        except:
            return "Error: Could not update_user_by_id()", 400

    def delete_user_by_id(self, id):
        try:
            response = self.db.users.delete_one({"_id": id}).deleted_count
            if response > 0:
                return f"Deleted with success id: {id}", 200
            if response == 0:
                return f"Error: Id {id} does not exist, try again!", 400
        except:
            return "Error: Could not delete_user_by_id() in database", 400

    def id_creation(self, id):
        try:
            return ObjectId(id)
        except:
            return f"Id is not valid, review your id: {id} and try again!", 400
