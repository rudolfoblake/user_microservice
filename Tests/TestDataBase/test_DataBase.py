from unittest import mock, TestCase
from DataBase import dataBase

db = dataBase.DataBase()


class TestDataBase(TestCase):

    def test_init(self):
        pass

    @mock.patch('DataBase.dataBase.datetime')
    @mock.patch('DataBase.dataBase.DataBase')
    def test_create_user(self, mock_database_users, mock_datetime):
        mock_datetime.today.return_value = "AAAA"
        mock_database_users.db.users.insert_one.return_value = "mock.Mock()"
        # mock_database_users.users.insert_one.inserted_id = "123"
        user_dict = dict()

        self.assertEqual(db.create_user(user_dict), ("123", 200))
        # delattr(mock_users, "insert_one")


    # def create_user(self, user_values: dict):
    #     todays_date = datetime.today()
    #     user_values['created_at'] = todays_date
    #     user_values['uploaded_at'] = todays_date
    #     try:
    #         user_added = self.db.users.insert_one(user_values).inserted_id
    #         return str(user_added), 200
    #     except:
    #         return "Error: Could not create user", 400


    def test_get_user_by_email(self):
        pass

    def test_get_user_by_id(self):
        pass

    def test_update_user_by_id(self):
        pass

    def test_delete_user_by_id(self):
        pass

    def test_id_creation(self):
        pass