from unittest import mock, TestCase
from DataBase.dataBase import DataBase

# db = dataBase.DataBase


class TestDataBase(TestCase):

    def test_init(self):
        pass

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_create_user(self, mock_database_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):

            mock_database_users.insert_one.return_value.inserted_id = "123"

            self.assertEqual(DataBase().create_user({}), ("123", 200))


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