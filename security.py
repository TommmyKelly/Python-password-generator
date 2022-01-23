from cryptography.fernet import Fernet


def get_key():
    with open("info.txt", mode="rb") as file:
        data = file.readline()
    return data


class Security:
    def __init__(self):
        self.key = get_key()
        self.f = Fernet(self.key)

    def encrypt(self, input_text):
        print(input_text)
        token = self.f.encrypt(input_text.encode())
        return token

    def decrypt(self, input_text):
        input_text = bytes(input_text[1:].replace("b'", "")[:-1], 'utf-8')
        token = self.f.decrypt(input_text)
        return token.decode('utf-8')
