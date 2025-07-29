#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 License Manager
=====================

Управление лицензиями и их валидация
"""

import os
import json
import re
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from ..config.constants import *
from ..tools.logger import get_logger
from ..core.encryption import crypto_manager
from ..core.hwid import hwid_generator

logger = get_logger(__name__)

@dataclass
class LicenseInfo:
    """Информация о лицензии"""
    key: str
    hwid: str
    ip_address: str
    issued_date: datetime
    expiry_date: datetime
    license_type: str  # 'trial', 'standard', 'premium', 'enterprise'
    max_activations: int
    current_activations: int
    is_revoked: bool
    signature: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        data = asdict(self)
        data['issued_date'] = self.issued_date.isoformat()
        data['expiry_date'] = self.expiry_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LicenseInfo':
        """Создание из словаря"""
        data['issued_date'] = datetime.fromisoformat(data['issued_date'])
        data['expiry_date'] = datetime.fromisoformat(data['expiry_date'])
        return cls(**data)
    
    def is_expired(self) -> bool:
        """Проверка истечения срока действия"""
        return datetime.now() > self.expiry_date
    
    def days_remaining(self) -> int:
        """Количество дней до истечения"""
        delta = self.expiry_date - datetime.now()
        return max(0, delta.days)

class LicenseManager:
    """Менеджер лицензий"""
    
    def __init__(self):
        self.license_file = LICENSE_FILE
        self.config_file = CONFIG_FILE
        self._current_license: Optional[LicenseInfo] = None
        
        # Создаем директории если не существуют
        self.license_file.parent.mkdir(exist_ok=True)
    
    def validate_license_key(self, license_key: str) -> bool:
        """
        Проверка формата лицензионного ключа
        
        Args:
            license_key: Лицензионный ключ
            
        Returns:
            bool: True если формат корректен
        """
        try:
            # Проверка формата
            if not re.match(LICENSE_PATTERN, license_key):
                logger.warning(f"Invalid license key format: {license_key}")
                return False
            
            # Проверка длины
            if len(license_key) != LICENSE_LENGTH:
                logger.warning(f"Invalid license key length: {len(license_key)}")
                return False
            
            logger.debug("License key format validation passed")
            return True
            
        except Exception as e:
            logger.error(f"License key validation error: {e}")
            return False
    
    def generate_license_key(self) -> str:
        """
        Генерация нового лицензионного ключа
        
        Returns:
            str: Новый лицензионный ключ
        """
        try:
            # Генерируем 4 блока по 4 символа
            blocks = []
            for _ in range(4):
                block = ""
                for _ in range(4):
                    # Используем только буквы и цифры (без 0, O, I, 1 для избежания путаницы)
                    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
                    block += chars[crypto_manager.generate_secure_random(1)[0] % len(chars)]
                blocks.append(block)
            
            license_key = f"{LICENSE_PREFIX}-{'-'.join(blocks)}"
            
            logger.info(f"Generated license key: {license_key}")
            return license_key
            
        except Exception as e:
            logger.error(f"License key generation failed: {e}")
            raise
    
    def create_license(self, license_key: str, license_type: str = "standard", 
                      validity_days: int = 365, max_activations: int = 1) -> LicenseInfo:
        """
        Создание новой лицензии
        
        Args:
            license_key: Лицензионный ключ
            license_type: Тип лицензии
            validity_days: Срок действия в днях
            max_activations: Максимальное количество активаций
            
        Returns:
            LicenseInfo: Объект лицензии
        """
        try:
            if not self.validate_license_key(license_key):
                raise ValueError("Invalid license key format")
            
            # Получаем текущий HWID и IP
            current_hwid = hwid_generator.generate()
            current_ip = self._get_current_ip()
            
            # Создаем лицензию
            license_info = LicenseInfo(
                key=license_key,
                hwid=current_hwid,
                ip_address=current_ip,
                issued_date=datetime.now(),
                expiry_date=datetime.now() + timedelta(days=validity_days),
                license_type=license_type,
                max_activations=max_activations,
                current_activations=1,
                is_revoked=False,
                signature=""
            )
            
            # Создаем подпись лицензии
            license_info.signature = self._sign_license(license_info)
            
            logger.info(f"License created: {license_key} ({license_type}, {validity_days} days)")
            return license_info
            
        except Exception as e:
            logger.error(f"License creation failed: {e}")
            raise
    
    def save_license(self, license_key: str, license_info: Optional[LicenseInfo] = None) -> bool:
        """
        Сохранение лицензии в локальный файл
        
        Args:
            license_key: Лицензионный ключ
            license_info: Информация о лицензии (опционально)
            
        Returns:
            bool: True если сохранение успешно
        """
        try:
            if license_info is None:
                # Если информация не передана, создаем базовую лицензию
                license_info = self.create_license(license_key)
            
            # Шифруем данные лицензии
            license_data = license_info.to_dict()
            encrypted_data = crypto_manager.aes_encrypt(
                json.dumps(license_data).encode('utf-8'),
                self._get_encryption_key()
            )
            
            # Сохраняем в файл
            with open(self.license_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Устанавливаем права доступа (только чтение для владельца)
            os.chmod(self.license_file, 0o600)
            
            self._current_license = license_info
            logger.info("License saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"License save failed: {e}")
            return False
    
    def load_license(self) -> Optional[LicenseInfo]:
        """
        Загрузка лицензии из локального файла
        
        Returns:
            Optional[LicenseInfo]: Лицензия или None если не найдена
        """
        try:
            if not self.license_file.exists():
                logger.debug("License file not found")
                return None
            
            # Читаем зашифрованные данные
            with open(self.license_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Расшифровываем
            decrypted_data = crypto_manager.aes_decrypt(
                encrypted_data,
                self._get_encryption_key()
            )
            
            # Парсим JSON
            license_data = json.loads(decrypted_data.decode('utf-8'))
            
            # Создаем объект лицензии
            license_info = LicenseInfo.from_dict(license_data)
            
            self._current_license = license_info
            logger.info(f"License loaded: {license_info.key}")
            return license_info
            
        except Exception as e:
            logger.error(f"License load failed: {e}")
            return None
    
    def validate_license(self, license_info: Optional[LicenseInfo] = None) -> Tuple[bool, str]:
        """
        Полная валидация лицензии
        
        Args:
            license_info: Лицензия для проверки (по умолчанию текущая)
            
        Returns:
            Tuple[bool, str]: (результат, сообщение об ошибке)
        """
        try:
            if license_info is None:
                license_info = self.load_license()
            
            if license_info is None:
                return False, "No license found"
            
            # 1. Проверка формата ключа
            if not self.validate_license_key(license_info.key):
                return False, "Invalid license key format"
            
            # 2. Проверка подписи
            if not self._verify_license_signature(license_info):
                return False, "Invalid license signature"
            
            # 3. Проверка срока действия
            if license_info.is_expired():
                return False, "License expired"
            
            # 4. Проверка отзыва
            if license_info.is_revoked:
                return False, "License revoked"
            
            # 5. Проверка HWID
            current_hwid = hwid_generator.generate()
            if license_info.hwid != current_hwid:
                return False, "Hardware ID mismatch"
            
            # 6. Проверка IP (если включена)
            if SECURITY_SETTINGS.get('enable_ip_check', False):
                current_ip = self._get_current_ip()
                if license_info.ip_address != current_ip:
                    return False, "IP address mismatch"
            
            # 7. Проверка времени системы
            if not self._verify_system_time(license_info):
                return False, "System time manipulation detected"
            
            logger.info("License validation successful")
            return True, "Valid"
            
        except Exception as e:
            logger.error(f"License validation error: {e}")
            return False, f"Validation error: {e}"
    
    def delete_license(self) -> bool:
        """
        Удаление лицензии
        
        Returns:
            bool: True если удаление успешно
        """
        try:
            if self.license_file.exists():
                os.remove(self.license_file)
                logger.info("License deleted")
            
            self._current_license = None
            return True
            
        except Exception as e:
            logger.error(f"License deletion failed: {e}")
            return False
    
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """
        Получение информации о текущей лицензии
        
        Returns:
            Optional[Dict]: Информация о лицензии
        """
        try:
            license_info = self.load_license()
            if not license_info:
                return None
            
            return {
                'key': license_info.key[-8:] + '...',  # Показываем только последние символы
                'type': license_info.license_type,
                'expires': license_info.expiry_date.strftime('%Y-%m-%d'),
                'days_remaining': license_info.days_remaining(),
                'is_expired': license_info.is_expired(),
                'is_revoked': license_info.is_revoked,
                'hwid': license_info.hwid[:8] + '...',
                'activations': f"{license_info.current_activations}/{license_info.max_activations}"
            }
            
        except Exception as e:
            logger.error(f"Error getting license info: {e}")
            return None
    
    def _sign_license(self, license_info: LicenseInfo) -> str:
        """Создание цифровой подписи лицензии"""
        try:
            # Создаем строку для подписи
            sign_data = f"{license_info.key}|{license_info.hwid}|{license_info.expiry_date.isoformat()}"
            
            # В реальном проекте здесь должен быть серверный приватный ключ
            # Для демонстрации используем заглушку
            signature = crypto_manager.hash_sha256(sign_data.encode('utf-8'))
            
            return signature
            
        except Exception as e:
            logger.error(f"License signing failed: {e}")
            return ""
    
    def _verify_license_signature(self, license_info: LicenseInfo) -> bool:
        """Проверка цифровой подписи лицензии"""
        try:
            # Пересоздаем строку для проверки
            sign_data = f"{license_info.key}|{license_info.hwid}|{license_info.expiry_date.isoformat()}"
            
            # Проверяем подпись
            expected_signature = crypto_manager.hash_sha256(sign_data.encode('utf-8'))
            
            return license_info.signature == expected_signature
            
        except Exception as e:
            logger.error(f"License signature verification failed: {e}")
            return False
    
    def _verify_system_time(self, license_info: LicenseInfo) -> bool:
        """Проверка манипуляций со временем"""
        try:
            # Проверка на откат времени
            current_time = datetime.now()
            
            # Если текущее время меньше времени выдачи лицензии - возможен откат
            if current_time < license_info.issued_date:
                logger.warning("System time is before license issue date")
                return False
            
            # Дополнительные проверки времени можно добавить здесь
            
            return True
            
        except Exception as e:
            logger.error(f"System time verification failed: {e}")
            return False
    
    def _get_encryption_key(self) -> str:
        """Получение ключа шифрования для локального хранения"""
        # Используем HWID как часть ключа
        hwid = hwid_generator.generate()
        key_material = f"Kil0p3_{hwid}_{VERSION}"
        return crypto_manager.hash_sha256(key_material.encode('utf-8'))[:32]
    
    def _get_current_ip(self) -> str:
        """Получение текущего IP адреса"""
        try:
            import requests
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text.strip()
        except:
            return "unknown"

# Глобальный экземпляр менеджера лицензий
license_manager = LicenseManager()

def validate_current_license() -> Tuple[bool, str]:
    """
    Быстрая проверка текущей лицензии
    
    Returns:
        Tuple[bool, str]: (результат, сообщение)
    """
    return license_manager.validate_license()

def get_current_license_info() -> Optional[Dict[str, Any]]:
    """
    Получение информации о текущей лицензии
    
    Returns:
        Optional[Dict]: Информация о лицензии
    """
    return license_manager.get_license_info()

def activate_license(license_key: str) -> bool:
    """
    Активация лицензии
    
    Args:
        license_key: Лицензионный ключ
        
    Returns:
        bool: True если активация успешна
    """
    try:
        if not license_manager.validate_license_key(license_key):
            return False
        
        # Создаем и сохраняем лицензию
        license_info = license_manager.create_license(license_key)
        return license_manager.save_license(license_key, license_info)
        
    except Exception as e:
        logger.error(f"License activation failed: {e}")
        return False