from unittest import TestCase, mock

from Controllers import tokenController
tk = tokenController.Token()


class TestTokenController(TestCase):
    def test_save_token_works(self):
        token = {
                "token_id": "XjfWHiXtQltejTQpPXSp",
                "user_id": "UWfDaRdIdzhGaNeMTX9L",
                "expire": 14868846548.185464 #Validade de 15 minutos nos tokens
            }
        self.assertIsNone(tk.save_token(token))

    def test_delete_token_works(self):
        token = {
                "token_id": "XjfWHiXtQltejTQpPXSp",
                "user_id": "UWfDaRdIdzhGaNeMTX9L",
                "expire": 14868846548.185464 #Validade de 15 minutos nos tokens
            }
        tk.save_token(token)
        token_index = 0
        self.assertIsNone(tk.delete_token(token_index))

    def test_generate_token_works(self):
        user_id = "UWfDaRdIdzhGaNeMTX9L"
        self.assertEqual(tk.generate_token(user_id, "test")['user_id'], user_id)

    def test_verify_token_works(self):
        token = {
                "token_id": "tHpfvw9LVHq9R3rc05GF",
                "user_id": "UWfDaRdIdzhGaNeMTX9L",
                "expire": 14868846548.185464 #Validade de 15 minutos nos tokens
            }
        self.assertEqual(tk.verify_token(token['token_id']), )
        tk.save_token(token)
        self.assertEqual(tk.verify_token(token['token_id']), token['user_id'])