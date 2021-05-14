import pymongo
from bson.objectid import ObjectId
from datetime import datetime

print(datetime)
class DataBase:

    def __init__(self):
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny."
                                            "mongodb.net/myFirstDatabase?retryWrites=true&w=majority", 
                                            ssl=True, ssl_cert_reqs='CERT_NONE')
            self.db = self.conn["database_teste"]
            self.users = self.db["users"]
        except:
            raise Exception("Failed to connect with the TestDataBase, check your string connection!!")

    def create_user(self, user_values: dict):
        todays_date = datetime.today()
        user_values['created_at'] = todays_date
        user_values['uploaded_at'] = todays_date
        # print(self.db)
        try:
            user_added = self.db.users.insert_one(user_values).inserted_id
            return str(user_added), 200
        except:
            return "Error: Could not create user", 400

    def get_user_by_email(self, email):
        try:
            response = self.db.users.find_one({"email": email})
            if response:
                response["_id"] = str(response["_id"])
                return response, 200
            return f"The following email: {email} does not exist", 400
        except:
            return "Error: Could not get_user_by_email() in database", 400

    def get_user_by_id(self, id):
        try:
            response = self.db.users.find_one({"_id": id})
            #, {"password": 0}
            if response:
                response["_id"] = str(response["_id"])
                return response, 200
            return f"The informed id: {id}, does not exist! Try again!", 400
        except:
            return "Error: Could not get_user_by_id() in database", 400

    def update_user_by_id(self, id, new_values):
        try:
            new_values['updated_at'] = datetime.today()
            response = self.db.users.update_one({"_id": id}, {"$set": new_values}).modified_count
            if response:
                return f"Id: {id} was updated with success!", 200
            return f"Error: Id {id} does not exist, try again!", 400
        except:
            return "Error: Could not update_user_by_id()", 400

    def delete_user_by_id(self, id):
        try:
            response = self.db.users.delete_one({"_id": id}).deleted_count
            if response:
                return f"Deleted with success id: {id}", 200
            return f"Error: Id {id} does not exist, try again!", 400
        except:
            return "Error: Could not delete_user_by_id() in database", 400

    def id_creation(self, id):
        try:
            return ObjectId(id)
        except:
            return f"Id is not valid, review your id: {id} and try again!", 400
