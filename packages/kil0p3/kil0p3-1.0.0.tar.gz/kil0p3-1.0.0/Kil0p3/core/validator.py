#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 System Validator
======================

Комплексная валидация всех систем защиты
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from ..config.constants import *
from ..tools.logger import get_logger
from ..core.license import license_manager, LicenseInfo
from ..core.hwid import hwid_generator
from ..runtime.attempt_counter import AttemptCounter
from ..runtime.block_state import BlockState

logger = get_logger(__name__)

class ValidationStatus(Enum):
    """Статусы валидации"""
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    REVOKED = "revoked"
    BLOCKED = "blocked"
    TAMPERED = "tampered"
    ERROR = "error"

@dataclass
class ValidationResult:
    """Результат валидации"""
    is_valid: bool
    status: ValidationStatus
    error_code: int
    error_message: str
    license_info: Optional[LicenseInfo] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

class SystemValidator:
    """Системный валидатор для комплексной проверки защиты"""
    
    def __init__(self):
        self.attempt_counter = AttemptCounter()
        self.block_state = BlockState()
        self._last_validation = None
        self._validation_cache_ttl = 300  # 5 минут кеш
    
    def validate_full(self, force_refresh: bool = False) -> ValidationResult:
        """
        Полная валидация всех систем защиты
        
        Args:
            force_refresh: Принудительное обновление кеша
            
        Returns:
            ValidationResult: Результат валидации
        """
        try:
            logger.debug("Starting full system validation...")
            
            # Проверка кеша
            if not force_refresh and self._is_cache_valid():
                logger.debug("Using cached validation result")
                return self._last_validation
            
            start_time = time.time()
            
            # 1. Проверка блокировки устройства
            block_result = self._check_device_block()
            if not block_result.is_valid:
                return block_result
            
            # 2. Проверка лимита попыток
            attempt_result = self._check_attempt_limit()
            if not attempt_result.is_valid:
                return attempt_result
            
            # 3. Базовая проверка лицензии
            license_result = self._check_license()
            if not license_result.is_valid:
                return license_result
            
            # 4. Проверка HWID
            hwid_result = self._check_hardware_binding(license_result.license_info)
            if not hwid_result.is_valid:
                return hwid_result
            
            # 5. Проверка времени системы
            time_result = self._check_system_time(license_result.license_info)
            if not time_result.is_valid:
                return time_result
            
            # 6. Проверка сетевых ограничений
            network_result = self._check_network_restrictions(license_result.license_info)
            if not network_result.is_valid:
                return network_result
            
            # 7. Проверка целостности системы
            integrity_result = self._check_system_integrity()
            if not integrity_result.is_valid:
                return integrity_result
            
            # Сбор всех предупреждений
            all_warnings = []
            for result in [license_result, hwid_result, time_result, network_result, integrity_result]:
                all_warnings.extend(result.warnings)
            
            # Создание финального результата
            final_result = ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="Validation successful",
                license_info=license_result.license_info,
                warnings=all_warnings
            )
            
            # Кеширование результата
            self._last_validation = final_result
            self._last_validation_time = time.time()
            
            validation_time = time.time() - start_time
            logger.info(f"Full validation completed in {validation_time:.2f}s - Status: VALID")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Full validation failed: {e}")
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.ERROR,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=f"Validation error: {e}"
            )
    
    def _check_device_block(self) -> ValidationResult:
        """Проверка блокировки устройства"""
        try:
            if self.block_state.is_blocked():
                block_info = self.block_state.get_block_info()
                
                logger.warning(f"Device is blocked: {block_info.get('reason', 'Unknown')}")
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.BLOCKED,
                    error_code=ERROR_CODES['TOO_MANY_ATTEMPTS'],
                    error_message=f"Device blocked: {block_info.get('reason', 'Security violation')}"
                )
            
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="Device not blocked"
            )
            
        except Exception as e:
            logger.error(f"Block check failed: {e}")
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.ERROR,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=f"Block check error: {e}"
            )
    
    def _check_attempt_limit(self) -> ValidationResult:
        """Проверка лимита попыток активации"""
        try:
            attempts = self.attempt_counter.get_attempts()
            
            if attempts >= MAX_ACTIVATION_ATTEMPTS:
                logger.warning(f"Too many activation attempts: {attempts}/{MAX_ACTIVATION_ATTEMPTS}")
                
                # Блокируем устройство
                self.block_state.block_device("Too many activation attempts")
                
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.BLOCKED,
                    error_code=ERROR_CODES['TOO_MANY_ATTEMPTS'],
                    error_message=f"Too many activation attempts ({attempts}/{MAX_ACTIVATION_ATTEMPTS})"
                )
            
            warnings = []
            if attempts > 0:
                warnings.append(f"Previous activation attempts: {attempts}/{MAX_ACTIVATION_ATTEMPTS}")
            
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="Attempt limit OK",
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Attempt limit check failed: {e}")
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.ERROR,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=f"Attempt check error: {e}"
            )
    
    def _check_license(self) -> ValidationResult:
        """Базовая проверка лицензии"""
        try:
            # Загружаем лицензию
            license_info = license_manager.load_license()
            
            if license_info is None:
                logger.info("No license found")
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.INVALID,
                    error_code=ERROR_CODES['LICENSE_INVALID'],
                    error_message="No license found"
                )
            
            # Валидация лицензии
            is_valid, error_message = license_manager.validate_license(license_info)
            
            if not is_valid:
                logger.warning(f"License validation failed: {error_message}")
                
                # Определяем тип ошибки
                if "expired" in error_message.lower():
                    status = ValidationStatus.EXPIRED
                    error_code = ERROR_CODES['LICENSE_EXPIRED']
                elif "revoked" in error_message.lower():
                    status = ValidationStatus.REVOKED
                    error_code = ERROR_CODES['LICENSE_REVOKED']
                else:
                    status = ValidationStatus.INVALID
                    error_code = ERROR_CODES['LICENSE_INVALID']
                
                return ValidationResult(
                    is_valid=False,
                    status=status,
                    error_code=error_code,
                    error_message=error_message,
                    license_info=license_info
                )
            
            # Проверка срока действия с предупреждением
            warnings = []
            days_remaining = license_info.days_remaining()
            if days_remaining <= 7:
                warnings.append(f"License expires in {days_remaining} days")
            
            logger.info(f"License validation successful: {license_info.key[-8:]}")
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="License valid",
                license_info=license_info,
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"License check failed: {e}")
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.ERROR,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=f"License check error: {e}"
            )
    
    def _check_hardware_binding(self, license_info: LicenseInfo) -> ValidationResult:
        """Проверка привязки к оборудованию"""
        try:
            if not license_info:
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.ERROR,
                    error_code=ERROR_CODES['UNKNOWN_ERROR'],
                    error_message="No license info for HWID check"
                )
            
            current_hwid = hwid_generator.generate()
            
            if license_info.hwid != current_hwid:
                logger.warning(f"HWID mismatch: expected {license_info.hwid[:8]}..., got {current_hwid[:8]}...")
                
                # Увеличиваем счетчик попыток
                self.attempt_counter.increment()
                
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.INVALID,
                    error_code=ERROR_CODES['HWID_MISMATCH'],
                    error_message="Hardware ID mismatch - license bound to different device"
                )
            
            logger.debug("HWID validation successful")
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="HWID binding valid"
            )
            
        except Exception as e:
            logger.error(f"HWID check failed: {e}")
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.ERROR,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=f"HWID check error: {e}"
            )
    
    def _check_system_time(self, license_info: LicenseInfo) -> ValidationResult:
        """Проверка манипуляций со временем"""
        try:
            if not license_info:
                return ValidationResult(
                    is_valid=True,
                    status=ValidationStatus.VALID,
                    error_code=ERROR_CODES['SUCCESS'],
                    error_message="No license for time check"
                )
            
            current_time = datetime.now()
            
            # Проверка на откат времени
            if current_time < license_info.issued_date:
                logger.warning("System time manipulation detected - time before license issue")
                
                # Блокируем устройство
                self.block_state.block_device("System time manipulation detected")
                
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.TAMPERED,
                    error_code=ERROR_CODES['TIME_MANIPULATION'],
                    error_message="System time manipulation detected"
                )
            
            # Проверка на слишком большое расхождение
            max_future_time = license_info.expiry_date + timedelta(days=MAX_CLOCK_DRIFT_DAYS)
            if current_time > max_future_time:
                logger.warning("System time too far in future")
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.TAMPERED,
                    error_code=ERROR_CODES['TIME_MANIPULATION'],
                    error_message="System time inconsistency detected"
                )
            
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="System time valid"
            )
            
        except Exception as e:
            logger.error(f"System time check failed: {e}")
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.ERROR,
                error_code=ERROR_CODES['UNKNOWN_ERROR'],
                error_message=f"Time check error: {e}"
            )
    
    def _check_network_restrictions(self, license_info: LicenseInfo) -> ValidationResult:
        """Проверка сетевых ограничений"""
        try:
            # Если сетевые проверки отключены
            if not SECURITY_SETTINGS.get('enable_network_validation', True):
                return ValidationResult(
                    is_valid=True,
                    status=ValidationStatus.VALID,
                    error_code=ERROR_CODES['SUCCESS'],
                    error_message="Network checks disabled"
                )
            
            warnings = []
            
            # Проверка IP адреса (если есть ограничения)
            if ALLOWED_IP_RANGES and license_info:
                current_ip = self._get_current_ip()
                if not self._is_ip_allowed(current_ip):
                    logger.warning(f"IP address not allowed: {current_ip}")
                    return ValidationResult(
                        is_valid=False,
                        status=ValidationStatus.INVALID,
                        error_code=ERROR_CODES['IP_BLOCKED'],
                        error_message=f"IP address blocked: {current_ip}"
                    )
            
            # Проверка геолокации (если есть ограничения)
            if BLOCKED_COUNTRIES:
                country = self._get_country_by_ip()
                if country in BLOCKED_COUNTRIES:
                    logger.warning(f"Country blocked: {country}")
                    return ValidationResult(
                        is_valid=False,
                        status=ValidationStatus.INVALID,
                        error_code=ERROR_CODES['IP_BLOCKED'],
                        error_message=f"Country blocked: {country}"
                    )
            
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="Network restrictions passed",
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Network check failed: {e}")
            return ValidationResult(
                is_valid=True,  # Не блокируем из-за сетевых ошибок
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="Network check skipped due to error",
                warnings=[f"Network check error: {e}"]
            )
    
    def _check_system_integrity(self) -> ValidationResult:
        """Проверка целостности системы"""
        try:
            if not SECURITY_SETTINGS.get('enable_integrity_check', True):
                return ValidationResult(
                    is_valid=True,
                    status=ValidationStatus.VALID,
                    error_code=ERROR_CODES['SUCCESS'],
                    error_message="Integrity checks disabled"
                )
            
            warnings = []
            
            # Проверка отладчиков
            from ..security.anti_debug import AntiDebug
            anti_debug = AntiDebug()
            
            if anti_debug.is_debugger_present():
                logger.warning("Debugger detected")
                self.block_state.block_device("Debugger detected")
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.TAMPERED,
                    error_code=ERROR_CODES['TAMPERING_DETECTED'],
                    error_message="Debugger detected"
                )
            
            # Проверка виртуальных машин
            if SECURITY_SETTINGS.get('enable_vm_detection', True):
                from ..security.vm_detect import VMDetector
                vm_detector = VMDetector()
                
                if vm_detector.is_virtual_machine():
                    vm_name = vm_detector.get_vm_name()
                    warnings.append(f"Virtual machine detected: {vm_name}")
                    logger.info(f"Running in VM: {vm_name}")
            
            # Проверка целостности кода
            from ..core.tamper import TamperProtection
            tamper = TamperProtection()
            
            if not tamper.verify_integrity():
                logger.warning("Code integrity violation")
                self.block_state.block_device("Code integrity violation")
                return ValidationResult(
                    is_valid=False,
                    status=ValidationStatus.TAMPERED,
                    error_code=ERROR_CODES['TAMPERING_DETECTED'],
                    error_message="Code integrity violation detected"
                )
            
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="System integrity valid",
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Integrity check failed: {e}")
            return ValidationResult(
                is_valid=True,  # Не блокируем из-за ошибок проверки
                status=ValidationStatus.VALID,
                error_code=ERROR_CODES['SUCCESS'],
                error_message="Integrity check skipped due to error",
                warnings=[f"Integrity check error: {e}"]
            )
    
    def _is_cache_valid(self) -> bool:
        """Проверка валидности кеша"""
        if not self._last_validation or not hasattr(self, '_last_validation_time'):
            return False
        
        cache_age = time.time() - self._last_validation_time
        return cache_age < self._validation_cache_ttl
    
    def _get_current_ip(self) -> str:
        """Получение текущего IP адреса"""
        try:
            import requests
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text.strip()
        except:
            return "unknown"
    
    def _is_ip_allowed(self, ip: str) -> bool:
        """Проверка разрешен ли IP адрес"""
        # Простая реализация - в реальности нужна более сложная логика
        if not ALLOWED_IP_RANGES:
            return True
        
        # Здесь должна быть логика проверки IP диапазонов
        return True
    
    def _get_country_by_ip(self) -> str:
        """Получение страны по IP адресу"""
        try:
            import requests
            ip = self._get_current_ip()
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            data = response.json()
            return data.get('countryCode', 'unknown')
        except:
            return "unknown"
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Получение сводки последней валидации
        
        Returns:
            Dict с информацией о валидации
        """
        if not self._last_validation:
            return {
                'status': 'not_validated',
                'message': 'No validation performed yet'
            }
        
        result = self._last_validation
        
        return {
            'status': result.status.value,
            'is_valid': result.is_valid,
            'error_code': result.error_code,
            'error_message': result.error_message,
            'warnings_count': len(result.warnings),
            'warnings': result.warnings,
            'license_info': {
                'key': result.license_info.key[-8:] + '...' if result.license_info else None,
                'type': result.license_info.license_type if result.license_info else None,
                'expires': result.license_info.expiry_date.strftime('%Y-%m-%d') if result.license_info else None,
                'days_remaining': result.license_info.days_remaining() if result.license_info else None
            } if result.license_info else None,
            'last_validation': getattr(self, '_last_validation_time', None),
            'validation_age': time.time() - getattr(self, '_last_validation_time', time.time())
        }
    
    def force_revalidation(self) -> ValidationResult:
        """
        Принудительная повторная валидация
        
        Returns:
            ValidationResult: Новый результат валидации
        """
        logger.info("Forcing system revalidation...")
        return self.validate_full(force_refresh=True)

# Глобальный экземпляр валидатора
system_validator = SystemValidator()

def validate_system() -> ValidationResult:
    """
    Быстрая валидация системы
    
    Returns:
        ValidationResult: Результат валидации
    """
    return system_validator.validate_full()

def get_system_status() -> Dict[str, Any]:
    """
    Получение статуса системы защиты
    
    Returns:
        Dict с информацией о статусе
    """
    return system_validator.get_validation_summary()