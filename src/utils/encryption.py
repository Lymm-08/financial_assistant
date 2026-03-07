# ==========================
# ARQUIVO: src/utils/encryption.py
# SISTEMA DE CRIPTOGRAFIA PARA DADOS SENSÍVEIS
# ==========================

# ==========================
# IMPORTAÇÕES
# ==========================

from cryptography.fernet import Fernet
import base64
import hashlib

# ==========================
# CLASSE ENCRYPTOR
# ==========================

class Encryptor:
    """Classe para criptografia e descriptografia de dados usando Fernet"""

    def __init__(self, master_key):
        """Inicializa o encryptor com uma chave mestra

        Args:
            master_key: Chave mestra para derivar a chave de criptografia
        """
        self.master_key = master_key

        # SUBSEÇÃO: Derivar chave de 32 bytes usando SHA256
        key_hash = hashlib.sha256(master_key.encode()).digest()
        fernet_key = base64.urlsafe_b64encode(key_hash)
        self.cipher = Fernet(fernet_key)

    def encrypt(self, data):
        """Criptografa dados string

        Args:
            data: Dados a serem criptografados (string ou bytes)

        Returns:
            str: Dados criptografados em base64
        """
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()

    def decrypt(self, encrypted_data):
        """Descriptografa dados

        Args:
            encrypted_data: Dados criptografados (string ou bytes)

        Returns:
            str: Dados descriptografados
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()

# ==========================
# FUNÇÕES UTILITÁRIAS
# ==========================

# Nota: encrypt_sensitive_data e decrypt_sensitive_data foram removidas
# Podem ser re-adicionadas usando a classe Encryptor se necessário no futuro
