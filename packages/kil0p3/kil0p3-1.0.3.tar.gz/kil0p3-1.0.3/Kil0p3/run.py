#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Protection Runner
=======================

Главная логика запуска и координации защиты
"""

import sys
import os
import time
import threading
from typing import Optional, Tuple, Dict, Any

from .config.constants import *
from .config.settings import Settings
from .tools.logger import get_logger
from .core.validator import SystemValidator, ValidationResult
from .security.anti_debug import AntiDebug
from .runtime.watchdog import ProtectionWatchdog
from .ui.auth_window import AuthWindow
from .ui.expired_window import ExpiredWindow  
from .ui.banned_window import BannedWindow

logger = get_logger(__name__)

class ProtectionManager:
    """Менеджер защиты - координирует все системы безопасности"""
    
    def __init__(self):
        self.settings = Settings()
        self.validator = SystemValidator()
        self.anti_debug = AntiDebug()
        self.watchdog = ProtectionWatchdog()
        self._protection_active = False
        self._last_validation = None
        
    def initialize(self) -> bool:
        """Инициализация системы защиты"""
        try:
            logger.info("Initializing Kil0p3 Protection System...")
            
            # Проверка базовой безопасности
            if not self._pre_flight_checks():
                logger.critical("Pre-flight security checks failed")
                return False
            
            # Запуск анти-отладки
            if SECURITY_SETTINGS['enable_anti_debug']:
                self.anti_debug.start_monitoring()
                logger.debug("Anti-debug monitoring started")
            
            # Запуск watchdog
            self.watchdog.start()
            logger.debug("Protection watchdog started")
            
            logger.info("Protection system initialized successfully")
            return True
            
        except Exception as e:
            logger.critical(f"Protection initialization failed: {e}")
            return False
    
    def _pre_flight_checks(self) -> bool:
        """Предварительные проверки безопасности"""
        try:
            # Проверка среды выполнения
            if SECURITY_SETTINGS['enable_vm_detection']:
                from .security.vm_detect import VMDetector
                vm_detector = VMDetector()
                if vm_detector.is_virtual_machine():
                    logger.warning("Virtual machine detected")
                    # В зависимости от политики можем блокировать или продолжить
            
            # Проверка отладчиков
            if self.anti_debug.is_debugger_present():
                logger.critical("Debugger detected!")
                self._handle_tampering("Debugger detected")
                return False
            
            # Проверка целостности
            if SECURITY_SETTINGS['enable_integrity_check']:
                from .core.tamper import TamperProtection
                tamper = TamperProtection()
                if not tamper.verify_integrity():
                    logger.critical("Code integrity violation!")
                    self._handle_tampering("Code integrity violation")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Pre-flight checks error: {e}")
            return False
    
    def validate_license(self) -> ValidationResult:
        """Основная проверка лицензии"""
        try:
            logger.debug("Starting license validation...")
            
            # Полная валидация через SystemValidator
            result = self.validator.validate_full()
            self._last_validation = result
            
            logger.info(f"Validation result: {'VALID' if result.is_valid else 'INVALID'}")
            if not result.is_valid:
                logger.warning(f"Validation failed: {result.error_message}")
            
            return result
            
        except Exception as e:
            logger.error(f"License validation error: {e}")
            return ValidationResult(
                is_valid=False,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=str(e)
            )
    
    def handle_validation_result(self, result: ValidationResult) -> bool:
        """Обработка результата валидации"""
        try:
            if result.is_valid:
                logger.info("License validation successful")
                return True
            
            # Обработка различных ошибок
            if result.error_code == ERROR_CODES['LICENSE_INVALID']:
                return self._show_activation_window()
                
            elif result.error_code == ERROR_CODES['LICENSE_EXPIRED']:
                return self._show_expired_window()
                
            elif result.error_code == ERROR_CODES['LICENSE_REVOKED']:
                return self._show_banned_window("License revoked")
                
            elif result.error_code == ERROR_CODES['TOO_MANY_ATTEMPTS']:
                return self._show_banned_window("Too many activation attempts")
                
            elif result.error_code == ERROR_CODES['TIME_MANIPULATION']:
                return self._show_banned_window("Time manipulation detected")
                
            elif result.error_code == ERROR_CODES['TAMPERING_DETECTED']:
                return self._show_banned_window("Tampering detected")
                
            else:
                return self._show_banned_window(f"Protection error: {result.error_message}")
                
        except Exception as e:
            logger.error(f"Error handling validation result: {e}")
            return False
    
    def _show_activation_window(self) -> bool:
        """Показать окно активации"""
        try:
            logger.info("Showing activation window")
            
            auth_window = AuthWindow()
            result = auth_window.show()
            
            if result['success']:
                logger.info("License activated successfully")
                return True
            else:
                logger.warning("License activation failed or cancelled")
                return False
                
        except Exception as e:
            logger.error(f"Error showing activation window: {e}")
            return False
    
    def _show_expired_window(self) -> bool:
        """Показать окно истечения лицензии"""
        try:
            logger.info("Showing license expired window")
            
            expired_window = ExpiredWindow()
            expired_window.show()
            
            return False  # Всегда блокируем при истечении
            
        except Exception as e:
            logger.error(f"Error showing expired window: {e}")
            return False
    
    def _show_banned_window(self, reason: str) -> bool:
        """Показать окно блокировки"""
        try:
            logger.info(f"Showing banned window: {reason}")
            
            banned_window = BannedWindow(reason)
            banned_window.show()
            
            return False  # Всегда блокируем при бане
            
        except Exception as e:
            logger.error(f"Error showing banned window: {e}")
            return False
    
    def _handle_tampering(self, reason: str):
        """Обработка обнаружения взлома"""
        try:
            logger.critical(f"TAMPERING DETECTED: {reason}")
            
            # Записываем в блок-лист
            from .runtime.block_state import BlockState
            block_state = BlockState()
            block_state.add_violation(reason)
            
            # Если включено самоуничтожение
            if SECURITY_SETTINGS['enable_self_delete']:
                from .runtime.self_delete import SelfDelete
                self_delete = SelfDelete()
                self_delete.trigger(reason)
            
            # Показываем окно и завершаем
            self._show_banned_window(f"Security violation: {reason}")
            sys.exit(ERROR_CODES['TAMPERING_DETECTED'])
            
        except Exception as e:
            logger.error(f"Error handling tampering: {e}")
            sys.exit(-1)
    
    def start_background_monitoring(self):
        """Запуск фонового мониторинга"""
        def monitor_thread():
            try:
                while self._protection_active:
                    time.sleep(300)  # Проверка каждые 5 минут
                    
                    # Переваlidация лицензии
                    if time.time() - getattr(self, '_last_check', 0) > 3600:  # Каждый час
                        result = self.validate_license()
                        if not result.is_valid:
                            logger.warning("Background validation failed")
                            self.handle_validation_result(result)
                        self._last_check = time.time()
                    
                    # Проверка безопасности
                    if self.anti_debug.is_debugger_present():
                        self._handle_tampering("Debugger attached during runtime")
                    
            except Exception as e:
                logger.error(f"Background monitoring error: {e}")
        
        thread = threading.Thread(target=monitor_thread, daemon=True)
        thread.start()
        logger.info("Background monitoring started")
    
    def shutdown(self):
        """Завершение работы защиты"""
        try:
            logger.info("Shutting down protection system...")
            
            self._protection_active = False
            self.watchdog.stop()
            self.anti_debug.stop_monitoring()
            
            logger.info("Protection system shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

def auto_protect() -> bool:
    """
    Главная функция автоматической защиты
    Вызывается при импорте библиотеки
    
    Returns:
        bool: True если защита активирована успешно
    """
    protection_manager = None
    
    try:
        logger.info("=== Kil0p3 Auto-Protection Starting ===")
        
        # Создаем менеджер защиты
        protection_manager = ProtectionManager()
        
        # Инициализация
        if not protection_manager.initialize():
            logger.critical("Protection initialization failed")
            return False
        
        # Валидация лицензии
        validation_result = protection_manager.validate_license()
        
        # Обработка результата
        if not protection_manager.handle_validation_result(validation_result):
            logger.warning("License validation failed - protection inactive")
            return False
        
        # Активация защиты
        protection_manager._protection_active = True
        protection_manager.start_background_monitoring()
        
        logger.info("=== Kil0p3 Protection Active ===")
        return True
        
    except KeyboardInterrupt:
        logger.info("Protection interrupted by user")
        return False
        
    except Exception as e:
        logger.critical(f"Auto-protection fatal error: {e}")
        
        # В случае критической ошибки принудительно завершаем
        if not os.getenv('KIL0P3_DEV_MODE'):
            sys.exit(ERROR_CODES['UNKNOWN_ERROR'])
        
        return False
        
    finally:
        # Cleanup
        if protection_manager and hasattr(protection_manager, '_protection_active'):
            if not protection_manager._protection_active:
                # Если защита не активна - завершаем программу
                if not os.getenv('KIL0P3_DEV_MODE'):
                    logger.critical("Protection failed - terminating application")
                    sys.exit(ERROR_CODES['LICENSE_INVALID'])

def manual_protect(license_key: Optional[str] = None) -> bool:
    """
    Ручная активация защиты с опциональным ключом
    
    Args:
        license_key: Лицензионный ключ (опционально)
        
    Returns:
        bool: True если защита активирована
    """
    try:
        logger.info("Manual protection activation requested")
        
        # Если передан ключ - устанавливаем его
        if license_key:
            from .core.license import LicenseManager
            license_manager = LicenseManager()
            license_manager.save_license(license_key)
            logger.info("License key set manually")
        
        # Запускаем автозащиту
        return auto_protect()
        
    except Exception as e:
        logger.error(f"Manual protection error: {e}")
        return False

def check_protection_status() -> Dict[str, Any]:
    """
    Проверить статус защиты
    
    Returns:
        Dict с информацией о состоянии защиты
    """
    try:
        protection_manager = ProtectionManager()
        validation_result = protection_manager.validate_license()
        
        return {
            'protection_active': validation_result.is_valid,
            'license_valid': validation_result.is_valid,
            'error_code': validation_result.error_code,
            'error_message': validation_result.error_message,
            'last_check': time.time(),
            'version': VERSION
        }
        
    except Exception as e:
        return {
            'protection_active': False,
            'license_valid': False,
            'error_code': ERROR_CODES['UNKNOWN_ERROR'],
            'error_message': str(e),
            'last_check': time.time(),
            'version': VERSION
        }

# Экспорт основных функций
__all__ = [
    'auto_protect',
    'manual_protect', 
    'check_protection_status',
    'ProtectionManager'
]