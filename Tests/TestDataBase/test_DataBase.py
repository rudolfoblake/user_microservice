from unittest import mock, TestCase
from DataBase.dataBase import DataBase
from bson.objectid import ObjectId


class TestDataBase(TestCase):

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_create_user(self, mock_database_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):

            mock_database_users.insert_one.return_value.inserted_id = "123"
            self.assertEqual(DataBase().create_user({}), ("123", 201))

            mock_database_users.insert_one.return_value = ""
            self.assertEqual(DataBase().create_user({}),
                             ("Error: Could not create user", 400))

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_get_user_by_email(self, mock_database_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):

            mock_database_users.find_one.side_effect = [{"_id": 1}, {}, {"A":"A"}]

            self.assertEqual(DataBase().get_user_by_email("aki"),
                             ({"_id":"1"}, 200))
            self.assertEqual(DataBase().get_user_by_email("aki"),
                             ("The following email: aki does not exist", 404))
            self.assertEqual(DataBase().get_user_by_email("aki"),
                             ("Error: Could not get_user_by_email()", 400))

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_get_user_by_id(self, mock_database_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):
            mock_database_users.find_one.side_effect = [{"_id": 1}, {}, {"A":"A"}]

            self.assertEqual(DataBase().get_user_by_id("60a1444b370ea792caef5419"),
                             ({"_id": "1"}, 200))
            self.assertEqual(DataBase().get_user_by_id("60a1444b370ea792caef5419"),
                             ("The informed id: 60a1444b370ea792caef5419, does not exist! Try again!", 400))
            self.assertEqual(DataBase().get_user_by_id("60a1444b370ea792caef5419"),
                             ("Error: Could not get_user_by_id()", 400))

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_update_user_by_id(self, mock_database_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):
            mock_database_users.update_one.return_value.modified_count = 1

            self.assertEqual(DataBase().update_user_by_id("60a1444b370ea792caef5419", {}),
                             ("Id: 60a1444b370ea792caef5419 was updated with success!", 200))

            mock_database_users.update_one.return_value.modified_count = 0
            self.assertEqual(DataBase().update_user_by_id("60a1444b370ea792caef5419", {}),
                             ("Error: Id 60a1444b370ea792caef5419 does not exist, try again!", 400))

            mock_database_users.update_one.return_value = ""
            self.assertEqual(DataBase().update_user_by_id("60a1444b370ea792caef5419", {}),
                             ("Error: Could not update_user_by_id()", 400))

    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_delete_user_by_id(self, mock_database_users):
        with mock.patch.object(DataBase, "__init__", lambda x: None):

            mock_database_users.delete_one.return_value.deleted_count = 1
            self.assertEqual(DataBase().delete_user_by_id("60a1444b370ea792caef5419"),
                             ("Deleted with success id: 60a1444b370ea792caef5419", 200))

            mock_database_users.delete_one.return_value.deleted_count = 0
            self.assertEqual(DataBase().delete_user_by_id("60a1444b370ea792caef5419"),
                             ("Error: Id 60a1444b370ea792caef5419 does not exist, try again!", 400))

            mock_database_users.delete_one.return_value = ""
            self.assertEqual(DataBase().delete_user_by_id("60a1444b370ea792caef5419"),
                             ("Error: Could not delete_user_by_id()", 400))

    def test_id_creation(self):
        informed_id = "60a1444b370ea792caef5419"
        returned_id = ObjectId("60a1444b370ea792caef5419")
        self.assertEqual(DataBase().id_creation(informed_id), returned_id)

        informed_id = "123"
        self.assertEqual(DataBase().id_creation(informed_id),
                         ("Id is not valid, review your id: 123 and try again!", 400))


    @mock.patch("DataBase.dataBase.DataBase.convert_list_id_to_objectId")
    @mock.patch("DataBase.dataBase.DataBase.users", create=True)
    def test_find_users_by_id(self, mock_database_users, mock_list_id):
        with mock.patch.object(DataBase, "__init__", lambda x: None):
            mock_list_id.return_value = [ObjectId("60a69dcc01d6c1f3dbdedba0")]
            mock_database_users.find.return_value = ""

            self.assertEqual(DataBase().find_users_by_id([""]), {})


    def test_convert_list_id_to_objectId(self):
        self.assertEqual(DataBase().convert_list_id_to_objectId([]), [])
        self.assertEqual(DataBase().convert_list_id_to_objectId(["60a69d4a27d88a4efe20d19e"]), [ObjectId("60a69d4a27d88a4efe20d19e")])


