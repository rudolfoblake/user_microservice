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

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_get_user_by_email(self, mock_databse_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):
            mock_databse_users.find_one.return_value = dict()

    def test_get_user_by_id(self):
        pass

    def test_update_user_by_id(self):
        pass

    def test_delete_user_by_id(self):
        pass

    def test_id_creation(self):
        pass