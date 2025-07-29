#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/core/tamper.py
=====================

Защита от модификации и взлома
"""

import os
import sys
import hashlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any

# Импорт констант
try:
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

class TamperProtection:
    """Система защиты от модификации кода"""
    
    def __init__(self):
        self._file_hashes: Dict[str, str] = {}
        self._critical_files: List[str] = []
        self._init_protection()
    
    def _init_protection(self):
        """Инициализация защиты"""
        try:
            # Определяем критически важные файлы
            self._critical_files = self._get_critical_files()
            
            # Вычисляем хеши критических файлов
            self._calculate_initial_hashes()
            
            logger.debug(f"Tamper protection initialized for {len(self._critical_files)} files")
            
        except Exception as e:
            logger.error(f"Failed to initialize tamper protection: {e}")
    
    def _get_critical_files(self) -> List[str]:
        """Получение списка критических файлов для мониторинга"""
        try:
            critical_files = []
            
            # Получаем путь к модулю Kil0p3
            try:
                import Kil0p3
                kil0p3_path = Path(Kil0p3.__file__).parent
            except:
                # Fallback - ищем относительно текущего файла
                kil0p3_path = Path(__file__).parent.parent
            
            # Критические модули
            critical_modules = [
                '__init__.py',
                'run.py',
                'core/encryption.py',
                'core/license.py',
                'core/validator.py',
                'core/hwid.py',
                'security/anti_debug.py',
                'runtime/attempt_counter.py',
                'runtime/block_state.py'
            ]
            
            for module in critical_modules:
                file_path = kil0p3_path / module
                if file_path.exists():
                    critical_files.append(str(file_path))
            
            return critical_files
            
        except Exception as e:
            logger.debug(f"Error getting critical files: {e}")
            return []
    
    def _calculate_initial_hashes(self):
        """Вычисление начальных хешей файлов"""
        try:
            for file_path in self._critical_files:
                try:
                    file_hash = self._calculate_file_hash(file_path)
                    if file_hash:
                        self._file_hashes[file_path] = file_hash
                except Exception as e:
                    logger.debug(f"Error hashing file {file_path}: {e}")
            
            logger.debug(f"Calculated hashes for {len(self._file_hashes)} files")
            
        except Exception as e:
            logger.error(f"Error calculating initial hashes: {e}")
    
    def _calculate_file_hash(self, file_path: str) -> Optional[str]:
        """
        Вычисление SHA256 хеша файла
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Optional[str]: Хеш файла или None при ошибке
        """
        try:
            hash_sha256 = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                # Читаем файл блоками для больших файлов
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            
            return hash_sha256.hexdigest()
            
        except Exception as e:
            logger.debug(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def verify_integrity(self) -> bool:
        """
        Проверка целостности критических файлов
        
        Returns:
            bool: True если целостность не нарушена
        """
        try:
            if not self._file_hashes:
                logger.warning("No file hashes available for integrity check")
                return True  # Не блокируем если нет хешей
            
            modified_files = []
            
            for file_path, original_hash in self._file_hashes.items():
                try:
                    # Проверяем существование файла
                    if not os.path.exists(file_path):
                        logger.warning(f"Critical file missing: {file_path}")
                        modified_files.append(f"{file_path} (missing)")
                        continue
                    
                    # Вычисляем текущий хеш
                    current_hash = self._calculate_file_hash(file_path)
                    
                    if current_hash != original_hash:
                        logger.warning(f"File integrity violation: {file_path}")
                        modified_files.append(f"{file_path} (modified)")
                
                except Exception as e:
                    logger.debug(f"Error checking file {file_path}: {e}")
                    continue
            
            if modified_files:
                logger.critical(f"Integrity violations detected in {len(modified_files)} files")
                for file_info in modified_files:
                    logger.critical(f"  - {file_info}")
                return False
            
            logger.debug("File integrity check passed")
            return True
            
        except Exception as e:
            logger.error(f"Error during integrity verification: {e}")
            return True  # Не блокируем при ошибках проверки
    
    def check_import_tampering(self) -> bool:
        """
        Проверка на модификацию импортированных модулей
        
        Returns:
            bool: True если модули не модифицированы
        """
        try:
            # Проверяем ключевые модули Kil0p3
            critical_modules = [
                'Kil0p3',
                'Kil0p3.core.encryption',
                'Kil0p3.core.license',
                'Kil0p3.core.validator'
            ]
            
            for module_name in critical_modules:
                if module_name in sys.modules:
                    module = sys.modules[module_name]
                    
                    # Проверяем наличие критических функций/классов
                    if not self._verify_module_structure(module, module_name):
                        logger.warning(f"Module structure tampering detected: {module_name}")
                        return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking import tampering: {e}")
            return True
    
    def _verify_module_structure(self, module, module_name: str) -> bool:
        """Проверка структуры модуля"""
        try:
            # Определяем ожидаемые атрибуты для каждого модуля
            expected_attributes = {
                'Kil0p3': ['get_version', 'get_status', 'set_license', '__version__'],
                'Kil0p3.core.encryption': ['CryptographyManager', 'crypto_manager'],
                'Kil0p3.core.license': ['LicenseManager', 'license_manager'],
                'Kil0p3.core.validator': ['SystemValidator', 'system_validator']
            }
            
            if module_name in expected_attributes:
                for attr_name in expected_attributes[module_name]:
                    if not hasattr(module, attr_name):
                        logger.warning(f"Missing attribute {attr_name} in {module_name}")
                        return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error verifying module structure for {module_name}: {e}")
            return True
    
    def check_runtime_tampering(self) -> bool:
        """
        Проверка на runtime модификации
        
        Returns:
            bool: True если runtime не скомпрометирован
        """
        try:
            # Проверяем sys.modules на подозрительные модули
            suspicious_modules = [
                'pdb', 'pudb', 'ipdb',  # Отладчики
                'dis',  # Дизассемблер
                'ast',  # Парсер AST (может использоваться для анализа)
            ]
            
            for sus_module in suspicious_modules:
                if sus_module in sys.modules:
                    logger.warning(f"Suspicious module detected: {sus_module}")
                    return False
            
            # Проверяем изменения в критических функциях
            if not self._check_function_integrity():
                return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking runtime tampering: {e}")
            return True
    
    def _check_function_integrity(self) -> bool:
        """Проверка целостности критических функций"""
        try:
            # Проверяем что критические функции не были перехвачены
            critical_functions = [
                ('builtins', '__import__'),
                ('sys', 'settrace'),
                ('os', 'system')
            ]
            
            for module_name, func_name in critical_functions:
                try:
                    if module_name == 'builtins':
                        import builtins
                        module = builtins
                    else:
                        module = sys.modules.get(module_name)
                    
                    if module and hasattr(module, func_name):
                        func = getattr(module, func_name)
                        
                        # Простая проверка - функция должна быть builtin или из правильного модуля
                        if hasattr(func, '__module__'):
                            if func.__module__ != module_name and func.__module__ != 'builtins':
                                logger.warning(f"Function {func_name} may be hooked: {func.__module__}")
                                return False
                
                except Exception as e:
                    logger.debug(f"Error checking function {module_name}.{func_name}: {e}")
                    continue
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking function integrity: {e}")
            return True
    
    def perform_full_check(self) -> Dict[str, Any]:
        """
        Полная проверка на вмешательство
        
        Returns:
            Dict: Результаты всех проверок
        """
        try:
            results = {
                'file_integrity': self.verify_integrity(),
                'import_tampering': self.check_import_tampering(),
                'runtime_tampering': self.check_runtime_tampering(),
                'overall_status': True
            }
            
            # Общий статус - все проверки должны пройти
            results['overall_status'] = all([
                results['file_integrity'],
                results['import_tampering'],
                results['runtime_tampering']
            ])
            
            if results['overall_status']:
                logger.info("All tamper protection checks passed")
            else:
                logger.warning("Tamper protection violations detected")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in full tamper check: {e}")
            return {
                'file_integrity': True,
                'import_tampering': True,
                'runtime_tampering': True,
                'overall_status': True,
                'error': str(e)
            }
    
    def get_protection_info(self) -> Dict[str, Any]:
        """
        Получение информации о состоянии защиты
        
        Returns:
            Dict: Информация о защите
        """
        return {
            'monitored_files': len(self._critical_files),
            'calculated_hashes': len(self._file_hashes),
            'critical_files': [os.path.basename(f) for f in self._critical_files],
            'protection_active': len(self._file_hashes) > 0
        }

# Глобальный экземпляр защиты от модификации
tamper_protection = TamperProtection()

# Удобные функции
def verify_code_integrity() -> bool:
    """Быстрая проверка целостности кода"""
    return tamper_protection.verify_integrity()

def check_for_tampering() -> bool:
    """Быстрая проверка на вмешательство"""
    results = tamper_protection.perform_full_check()
    return results['overall_status']

def get_tamper_protection_status() -> Dict[str, Any]:
    """Получение статуса защиты от модификации"""
    return tamper_protection.get_protection_info()