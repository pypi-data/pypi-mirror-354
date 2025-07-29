#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 - Advanced Python Application Protection Library
========================================================

АВТОМАТИЧЕСКАЯ ЗАЩИТА АКТИВИРУЕТСЯ ПРИ ИМПОРТЕ:

    import kil0p3

Библиотека обеспечивает:
- Лицензионную защиту с цифровыми подписями
- Привязку к оборудованию (HWID)
- Защиту от отладки и модификации
- Блокировку по IP и геолокации
- Анти-тампер механизмы
- Самоуничтожение при взломе

Copyright (c) 2025 Kil0p3 Security
"""

__version__ = "1.0.0"
__author__ = "Kil0p3 Security Team"
__license__ = "Proprietary"
__copyright__ = "Copyright (c) 2025 Kil0p3 Security"

import os
import sys
import threading
import time
from typing import Optional, Dict, Any

# Проверка минимальной версии Python
if sys.version_info < (3, 8):
    raise RuntimeError("Kil0p3 requires Python 3.8 or higher")

# Глобальные переменные
_protection_active = False
_license_key: Optional[str] = None
_validation_result = None
_initialization_complete = False

def get_version() -> str:
    """Получить версию библиотеки"""
    return __version__

def get_status() -> Dict[str, Any]:
    """Получить статус защиты"""
    global _protection_active, _validation_result, _license_key
    return {
        'version': __version__,
        'protection_active': _protection_active,
        'license_valid': _validation_result.is_valid if _validation_result else False,
        'license_key': _license_key[-8:] + '...' if _license_key else None,
        'dev_mode': os.getenv('KIL0P3_DEV_MODE', '0') == '1',
        'initialized': _initialization_complete
    }

def set_license(license_key: str) -> bool:
    """
    Установить лицензионный ключ программно
    
    Args:
        license_key: Лицензионный ключ в формате KLP-XXXX-XXXX-XXXX-XXXX
        
    Returns:
        bool: True если ключ валиден
    """
    global _license_key
    try:
        from .core.license import license_manager
        
        if license_manager.validate_license_key(license_key):
            _license_key = license_key
            license_manager.save_license(license_key)
            return True
        else:
            return False
            
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error setting license: {e}")
        return False

def check_license() -> bool:
    """Проверить валидность текущей лицензии"""
    try:
        from .core.validator import system_validator
        
        result = system_validator.validate_full()
        
        global _validation_result
        _validation_result = result
        
        return result.is_valid
        
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error checking license: {e}")
        return False

def get_hwid() -> str:
    """Получить Hardware ID текущего устройства"""
    try:
        from .core.hwid import hwid_generator
        return hwid_generator.generate()
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error getting HWID: {e}")
        return "ERROR"

def is_protected() -> bool:
    """Проверить активна ли защита"""
    return _protection_active

def _initialize_protection():
    """Инициализация защиты при импорте - ВСЕГДА выполняется"""
    global _protection_active, _initialization_complete
    
    try:
        # DEV режим - только для разработки
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print("🛠️ Kil0p3 DEV MODE - Protection disabled for development")
            _protection_active = False
            _initialization_complete = True
            return
        
        # Проверяем тестовую среду
        if any(test_indicator in sys.modules for test_indicator in ['pytest', 'unittest', 'nose']):
            print("🧪 Kil0p3: Test environment detected - Protection disabled")
            _protection_active = False
            _initialization_complete = True
            return
            
        # Проверяем интерактивную среду
        if hasattr(sys, 'ps1') or sys.flags.interactive:
            print("🐍 Kil0p3: Interactive environment detected - Protection in monitoring mode")
            _protection_active = True  # Включаем но не блокируем
            _initialization_complete = True
            return
        
        # ОСНОВНОЙ РЕЖИМ - полная защита
        print(f"🔐 Kil0p3 v{__version__} - Initializing protection...")
        
        def protection_init():
            """Инициализация в отдельном потоке"""
            global _protection_active, _initialization_complete
            
            try:
                from .run import auto_protect
                result = auto_protect()
                _protection_active = result
                _initialization_complete = True
                
                if result:
                    print("✅ Kil0p3: Protection activated successfully")
                else:
                    print("❌ Kil0p3: Protection activation failed")
                    if not os.getenv('KIL0P3_DEV_MODE'):
                        # В продакшене блокируем выполнение
                        print("🚫 Application terminating due to protection failure")
                        sys.exit(1)
                        
            except Exception as e:
                print(f"💥 Kil0p3: Protection initialization error: {e}")
                _protection_active = False
                _initialization_complete = True
                
                if not os.getenv('KIL0P3_DEV_MODE'):
                    sys.exit(1)
        
        # Запускаем инициализацию
        thread = threading.Thread(target=protection_init, daemon=False, name="Kil0p3Init")
        thread.start()
        
        # Ждем инициализацию максимум 15 секунд
        thread.join(timeout=15.0)
        
        if thread.is_alive():
            print("⏰ Kil0p3: Protection initialization timeout")
            if not os.getenv('KIL0P3_DEV_MODE'):
                sys.exit(1)
        
    except KeyboardInterrupt:
        print("⚠️ Kil0p3: Protection interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Kil0p3: Unexpected protection error: {e}")
        if not os.getenv('KIL0P3_DEV_MODE'):
            sys.exit(1)

# Экспортируемые функции
__all__ = [
    'get_version',
    'get_status', 
    'set_license',
    'check_license',
    'get_hwid',
    'is_protected',
    '__version__',
    '__author__'
]

# ============================================================================
# АВТОМАТИЧЕСКИЙ ЗАПУСК ЗАЩИТЫ ПРИ ИМПОРТЕ
# Это ключевая особенность - защита активируется сразу при import kil0p3
# ============================================================================

try:
    _initialize_protection()
except Exception as e:
    print(f"💥 Kil0p3: Fatal initialization error: {e}")
    if not os.getenv('KIL0P3_DEV_MODE'):
        sys.exit(1)

# Финальное сообщение
if os.getenv('KIL0P3_DEV_MODE') == '1':
    print(f"🛠️ Kil0p3 v{__version__} loaded in DEV MODE")
else:
    protection_status = "ACTIVE" if _protection_active else "INACTIVE"
    print(f"🔐 Kil0p3 v{__version__} - Protection {protection_status}")