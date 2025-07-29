#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Hardware ID Generator
============================

Генерация уникальных идентификаторов оборудования
"""

import os
import sys
import platform
import hashlib
import subprocess
import uuid
from typing import Dict, List, Optional
import psutil

from ..config.constants import HWID_COMPONENTS
from ..tools.logger import get_logger

logger = get_logger(__name__)

class HardwareID:
    """Генератор уникального идентификатора оборудования"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self._hwid_cache = None
        
    def generate(self, use_cache: bool = True) -> str:
        """
        Генерация HWID
        
        Args:
            use_cache: Использовать кеш если доступен
            
        Returns:
            str: Уникальный идентификатор оборудования
        """
        try:
            if use_cache and self._hwid_cache:
                return self._hwid_cache
            
            logger.debug("Generating Hardware ID...")
            
            # Собираем компоненты системы
            components = self._collect_hardware_info()
            
            # Создаем уникальную строку
            hwid_string = self._create_hwid_string(components)
            
            # Хешируем для получения финального HWID
            hwid = self._hash_hwid(hwid_string)
            
            self._hwid_cache = hwid
            logger.info(f"HWID generated: {hwid[:8]}...{hwid[-8:]}")
            
            return hwid
            
        except Exception as e:
            logger.error(f"HWID generation failed: {e}")
            # Возвращаем fallback HWID
            return self._generate_fallback_hwid()
    
    def _collect_hardware_info(self) -> Dict[str, str]:
        """Сбор информации об оборудовании"""
        components = {}
        
        try:
            # CPU информация
            if 'cpu_id' in HWID_COMPONENTS:
                components['cpu_id'] = self._get_cpu_id()
            
            # Серийный номер материнской платы
            if 'motherboard_serial' in HWID_COMPONENTS:
                components['motherboard_serial'] = self._get_motherboard_serial()
            
            # Серийный номер диска
            if 'disk_serial' in HWID_COMPONENTS:
                components['disk_serial'] = self._get_disk_serial()
            
            # MAC адрес
            if 'mac_address' in HWID_COMPONENTS:
                components['mac_address'] = self._get_mac_address()
            
            # System UUID
            if 'system_uuid' in HWID_COMPONENTS:
                components['system_uuid'] = self._get_system_uuid()
            
            # Дополнительные компоненты
            components['architecture'] = platform.machine()
            components['processor'] = platform.processor()
            
            logger.debug(f"Collected {len(components)} hardware components")
            return components
            
        except Exception as e:
            logger.error(f"Error collecting hardware info: {e}")
            return {}
    
    def _get_cpu_id(self) -> str:
        """Получение CPU ID"""
        try:
            if self.platform == 'windows':
                return self._get_windows_cpu_id()
            elif self.platform == 'linux':
                return self._get_linux_cpu_id()
            elif self.platform == 'darwin':
                return self._get_macos_cpu_id()
            else:
                return platform.processor()
                
        except Exception as e:
            logger.debug(f"CPU ID detection failed: {e}")
            return "unknown_cpu"
    
    def _get_windows_cpu_id(self) -> str:
        """CPU ID для Windows"""
        try:
            # Используем WMIC для получения CPU ID
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'ProcessorId', '/value'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            for line in result.stdout.split('\n'):
                if 'ProcessorId=' in line:
                    return line.split('=')[1].strip()
            
            return "windows_cpu_unknown"
            
        except Exception:
            return "windows_cpu_error"
    
    def _get_linux_cpu_id(self) -> str:
        """CPU ID для Linux"""
        try:
            # Читаем /proc/cpuinfo
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        return line.split(':')[1].strip()
            
            return "linux_cpu_unknown"
            
        except Exception:
            return "linux_cpu_error"
    
    def _get_macos_cpu_id(self) -> str:
        """CPU ID для macOS"""
        try:
            result = subprocess.run(
                ['sysctl', '-n', 'machdep.cpu.brand_string'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
            
        except Exception:
            return "macos_cpu_error"
    
    def _get_motherboard_serial(self) -> str:
        """Получение серийного номера материнской платы"""
        try:
            if self.platform == 'windows':
                result = subprocess.run(
                    ['wmic', 'baseboard', 'get', 'SerialNumber', '/value'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                for line in result.stdout.split('\n'):
                    if 'SerialNumber=' in line:
                        serial = line.split('=')[1].strip()
                        if serial and serial != 'To be filled by O.E.M.':
                            return serial
                
            elif self.platform == 'linux':
                try:
                    result = subprocess.run(
                        ['sudo', 'dmidecode', '-s', 'baseboard-serial-number'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    pass
            
            return "motherboard_unknown"
            
        except Exception:
            return "motherboard_error"
    
    def _get_disk_serial(self) -> str:
        """Получение серийного номера диска"""
        try:
            # Получаем информацию о дисках через psutil
            disks = psutil.disk_partitions()
            
            for disk in disks:
                if disk.device == '/' or 'C:' in disk.device:
                    # Основной диск найден
                    if self.platform == 'windows':
                        result = subprocess.run(
                            ['wmic', 'diskdrive', 'get', 'SerialNumber', '/value'],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        
                        for line in result.stdout.split('\n'):
                            if 'SerialNumber=' in line:
                                serial = line.split('=')[1].strip()
                                if serial:
                                    return serial
                    
                    elif self.platform == 'linux':
                        # Пытаемся получить серийный номер через различные методы
                        device = disk.device.replace('/dev/', '').rstrip('0123456789')
                        try:
                            result = subprocess.run(
                                ['lsblk', '-d', '-o', 'serial', f'/dev/{device}'],
                                capture_output=True,
                                text=True,
                                timeout=10
                            )
                            if result.returncode == 0:
                                lines = result.stdout.strip().split('\n')
                                if len(lines) > 1:
                                    return lines[1].strip()
                        except:
                            pass
                    break
            
            return "disk_unknown"
            
        except Exception:
            return "disk_error"
    
    def _get_mac_address(self) -> str:
        """Получение MAC адреса"""
        try:
            # Получаем MAC адрес первого активного сетевого интерфейса
            interfaces = psutil.net_if_addrs()
            
            for interface_name, addresses in interfaces.items():
                # Пропускаем loopback и виртуальные интерфейсы
                if interface_name.startswith(('lo', 'docker', 'veth', 'br-')):
                    continue
                
                for addr in addresses:
                    if addr.family == psutil.AF_LINK:  # MAC address
                        mac = addr.address
                        if mac and mac != '00:00:00:00:00:00':
                            return mac.replace(':', '').replace('-', '').upper()
            
            # Fallback - используем uuid.getnode()
            mac = hex(uuid.getnode())[2:].upper()
            return mac
            
        except Exception:
            return "mac_unknown"
    
    def _get_system_uuid(self) -> str:
        """Получение System UUID"""
        try:
            if self.platform == 'windows':
                result = subprocess.run(
                    ['wmic', 'csproduct', 'get', 'UUID', '/value'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                for line in result.stdout.split('\n'):
                    if 'UUID=' in line:
                        uuid_str = line.split('=')[1].strip()
                        if uuid_str and uuid_str != 'To be filled by O.E.M.':
                            return uuid_str
                
            elif self.platform == 'linux':
                try:
                    with open('/sys/class/dmi/id/product_uuid', 'r') as f:
                        return f.read().strip()
                except:
                    try:
                        result = subprocess.run(
                            ['sudo', 'dmidecode', '-s', 'system-uuid'],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        if result.returncode == 0:
                            return result.stdout.strip()
                    except:
                        pass
            
            elif self.platform == 'darwin':
                result = subprocess.run(
                    ['system_profiler', 'SPHardwareDataType'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                for line in result.stdout.split('\n'):
                    if 'Hardware UUID' in line:
                        return line.split(':')[1].strip()
            
            return str(uuid.uuid4())
            
        except Exception:
            return "uuid_error"
    
    def _create_hwid_string(self, components: Dict[str, str]) -> str:
        """Создание строки HWID из компонентов"""
        try:
            # Сортируем компоненты для консистентности
            sorted_components = sorted(components.items())
            
            # Создаем строку
            hwid_parts = []
            for key, value in sorted_components:
                if value and value not in ['unknown', 'error', '']:
                    hwid_parts.append(f"{key}:{value}")
            
            hwid_string = "|".join(hwid_parts)
            
            # Добавляем системную информацию
            hwid_string += f"|platform:{self.platform}"
            hwid_string += f"|python:{sys.version_info.major}.{sys.version_info.minor}"
            
            logger.debug(f"HWID string created: {len(hwid_string)} chars")
            return hwid_string
            
        except Exception as e:
            logger.error(f"Error creating HWID string: {e}")
            return "fallback_hwid_string"
    
    def _hash_hwid(self, hwid_string: str) -> str:
        """Хеширование HWID строки"""
        try:
            # Используем SHA256 для получения финального HWID
            hash_obj = hashlib.sha256(hwid_string.encode('utf-8'))
            hwid_hash = hash_obj.hexdigest()
            
            # Возвращаем первые 32 символа для удобства
            return hwid_hash[:32].upper()
            
        except Exception as e:
            logger.error(f"HWID hashing failed: {e}")
            return "FALLBACK_HWID_HASH_ERROR"
    
    def _generate_fallback_hwid(self) -> str:
        """Генерация fallback HWID в случае ошибок"""
        try:
            # Используем базовую системную информацию
            fallback_data = [
                platform.system(),
                platform.machine(),
                platform.processor() or "unknown_processor",
                str(uuid.getnode()),  # MAC address как число
                os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'unknown'))
            ]
            
            fallback_string = "|".join(str(item) for item in fallback_data)
            return hashlib.sha256(fallback_string.encode('utf-8')).hexdigest()[:32].upper()
            
        except Exception:
            # Последний резерв - статический HWID
            return "STATIC_FALLBACK_HWID_12345678"
    
    def validate_hwid(self, expected_hwid: str) -> bool:
        """
        Проверка соответствия HWID
        
        Args:
            expected_hwid: Ожидаемый HWID
            
        Returns:
            bool: True если HWID совпадает
        """
        try:
            current_hwid = self.generate()
            match = current_hwid == expected_hwid
            
            if match:
                logger.info("HWID validation successful")
            else:
                logger.warning(f"HWID mismatch: expected {expected_hwid[:8]}..., got {current_hwid[:8]}...")
            
            return match
            
        except Exception as e:
            logger.error(f"HWID validation error: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Получение детальной информации о системе
        
        Returns:
            Dict с информацией о системе
        """
        try:
            info = {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'python_implementation': platform.python_implementation(),
            }
            
            # Добавляем CPU информацию
            try:
                info['cpu_count'] = str(psutil.cpu_count())
                info['cpu_freq'] = str(psutil.cpu_freq().current if psutil.cpu_freq() else 'unknown')
            except:
                pass
            
            # Добавляем память
            try:
                memory = psutil.virtual_memory()
                info['total_memory'] = str(memory.total)
            except:
                pass
            
            # Добавляем диски
            try:
                disk_usage = psutil.disk_usage('/')
                info['disk_total'] = str(disk_usage.total)
            except:
                try:
                    disk_usage = psutil.disk_usage('C:\\')
                    info['disk_total'] = str(disk_usage.total)
                except:
                    pass
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}

# Глобальный экземпляр генератора HWID
hwid_generator = HardwareID()

def get_hwid() -> str:
    """
    Быстрое получение HWID
    
    Returns:
        str: Hardware ID текущей системы
    """
    return hwid_generator.generate()

def validate_hwid(expected_hwid: str) -> bool:
    """
    Быстрая проверка HWID
    
    Args:
        expected_hwid: Ожидаемый HWID
        
    Returns:
        bool: True если HWID совпадает
    """
    return hwid_generator.validate_hwid(expected_hwid)

def get_system_fingerprint() -> Dict[str, str]:
    """
    Получение отпечатка системы
    
    Returns:
        Dict с системной информацией
    """
    return hwid_generator.get_system_info()