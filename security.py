from cryptography.fernet import Fernet


class Security:
    def __init__(self):
        self.key = self.get_key()
        self.f = Fernet(self.key)

    def get_key(self):
        with open("info.txt", mode="rb") as file:
            data = file.readline()
        return data

    def encrypt(self, input_text):
        print(input_text)
        token = self.f.encrypt(input_text.encode())
        print(type(token))
        # self.decrypt(token)
        return token

    def decrypt(self, input_text):
        input_text = bytes(input_text[1:].replace("b'", "")[:-1], 'utf-8')
        token = self.f.decrypt(input_text)
        print(token.decode())
        return token.decode('utf-8')


# test = Security()
#
# de = "'b'gAAAAABhSu5YjkzGjJRbm9F9fJNg0tfD4vzTrdwu7qZTxL7ZhEeaIOAHeVuGrnVsWIbec3I394nA2SbeiTYLSZehvzP_EEZQo9D7QWm1c7fheqYHMkDE0V8='" #[1:].replace("b'", "")[:-1]
# # print(bytes(de), 'utf-8')
# # print(de)
# print(test.decrypt(de))
# # test.decrypt(bytes(de, 'utf-8'))
# # test.encrypt("FFF")
#
# # print(f"'{test.encrypt('dict1')}")
