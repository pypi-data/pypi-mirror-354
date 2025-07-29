#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/security/vm_detect.py
============================

Детекция виртуальных машин и песочниц
"""

import platform
import subprocess
import os
import re
from typing import List, Dict, Any, Optional

# Импорт констант
try:
    from ..config.constants import VM_ARTIFACTS, SANDBOX_ARTIFACTS
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback если модули недоступны
    VM_ARTIFACTS = ['VMware', 'VirtualBox', 'QEMU', 'Xen', 'Hyper-V', 'KVM']
    SANDBOX_ARTIFACTS = ['Cuckoo', 'Anubis', 'Joe Sandbox']
    
    import logging
    logger = logging.getLogger(__name__)

class VMDetector:
    """Детектор виртуальных машин и песочниц"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self._vm_cache = None
        self._detection_methods = [
            self._check_system_info,
            self._check_hardware_info,
            self._check_processes,
            self._check_registry,
            self._check_files,
            self._check_network_adapters,
            self._check_system_uptime
        ]
    
    def is_virtual_machine(self) -> bool:
        """
        Комплексная проверка виртуальной машины
        
        Returns:
            bool: True если обнаружена VM
        """
        try:
            # Используем кеш если доступен
            if self._vm_cache is not None:
                return self._vm_cache
            
            logger.debug("Starting VM detection...")
            
            detection_results = []
            
            # Выполняем все методы детекции
            for method in self._detection_methods:
                try:
                    result = method()
                    detection_results.append(result)
                    
                    if result:
                        method_name = method.__name__
                        logger.info(f"VM detected by {method_name}")
                        
                except Exception as e:
                    logger.debug(f"Error in detection method {method.__name__}: {e}")
                    detection_results.append(False)
            
            # VM обнаружена если любой метод вернул True
            is_vm = any(detection_results)
            
            # Кешируем результат
            self._vm_cache = is_vm
            
            if is_vm:
                vm_name = self.get_vm_name()
                logger.info(f"Virtual machine detected: {vm_name}")
            else:
                logger.debug("No virtual machine detected")
            
            return is_vm
            
        except Exception as e:
            logger.error(f"VM detection error: {e}")
            return False
    
    def get_vm_name(self) -> str:
        """
        Получение имени виртуальной машины
        
        Returns:
            str: Название VM или "Unknown"
        """
        try:
            # Проверяем системную информацию
            system_info = platform.platform().lower()
            
            for vm_name in VM_ARTIFACTS:
                if vm_name.lower() in system_info:
                    return vm_name
            
            # Проверяем дополнительные источники
            vm_name = self._detect_vm_name_advanced()
            if vm_name:
                return vm_name
            
            return "Unknown VM"
            
        except Exception as e:
            logger.debug(f"Error getting VM name: {e}")
            return "Unknown"
    
    def _check_system_info(self) -> bool:
        """Проверка системной информации"""
        try:
            # Проверяем platform
            system_info = platform.platform().lower()
            processor = platform.processor().lower()
            
            vm_indicators = VM_ARTIFACTS + SANDBOX_ARTIFACTS
            
            for indicator in vm_indicators:
                if indicator.lower() in system_info or indicator.lower() in processor:
                    logger.debug(f"VM indicator found in system info: {indicator}")
                    return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking system info: {e}")
            return False
    
    def _check_hardware_info(self) -> bool:
        """Проверка информации об оборудовании"""
        try:
            if self.platform == 'windows':
                return self._check_windows_hardware()
            elif self.platform == 'linux':
                return self._check_linux_hardware()
            elif self.platform == 'darwin':
                return self._check_macos_hardware()
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking hardware info: {e}")
            return False
    
    def _check_windows_hardware(self) -> bool:
        """Проверка оборудования Windows"""
        try:
            # Проверяем BIOS
            result = subprocess.run(
                ['wmic', 'bios', 'get', 'manufacturer', '/value'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout.lower()
                vm_bios = ['vmware', 'virtualbox', 'qemu', 'microsoft corporation']
                
                for vm in vm_bios:
                    if vm in output:
                        logger.debug(f"VM BIOS detected: {vm}")
                        return True
            
            # Проверяем модель компьютера
            result = subprocess.run(
                ['wmic', 'computersystem', 'get', 'model', '/value'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout.lower()
                vm_models = ['vmware', 'virtualbox', 'virtual machine']
                
                for vm in vm_models:
                    if vm in output:
                        logger.debug(f"VM model detected: {vm}")
                        return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking Windows hardware: {e}")
            return False
    
    def _check_linux_hardware(self) -> bool:
        """Проверка оборудования Linux"""
        try:
            # Проверяем DMI информацию
            dmi_files = [
                '/sys/class/dmi/id/sys_vendor',
                '/sys/class/dmi/id/product_name',
                '/sys/class/dmi/id/board_vendor'
            ]
            
            for dmi_file in dmi_files:
                try:
                    with open(dmi_file, 'r') as f:
                        content = f.read().lower().strip()
                        
                        vm_vendors = ['vmware', 'virtualbox', 'qemu', 'microsoft']
                        for vm in vm_vendors:
                            if vm in content:
                                logger.debug(f"VM vendor detected in {dmi_file}: {vm}")
                                return True
                except:
                    continue
            
            # Проверяем /proc/cpuinfo
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read().lower()
                    
                    vm_cpu_flags = ['hypervisor', 'vmware', 'virtualbox']
                    for flag in vm_cpu_flags:
                        if flag in cpuinfo:
                            logger.debug(f"VM CPU flag detected: {flag}")
                            return True
            except:
                pass
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking Linux hardware: {e}")
            return False
    
    def _check_macos_hardware(self) -> bool:
        """Проверка оборудования macOS"""
        try:
            # Проверяем system_profiler
            result = subprocess.run(
                ['system_profiler', 'SPHardwareDataType'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                output = result.stdout.lower()
                vm_indicators = ['vmware', 'parallels', 'virtualbox']
                
                for vm in vm_indicators:
                    if vm in output:
                        logger.debug(f"VM detected in macOS hardware: {vm}")
                        return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking macOS hardware: {e}")
            return False
    
    def _check_processes(self) -> bool:
        """Проверка запущенных процессов"""
        try:
            import psutil
            
            vm_processes = [
                'vmware', 'vmtoolsd', 'vboxservice', 'vboxtray',
                'qemu', 'xenservice', 'vmicsvc'
            ]
            
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    for vm_proc in vm_processes:
                        if vm_proc in proc_name:
                            logger.debug(f"VM process detected: {proc_name}")
                            return True
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return False
            
        except ImportError:
            logger.debug("psutil not available for process checking")
            return False
        except Exception as e:
            logger.debug(f"Error checking processes: {e}")
            return False
    
    def _check_registry(self) -> bool:
        """Проверка реестра Windows"""
        try:
            if self.platform != 'windows':
                return False
            
            import winreg
            
            vm_registry_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VMware, Inc.\VMware Tools"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Oracle\VirtualBox Guest Additions"),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\ControlSet001\Services\VBoxGuest"),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\ControlSet001\Services\VMTools")
            ]
            
            for hkey, subkey in vm_registry_keys:
                try:
                    winreg.OpenKey(hkey, subkey)
                    logger.debug(f"VM registry key found: {subkey}")
                    return True
                except FileNotFoundError:
                    continue
                except Exception:
                    continue
            
            return False
            
        except ImportError:
            return False
        except Exception as e:
            logger.debug(f"Error checking registry: {e}")
            return False
    
    def _check_files(self) -> bool:
        """Проверка характерных файлов VM"""
        try:
            vm_files = []
            
            if self.platform == 'windows':
                vm_files = [
                    r"C:\Program Files\VMware\VMware Tools",
                    r"C:\Program Files\Oracle\VirtualBox Guest Additions",
                    r"C:\Windows\System32\drivers\vmmouse.sys",
                    r"C:\Windows\System32\drivers\vmhgfs.sys"
                ]
            elif self.platform == 'linux':
                vm_files = [
                    '/usr/bin/vmware-user',
                    '/usr/bin/VBoxClient',
                    '/dev/vmci',
                    '/proc/vz'
                ]
            
            for vm_file in vm_files:
                if os.path.exists(vm_file):
                    logger.debug(f"VM file detected: {vm_file}")
                    return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking files: {e}")
            return False
    
    def _check_network_adapters(self) -> bool:
        """Проверка сетевых адаптеров"""
        try:
            import psutil
            
            vm_mac_prefixes = [
                '00:05:69',  # VMware
                '00:0C:29',  # VMware
                '00:50:56',  # VMware
                '08:00:27',  # VirtualBox
                '00:16:3E',  # Xen
                '00:1C:42'   # Parallels
            ]
            
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:  # MAC address
                        mac = addr.address.upper()
                        
                        for prefix in vm_mac_prefixes:
                            if mac.startswith(prefix.upper()):
                                logger.debug(f"VM MAC prefix detected: {mac} ({prefix})")
                                return True
            
            return False
            
        except ImportError:
            return False
        except Exception as e:
            logger.debug(f"Error checking network adapters: {e}")
            return False
    
    def _check_system_uptime(self) -> bool:
        """Проверка времени работы системы (песочницы часто имеют малое время работы)"""
        try:
            if self.platform == 'windows':
                import ctypes
                uptime_ms = ctypes.windll.kernel32.GetTickCount64()
                uptime_hours = uptime_ms / (1000 * 60 * 60)
            elif self.platform == 'linux':
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    uptime_hours = uptime_seconds / 3600
            else:
                return False
            
            # Если система работает меньше 10 минут - подозрительно
            if uptime_hours < 0.17:  # 10 минут
                logger.debug(f"Suspicious low uptime: {uptime_hours:.2f} hours")
                return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking uptime: {e}")
            return False
    
    def _detect_vm_name_advanced(self) -> Optional[str]:
        """Расширенное определение имени VM"""
        try:
            # Дополнительные проверки для определения конкретной VM
            if self.platform == 'windows':
                # Проверяем службы
                result = subprocess.run(
                    ['sc', 'query', 'type=', 'service'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    services = result.stdout.lower()
                    
                    if 'vmware' in services:
                        return 'VMware'
                    elif 'vbox' in services:
                        return 'VirtualBox'
                    elif 'qemu' in services:
                        return 'QEMU'
            
            return None
            
        except Exception:
            return None
    
    def get_detection_details(self) -> Dict[str, Any]:
        """
        Получение детальной информации о детекции
        
        Returns:
            Dict: Подробности детекции
        """
        details = {
            'is_vm': self.is_virtual_machine(),
            'vm_name': self.get_vm_name(),
            'platform': self.platform,
            'detection_methods': {}
        }
        
        # Выполняем все методы детекции для получения деталей
        for method in self._detection_methods:
            try:
                method_name = method.__name__.replace('_check_', '')
                result = method()
                details['detection_methods'][method_name] = result
            except Exception as e:
                details['detection_methods'][method_name] = f"Error: {e}"
        
        return details

# Глобальный экземпляр детектора VM
vm_detector = VMDetector()

# Удобные функции
def is_running_in_vm() -> bool:
    """Быстрая проверка VM"""
    return vm_detector.is_virtual_machine()

def get_vm_name() -> str:
    """Быстрое получение имени VM"""
    return vm_detector.get_vm_name()

def get_vm_detection_report() -> Dict[str, Any]:
    """Получение полного отчета о детекции VM"""
    return vm_detector.get_detection_details()