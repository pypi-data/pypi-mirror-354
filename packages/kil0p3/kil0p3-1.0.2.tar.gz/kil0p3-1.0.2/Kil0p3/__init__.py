#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 - Advanced Python Application Protection Library
========================================================

АВТОМАТИЧЕСКАЯ ЗАЩИТА И ТРИАЛЬНЫЙ ПЕРИОД:

    import Kil0p3  # Запускает 30-секундный триал!

Библиотека обеспечивает:
- 30-секундный триальный период
- Лицензионную защиту с цифровыми подписями
- Привязку к оборудованию (HWID)
- Защиту от отладки и модификации

Copyright (c) 2025 Kil0p3 Security
"""

__version__ = "1.0.2"
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
_trial_active = False

def get_version() -> str:
    """Получить версию библиотеки"""
    return __version__

def get_status() -> Dict[str, Any]:
    """Получить статус защиты"""
    global _protection_active, _validation_result, _license_key, _trial_active
    
    status = {
        'version': __version__,
        'protection_active': _protection_active,
        'license_valid': _validation_result.is_valid if _validation_result else False,
        'license_key': _license_key[-8:] + '...' if _license_key else None,
        'dev_mode': os.getenv('KIL0P3_DEV_MODE', '0') == '1',
        'initialized': _initialization_complete,
        'trial_active': _trial_active
    }
    
    # Добавляем информацию о триале
    try:
        from .core.trial import trial_manager
        trial_info = trial_manager.get_trial_info()
        status['trial'] = trial_info
    except:
        status['trial'] = {'error': 'Trial manager not available'}
    
    return status

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

def is_trial_active() -> bool:
    """Проверить активен ли триальный период"""
    try:
        from .core.trial import trial_manager
        return not trial_manager.is_trial_expired()
    except:
        return False

def get_trial_time_remaining() -> float:
    """Получить оставшееся время триала в секундах"""
    try:
        from .core.trial import trial_manager
        return trial_manager.get_remaining_time()
    except:
        return 0.0

def get_trial_info() -> Dict[str, Any]:
    """Получить полную информацию о триале"""
    try:
        from .core.trial import trial_manager
        return trial_manager.get_trial_info()
    except Exception as e:
        return {'error': str(e)}

def check_trial_access() -> bool:
    """
    Проверить доступ в рамках триального периода
    Основная функция для использования в приложениях
    
    Returns:
        bool: True если доступ разрешен (есть лицензия или триал активен)
    """
    try:
        # В DEV режиме всегда разрешаем
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            return True
        
        # Проверяем лицензию
        if check_license():
            return True
        
        # Если нет лицензии - проверяем триал
        from .core.trial import trial_manager
        
        if trial_manager.check_continuous_usage():
            global _trial_active
            _trial_active = True
            return True
        else:
            _trial_active = False
            return False
            
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error checking trial access: {e}")
        return False

def show_trial_expired_message():
    """Показать сообщение об истечении триала"""
    try:
        from .ui.trial_expired_window import TrialExpiredWindow
        window = TrialExpiredWindow()
        window.show()
    except:
        # Fallback сообщение
        print("🔒 Триальный период истек!")
        print("💡 Для продолжения работы приобретите лицензию")

def _initialize_protection():
    """Инициализация защиты при импорте - ВСЕГДА выполняется"""
    global _protection_active, _initialization_complete, _trial_active
    
    try:
        # DEV режим - только для разработки
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print("🛠️ Kil0p3 DEV MODE - Protection disabled for development")
            _protection_active = False
            _trial_active = True  # В DEV режиме триал всегда активен
            _initialization_complete = True
            return
        
        print(f"🔐 Kil0p3 v{__version__} - Initializing protection with trial...")
        
        # Проверяем лицензию
        if check_license():
            print("✅ Valid license found - full access granted")
            _protection_active = True
            _trial_active = False
            _initialization_complete = True
            return
        
        # Если нет лицензии - запускаем триал
        from .core.trial import trial_manager
        
        if trial_manager.start_trial_session():
            remaining = trial_manager.get_remaining_time()
            print(f"🕐 Trial period active - {remaining:.1f} seconds remaining")
            _trial_active = True
            _protection_active = True
            _initialization_complete = True
        else:
            print("🔒 Trial period expired - access denied")
            _trial_active = False
            _protection_active = False
            _initialization_complete = True
            
            # Показываем сообщение о необходимости покупки
            show_trial_expired_message()
            
    except Exception as e:
        print(f"💥 Kil0p3: Protection initialization error: {e}")
        _protection_active = False
        _initialization_complete = True

# Экспортируемые функции
__all__ = [
    'get_version',
    'get_status', 
    'set_license',
    'check_license',
    'get_hwid',
    'is_protected',
    'is_trial_active',
    'get_trial_time_remaining',
    'get_trial_info',
    'check_trial_access',  # ← ГЛАВНАЯ ФУНКЦИЯ ДЛЯ ПРИЛОЖЕНИЙ
    '__version__',
    '__author__'
]

# ============================================================================
# АВТОМАТИЧЕСКИЙ ЗАПУСК ЗАЩИТЫ ПРИ ИМПОРТЕ
# Защита и триал активируются сразу при import Kil0p3
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
    status = "LICENSED" if check_license() else ("TRIAL" if _trial_active else "EXPIRED")
    print(f"🔐 Kil0p3 v{__version__} - Status: {status}")