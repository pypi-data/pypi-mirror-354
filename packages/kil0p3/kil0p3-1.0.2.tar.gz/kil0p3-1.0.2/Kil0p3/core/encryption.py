#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Encryption Module
========================

Криптографические функции для защиты данных
"""

import os
import base64
import hashlib
import secrets
from typing import Optional, Tuple, Union
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from ..config.constants import RSA_KEY_SIZE, AES_KEY_SIZE, SALT_SIZE, IV_SIZE
from ..tools.logger import get_logger

logger = get_logger(__name__)

class CryptographyManager:
    """Менеджер криптографических операций"""
    
    def __init__(self):
        self.backend = default_backend()
        self._rsa_private_key = None
        self._rsa_public_key = None
    
    def generate_rsa_keypair(self) -> Tuple[bytes, bytes]:
        """
        Генерация RSA ключевой пары
        
        Returns:
            Tuple[bytes, bytes]: (private_key_pem, public_key_pem)
        """
        try:
            logger.debug("Generating RSA keypair...")
            
            # Генерация приватного ключа
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=RSA_KEY_SIZE,
                backend=self.backend
            )
            
            # Сериализация приватного ключа
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Получение публичного ключа
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            self._rsa_private_key = private_key
            self._rsa_public_key = public_key
            
            logger.info("RSA keypair generated successfully")
            return private_pem, public_pem
            
        except Exception as e:
            logger.error(f"RSA keypair generation failed: {e}")
            raise
    
    def load_rsa_public_key(self, public_key_pem: Union[str, bytes]) -> bool:
        """
        Загрузка RSA публичного ключа
        
        Args:
            public_key_pem: PEM формат публичного ключа
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            if isinstance(public_key_pem, str):
                public_key_pem = public_key_pem.encode('utf-8')
            
            self._rsa_public_key = serialization.load_pem_public_key(
                public_key_pem,
                backend=self.backend
            )
            
            logger.debug("RSA public key loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load RSA public key: {e}")
            return False
    
    def rsa_sign(self, data: bytes, private_key_pem: bytes) -> bytes:
        """
        RSA подпись данных
        
        Args:
            data: Данные для подписи
            private_key_pem: Приватный ключ в PEM формате
            
        Returns:
            bytes: Цифровая подпись
        """
        try:
            # Загрузка приватного ключа
            private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None,
                backend=self.backend
            )
            
            # Создание подписи
            signature = private_key.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.debug("RSA signature created")
            return signature
            
        except Exception as e:
            logger.error(f"RSA signing failed: {e}")
            raise
    
    def rsa_verify(self, data: bytes, signature: bytes, public_key_pem: Optional[bytes] = None) -> bool:
        """
        Проверка RSA подписи
        
        Args:
            data: Оригинальные данные
            signature: Подпись для проверки
            public_key_pem: Публичный ключ (опционально, если не загружен ранее)
            
        Returns:
            bool: True если подпись валидна
        """
        try:
            # Загрузка публичного ключа если необходимо
            if public_key_pem:
                public_key = serialization.load_pem_public_key(
                    public_key_pem,
                    backend=self.backend
                )
            elif self._rsa_public_key:
                public_key = self._rsa_public_key
            else:
                raise ValueError("No public key available")
            
            # Проверка подписи
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.debug("RSA signature verified successfully")
            return True
            
        except Exception as e:
            logger.debug(f"RSA signature verification failed: {e}")
            return False
    
    def aes_encrypt(self, data: bytes, password: str, salt: Optional[bytes] = None) -> bytes:
        """
        AES шифрование с паролем
        
        Args:
            data: Данные для шифрования
            password: Пароль
            salt: Соль (опционально, будет сгенерирована)
            
        Returns:
            bytes: Зашифрованные данные (salt + iv + encrypted_data)
        """
        try:
            # Генерация соли если не передана
            if salt is None:
                salt = os.urandom(SALT_SIZE)
            
            # Генерация ключа из пароля
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=AES_KEY_SIZE // 8,
                salt=salt,
                iterations=100000,
                backend=self.backend
            )
            key = kdf.derive(password.encode('utf-8'))
            
            # Генерация IV
            iv = os.urandom(IV_SIZE)
            
            # Шифрование
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            
            # Padding для AES
            padded_data = self._add_padding(data)
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            # Возвращаем salt + iv + encrypted_data
            result = salt + iv + encrypted_data
            
            logger.debug("AES encryption completed")
            return result
            
        except Exception as e:
            logger.error(f"AES encryption failed: {e}")
            raise
    
    def aes_decrypt(self, encrypted_data: bytes, password: str) -> bytes:
        """
        AES расшифровка с паролем
        
        Args:
            encrypted_data: Зашифрованные данные (salt + iv + data)
            password: Пароль
            
        Returns:
            bytes: Расшифрованные данные
        """
        try:
            # Извлечение компонентов
            salt = encrypted_data[:SALT_SIZE]
            iv = encrypted_data[SALT_SIZE:SALT_SIZE + IV_SIZE]
            ciphertext = encrypted_data[SALT_SIZE + IV_SIZE:]
            
            # Восстановление ключа
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=AES_KEY_SIZE // 8,
                salt=salt,
                iterations=100000,
                backend=self.backend
            )
            key = kdf.derive(password.encode('utf-8'))
            
            # Расшифровка
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            data = self._remove_padding(padded_data)
            
            logger.debug("AES decryption completed")
            return data
            
        except Exception as e:
            logger.error(f"AES decryption failed: {e}")
            raise
    
    def _add_padding(self, data: bytes) -> bytes:
        """Добавление PKCS7 padding"""
        block_size = 16  # AES block size
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _remove_padding(self, padded_data: bytes) -> bytes:
        """Удаление PKCS7 padding"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def generate_secure_random(self, length: int) -> bytes:
        """
        Генерация криптографически стойкого случайного числа
        
        Args:
            length: Длина в байтах
            
        Returns:
            bytes: Случайные данные
        """
        return secrets.token_bytes(length)
    
    def hash_sha256(self, data: bytes) -> str:
        """
        SHA256 хеширование
        
        Args:
            data: Данные для хеширования
            
        Returns:
            str: Hex представление хеша
        """
        return hashlib.sha256(data).hexdigest()
    
    def hash_sha512(self, data: bytes) -> str:
        """
        SHA512 хеширование
        
        Args:
            data: Данные для хеширования
            
        Returns:
            str: Hex представление хеша
        """
        return hashlib.sha512(data).hexdigest()
    
    def encode_base64(self, data: bytes) -> str:
        """Base64 кодирование"""
        return base64.b64encode(data).decode('utf-8')
    
    def decode_base64(self, encoded_data: str) -> bytes:
        """Base64 декодирование"""
        return base64.b64decode(encoded_data.encode('utf-8'))

# Глобальный экземпляр криптографического менеджера
crypto_manager = CryptographyManager()

# Удобные функции для быстрого использования
def encrypt_string(plaintext: str, password: str) -> str:
    """
    Шифрование строки с паролем
    
    Args:
        plaintext: Исходная строка
        password: Пароль для шифрования
        
    Returns:
        str: Base64 зашифрованная строка
    """
    encrypted_bytes = crypto_manager.aes_encrypt(plaintext.encode('utf-8'), password)
    return crypto_manager.encode_base64(encrypted_bytes)

def decrypt_string(encrypted_b64: str, password: str) -> str:
    """
    Расшифровка строки с паролем
    
    Args:
        encrypted_b64: Base64 зашифрованная строка
        password: Пароль для расшифровки
        
    Returns:
        str: Расшифрованная строка
    """
    encrypted_bytes = crypto_manager.decode_base64(encrypted_b64)
    decrypted_bytes = crypto_manager.aes_decrypt(encrypted_bytes, password)
    return decrypted_bytes.decode('utf-8')

def sign_data(data: str, private_key_pem: bytes) -> str:
    """
    Подпись строковых данных
    
    Args:
        data: Данные для подписи
        private_key_pem: Приватный ключ
        
    Returns:
        str: Base64 подпись
    """
    signature = crypto_manager.rsa_sign(data.encode('utf-8'), private_key_pem)
    return crypto_manager.encode_base64(signature)

def verify_signature(data: str, signature_b64: str, public_key_pem: bytes) -> bool:
    """
    Проверка подписи строковых данных
    
    Args:
        data: Оригинальные данные
        signature_b64: Base64 подпись
        public_key_pem: Публичный ключ
        
    Returns:
        bool: True если подпись валидна
    """
    signature = crypto_manager.decode_base64(signature_b64)
    return crypto_manager.rsa_verify(data.encode('utf-8'), signature, public_key_pem)