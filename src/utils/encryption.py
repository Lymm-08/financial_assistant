# ==========================
# ARQUIVO: src/utils/encryption.py
# CRIPTOGRAFIA DE DADOS SENSIVEIS
# ==========================

from cryptography.fernet import Fernet
import base64
import hashlib

class Encryptor:
    def __init__(self, master_key):
        """Initialize encryptor with master key"""
        self.master_key = master_key
        # Derivar chave de 32 bytes usando SHA256
        key_hash = hashlib.sha256(master_key.encode()).digest()
        fernet_key = base64.urlsafe_b64encode(key_hash)
        self.cipher = Fernet(fernet_key)
    
    def encrypt(self, data):
        """Encrypt string data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()
    
    def decrypt(self, encrypted_data):
        """Decrypt data back to string"""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()

def encrypt_sensitive_data(data, key):
    """Helper function to encrypt data"""
    encryptor = Encryptor(key)
    return encryptor.encrypt(data)

def decrypt_sensitive_data(encrypted, key):
    """Helper function to decrypt data"""
    encryptor = Encryptor(key)
    return encryptor.decrypt(encrypted)
