import pymongo


class DataBase:

    def __init__(self):
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny."
                                            "mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            self.db = self.conn["database_teste"]
            self.users = self.db["users"]
        except:
            raise Exception("Falha ao conectar ao banco de dados!")



    def create_user(self, user_date: dict):
        pass

    def get_all_users(self):
        pass

    def get_user_by_email(self):
        pass