#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/security/anti_debug.py
=============================

Система защиты от отладки
"""

import sys
import os
import threading
import time
from typing import List, Optional

# Импорт констант
try:
    from ..config.constants import DEBUG_ARTIFACTS, FORBIDDEN_PROCESSES
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback если модули недоступны
    DEBUG_ARTIFACTS = ['pdb', 'pydevd', 'debugpy']
    FORBIDDEN_PROCESSES = ['ida.exe', 'x32dbg.exe', 'ollydbg.exe']
    
    import logging
    logger = logging.getLogger(__name__)

class AntiDebug:
    """Система защиты от отладки"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.check_interval = 1.0  # Проверка каждую секунду
        self._detection_callbacks = []
    
    def start_monitoring(self):
        """Запуск мониторинга отладчиков"""
        try:
            if self.monitoring:
                logger.debug("Anti-debug monitoring already running")
                return
            
            self.monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                daemon=True,
                name="AntiDebugMonitor"
            )
            self.monitor_thread.start()
            
            logger.info("Anti-debug monitoring started")
            
        except Exception as e:
            logger.error(f"Failed to start anti-debug monitoring: {e}")
            self.monitoring = False
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        try:
            if not self.monitoring:
                return
            
            self.monitoring = False
            
            if self.monitor_thread and self.monitor_thread.is_alive():
                # Ждем завершения потока
                self.monitor_thread.join(timeout=2.0)
            
            logger.info("Anti-debug monitoring stopped")
            
        except Exception as e:
            logger.error(f"Error stopping anti-debug monitoring: {e}")
    
    def _monitor_loop(self):
        """Основной цикл мониторинга"""
        logger.debug("Anti-debug monitor loop started")
        
        while self.monitoring:
            try:
                if self.is_debugger_present():
                    logger.critical("DEBUGGER DETECTED!")
                    self._handle_debugger_detection()
                    break
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in anti-debug monitor loop: {e}")
                time.sleep(5.0)  # Увеличиваем интервал при ошибке
        
        logger.debug("Anti-debug monitor loop ended")
    
    def is_debugger_present(self) -> bool:
        """
        Комплексная проверка наличия отладчика
        
        Returns:
            bool: True если обнаружен отладчик
        """
        try:
            # 1. Проверка модулей отладки в sys.modules
            if self._check_debug_modules():
                return True
            
            # 2. Проверка запущенных процессов
            if self._check_forbidden_processes():
                return True
            
            # 3. Проверка трассировки Python
            if self._check_trace_function():
                return True
            
            # 4. Проверка переменных окружения
            if self._check_debug_environment():
                return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error in debugger detection: {e}")
            return False
    
    def _check_debug_modules(self) -> bool:
        """Проверка загруженных модулей отладки"""
        try:
            for debug_module in DEBUG_ARTIFACTS:
                if debug_module in sys.modules:
                    logger.warning(f"Debug module detected: {debug_module}")
                    return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking debug modules: {e}")
            return False
    
    def _check_forbidden_processes(self) -> bool:
        """Проверка запрещенных процессов"""
        try:
            import psutil
            
            # Получаем список всех процессов
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    # Проверяем против списка запрещенных
                    for forbidden in FORBIDDEN_PROCESSES:
                        if forbidden.lower() in proc_name:
                            logger.warning(f"Forbidden process detected: {proc_name} (PID: {proc.info['pid']})")
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
    
    def _check_trace_function(self) -> bool:
        """Проверка функции трассировки Python"""
        try:
            # Проверяем установлена ли функция трассировки
            if sys.gettrace() is not None:
                logger.warning("Python trace function detected")
                return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking trace function: {e}")
            return False
    
    def _check_debug_environment(self) -> bool:
        """Проверка переменных окружения"""
        try:
            debug_vars = [
                'PYTHONBREAKPOINT',
                'PYDEBUG',
                'PYTHONDEBUG'
            ]
            
            for var in debug_vars:
                if os.environ.get(var):
                    logger.warning(f"Debug environment variable detected: {var}")
                    return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking environment: {e}")
            return False
    
    def _handle_debugger_detection(self):
        """Обработка обнаружения отладчика"""
        try:
            # Останавливаем мониторинг
            self.monitoring = False
            
            # Вызываем все зарегистрированные callbacks
            for callback in self._detection_callbacks:
                try:
                    callback("Debugger detected")
                except Exception as e:
                    logger.error(f"Error in detection callback: {e}")
            
            # Если нет callbacks, выполняем стандартные действия
            if not self._detection_callbacks:
                self._default_detection_action()
            
        except Exception as e:
            logger.error(f"Error handling debugger detection: {e}")
    
    def _default_detection_action(self):
        """Стандартные действия при обнаружении отладчика"""
        try:
            # Добавляем нарушение в блок-лист
            from ..runtime.block_state import block_state
            block_state.add_violation("Debugger detected", "critical")
            
            # В DEV режиме только предупреждаем
            if os.getenv('KIL0P3_DEV_MODE') == '1':
                logger.warning("DEV MODE: Debugger detection ignored")
                return
            
            # В продакшене блокируем и завершаем
            block_state.block_device("Debugger detected during runtime")
            
            logger.critical("Application terminating due to debugger detection")
            sys.exit(1)
            
        except Exception as e:
            logger.error(f"Error in default detection action: {e}")
            sys.exit(1)
    
    def add_detection_callback(self, callback):
        """
        Добавление callback для обнаружения отладчика
        
        Args:
            callback: Функция, вызываемая при обнаружении (принимает reason: str)
        """
        if callable(callback):
            self._detection_callbacks.append(callback)
            logger.debug("Detection callback added")
    
    def remove_detection_callback(self, callback):
        """Удаление callback"""
        try:
            self._detection_callbacks.remove(callback)
            logger.debug("Detection callback removed")
        except ValueError:
            pass
    
    def perform_single_check(self) -> bool:
        """
        Одиночная проверка без запуска мониторинга
        
        Returns:
            bool: True если обнаружен отладчик
        """
        return self.is_debugger_present()
    
    def get_status(self) -> dict:
        """
        Получение статуса анти-отладки
        
        Returns:
            dict: Информация о состоянии
        """
        return {
            'monitoring_active': self.monitoring,
            'check_interval': self.check_interval,
            'callbacks_count': len(self._detection_callbacks),
            'thread_alive': self.monitor_thread.is_alive() if self.monitor_thread else False,
            'debugger_present': self.is_debugger_present()
        }

# Глобальный экземпляр анти-отладки
anti_debug = AntiDebug()

# Удобные функции
def start_anti_debug_monitoring():
    """Быстрый запуск мониторинга"""
    anti_debug.start_monitoring()

def stop_anti_debug_monitoring():
    """Быстрая остановка мониторинга"""
    anti_debug.stop_monitoring()

def check_for_debugger() -> bool:
    """Быстрая проверка отладчика"""
    return anti_debug.is_debugger_present()

def is_monitoring_active() -> bool:
    """Проверка активности мониторинга"""
    return anti_debug.monitoring