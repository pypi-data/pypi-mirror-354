#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Constants
================

Основные константы и настройки безопасности
"""

import os
from pathlib import Path

# Версия и информация
VERSION = "1.0.0"
BUILD_NUMBER = "20250610"
PRODUCT_NAME = "Kil0p3 Protection"

# Криптографические константы
RSA_KEY_SIZE = 4096
AES_KEY_SIZE = 256
SALT_SIZE = 32
IV_SIZE = 16

# Форматы лицензий
LICENSE_PREFIX = "KLP"
LICENSE_PATTERN = r"^KLP-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$"
LICENSE_LENGTH = 23  # KLP-XXXX-XXXX-XXXX-XXXX

# Серверные настройки
DEFAULT_LICENSE_SERVER = "https://api.kil0p3.security"
API_VERSION = "v1"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# Пути к файлам
HOME_DIR = Path.home()
APP_DATA_DIR = HOME_DIR / ".kil0p3"
LICENSE_FILE = APP_DATA_DIR / "license.dat"
CONFIG_FILE = APP_DATA_DIR / "config.json"
LOG_FILE = APP_DATA_DIR / "protection.log"
ATTEMPT_FILE = APP_DATA_DIR / "attempts.dat"
BLOCK_FILE = APP_DATA_DIR / "blocked.dat"

# Создаем директории если не существуют
try:
    APP_DATA_DIR.mkdir(exist_ok=True)
except:
    pass

# Лимиты и ограничения
MAX_ACTIVATION_ATTEMPTS = 3
MAX_FAILED_VALIDATIONS = 5
ATTEMPT_RESET_HOURS = 24
BLOCK_DURATION_HOURS = 72

# HWID настройки
HWID_COMPONENTS = [
    'cpu_id',
    'motherboard_serial', 
    'disk_serial',
    'mac_address',
    'system_uuid'
]

# Настройки безопасности
SECURITY_SETTINGS = {
    'enable_anti_debug': True,
    'enable_vm_detection': True,
    'enable_integrity_check': True,
    'enable_time_check': True,
    'enable_network_validation': True,
    'enable_hwid_binding': True,
    'enable_self_delete': True,
    'enable_process_monitor': True
}

# Логирование
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Детекция среды выполнения
VM_ARTIFACTS = [
    'VMware',
    'VirtualBox', 
    'QEMU',
    'Xen',
    'Hyper-V',
    'KVM',
    'Parallels'
]

SANDBOX_ARTIFACTS = [
    'Cuckoo',
    'Anubis',
    'Joe Sandbox',
    'ThreatAnalyzer',
    'Falcon Sandbox'
]

# Debugging детекция
DEBUG_ARTIFACTS = [
    'pdb',
    'pydevd',
    'debugpy',
    'winpdb',
    'pudb'
]

# Защищенные процессы (не должны быть запущены)
FORBIDDEN_PROCESSES = [
    'ida.exe',
    'ida64.exe', 
    'x32dbg.exe',
    'x64dbg.exe',
    'ollydbg.exe',
    'wireshark.exe',
    'fiddler.exe',
    'processhacker.exe',
    'cheatengine.exe'
]

# Коды ошибок
ERROR_CODES = {
    'SUCCESS': 0,
    'LICENSE_INVALID': 1001,
    'LICENSE_EXPIRED': 1002,
    'LICENSE_REVOKED': 1003,
    'HWID_MISMATCH': 1004,
    'IP_BLOCKED': 1005,
    'TOO_MANY_ATTEMPTS': 1006,
    'TIME_MANIPULATION': 1007,
    'TAMPERING_DETECTED': 1008,
    'NETWORK_ERROR': 1009,
    'UNKNOWN_ERROR': 9999
}

# UI настройки
WINDOW_TITLE = "Kil0p3 Protection"
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 350
WINDOW_RESIZABLE = False

# Настройки по умолчанию
DEFAULT_CONFIG = {
    'license_server': DEFAULT_LICENSE_SERVER,
    'check_interval': 3600,
    'offline_grace_period': 86400,
    'ui_theme': 'modern',
    'language': 'en',
    'auto_update': True,
    'telemetry': True,
    'debug_mode': False
}

# Цветовая схема UI
COLORS = {
    'background': '#f0f0f0',
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'text': '#2c3e50'
}

# Ограничения времени
MAX_CLOCK_DRIFT_DAYS = 1

# IP ограничения (пустые по умолчанию - можно настроить)
ALLOWED_IP_RANGES = []
BLOCKED_COUNTRIES = []

# Дополнительные настройки безопасности
TAMPER_DETECTION_ENABLED = True
AUTO_BLOCK_ON_TAMPER = True
NETWORK_VALIDATION_TIMEOUT = 10

# Настройки окон
WINDOW_ALWAYS_ON_TOP = True
WINDOW_ICON_PATH = None