import pymongo
from bson.objectid import ObjectId
from datetime import datetime


class DataBase:

    def __init__(self):
        """
        Esta função init faz a conexão com banco de dados e gera a collection
        """
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny."
                                            "mongodb.net/myFirstDatabase?retryWrites=true&w=majority", 
                                            ssl=True, ssl_cert_reqs='CERT_NONE')
            self.db = self.conn["database_teste"]
            self.users = self.db["users"]
        except:
            raise Exception("Failed to connect with the TestDataBase, check your string connection!!")

    def create_user(self, user_values: dict):
        """
        Essa função cria o usuário no banco de dados,
        Recebe um dicionário com as informações, as colunas created_at
        e updated_at são geradas automaticamente através do datetime.today
        A função retorna uma tupla com id do usuário criado e um código status quo.
        :param user_values:
        :return:
        """
        todays_date = datetime.today()
        user_values['created_at'] = todays_date
        user_values['uploaded_at'] = todays_date

        try:
            user_added = self.users.insert_one(user_values).inserted_id
            return str(user_added), 200
        except:
            return "Error: Could not create user", 400

    def get_user_by_email(self, email):
        """
        Esta função procura o usuário por e-mail informado,
        recebe um e-mail e retorna uma tupla com o usuário e o status quo, caso não encontrado,
        retorna uma mensagem relatando o mesmo.
        :param email:
        :return:
        """
        try:
            response = self.users.find_one({"email": email})
            if response:
                response["_id"] = str(response["_id"])
                return response, 200
            return f"The following email: {email} does not exist", 400
        except:
            return "Error: Could not get_user_by_email() in database", 400

    def get_user_by_id(self, id):
        """
        Esta função procura o usuário por id informado,
        recebe um id e retorna o usuário e o status quo, caso não encontrado,
        retorna uma mensagem relatando o mesmo.
        :param email:
        :return:
        """
        try:
            response = self.users.find_one({"_id": id})
            #, {"password": 0}
            if response:
                response["_id"] = str(response["_id"])
                return response, 200
            return f"The informed id: {id}, does not exist! Try again!", 400
        except:
            return "Error: Could not get_user_by_id() in database", 400

    def update_user_by_id(self, id, new_values):
        """
        Esta função atualiuza o usuário,
        recebe um id e um dicionário com os valores a serem atualizados
        retorna o usuário e o status quo, caso não encontrado,
        retorna uma mensagem relatando o mesmo.
        :param email:
        :return:
        """
        try:
            new_values['updated_at'] = datetime.today()
            response = self.users.update_one({"_id": id}, {"$set": new_values}).modified_count
            if response:
                return f"Id: {id} was updated with success!", 200
            return f"Error: Id {id} does not exist, try again!", 400
        except:
            return "Error: Could not update_user_by_id()", 400

    def delete_user_by_id(self, id):
        """
        Esta função deleta o usuário, o achando pelo id informado.
        retorna mensagem de erro caso nao encontrado o id.
        :param id:
        :return:
        """
        try:
            response = self.users.delete_one({"_id": id}).deleted_count
            if response:
                return f"Deleted with success id: {id}", 200
            return f"Error: Id {id} does not exist, try again!", 400
        except:
            return "Error: Could not delete_user_by_id() in database", 400

    def id_creation(self, id):
        """
        Esta função trasnforma um id string em um ObjectId
        retorna o ObjectId
        :param id:
        :return:
        """
        try:
            return ObjectId(id)
        except:
            return f"Id is not valid, review your id: {id} and try again!", 400
