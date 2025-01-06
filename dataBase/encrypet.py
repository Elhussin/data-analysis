from cryptography.fernet import Fernet, InvalidToken
import os 
class EncryptionManager:
    def __init__(self, key_file="secret.key"):
        
        self.key_file = os.path.join(os.path.dirname(__file__), key_file)
        # إذا كان الملف لا يحتوي على مفتاح، نقوم بتوليده
        try:
            self.key = self.load_key()
        except FileNotFoundError:
            self.key = self.generate_key()
            self.save_key(self.key)

    # توليد مفتاح جديد
    def generate_key(self):
        return Fernet.generate_key()

    # حفظ المفتاح في ملف
    def save_key(self, key):
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

    # تحميل المفتاح من الملف
    def load_key(self):
        return open(self.key_file, "rb").read()

    # تشفير كلمة المرور
    def encrypt_password(self, password):
        f = Fernet(self.key)
        encrypted_password = f.encrypt(password.encode())
        return encrypted_password

    # فك تشفير كلمة المرور
    def decrypt_password(self, encrypted_password):
        try:
            f = Fernet(self.key)
            decrypted_password = f.decrypt(encrypted_password).decode()
            return decrypted_password
        except InvalidToken:
            print("Error: Invalid key or corrupted data")
            return None


