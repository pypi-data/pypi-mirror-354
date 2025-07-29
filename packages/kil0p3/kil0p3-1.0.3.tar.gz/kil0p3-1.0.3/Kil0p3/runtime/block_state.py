#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/runtime/block_state.py
==============================

Управление состоянием блокировки устройства
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

# Импорт констант
try:
    from ..config.constants import BLOCK_FILE, BLOCK_DURATION_HOURS
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback если модули недоступны
    BLOCK_FILE = Path.home() / ".kil0p3" / "blocked.dat"
    BLOCK_DURATION_HOURS = 72
    
    import logging
    logger = logging.getLogger(__name__)

class BlockState:
    """Управление состоянием блокировки устройства"""
    
    def __init__(self):
        self.block_file = BLOCK_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Создание файла блокировки если не существует"""
        try:
            if not self.block_file.exists():
                # Создаем директорию
                self.block_file.parent.mkdir(exist_ok=True)
                
                # Создаем файл с начальными данными
                initial_data = {
                    'is_blocked': False,
                    'block_reason': None,
                    'block_time': None,
                    'unblock_time': None,
                    'violations': [],
                    'block_duration_hours': BLOCK_DURATION_HOURS,
                    'created': datetime.now().isoformat()
                }
                self._save_data(initial_data)
                
        except Exception as e:
            logger.error(f"Failed to create block file: {e}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Загрузка данных о блокировке"""
        try:
            if self.block_file.exists():
                with open(self.block_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Проверяем автоснятие блокировки
                if self._should_auto_unblock(data):
                    logger.info("Auto-unblocking device due to time expiration")
                    data = self._unblock_data(data)
                    self._save_data(data)
                
                return data
            else:
                # Файл не существует, создаем новый
                return self._create_initial_data()
                
        except Exception as e:
            logger.error(f"Failed to load block data: {e}")
            # Возвращаем безопасные значения
            return self._create_initial_data()
    
    def _save_data(self, data: Dict[str, Any]):
        """Сохранение данных о блокировке"""
        try:
            # Создаем директорию если не существует
            self.block_file.parent.mkdir(exist_ok=True)
            
            with open(self.block_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # На Windows делаем файл скрытым и системным
            if os.name == 'nt':
                try:
                    os.system(f'attrib +h +s "{self.block_file}"')
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Failed to save block data: {e}")
    
    def _create_initial_data(self) -> Dict[str, Any]:
        """Создание начальных данных"""
        return {
            'is_blocked': False,
            'block_reason': None,
            'block_time': None,
            'unblock_time': None,
            'violations': [],
            'block_duration_hours': BLOCK_DURATION_HOURS,
            'created': datetime.now().isoformat()
        }
    
    def _unblock_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Данные для разблокировки"""
        data['is_blocked'] = False
        data['block_reason'] = None
        data['unblock_time'] = datetime.now().isoformat()
        return data
    
    def _should_auto_unblock(self, data: Dict[str, Any]) -> bool:
        """Проверка необходимости автоматической разблокировки"""
        try:
            # Если не заблокировано - не нужно разблокировать
            if not data.get('is_blocked', False):
                return False
            
            block_time = data.get('block_time')
            if not block_time:
                return False
            
            # Парсим время блокировки
            block_datetime = datetime.fromisoformat(block_time)
            
            # Получаем продолжительность блокировки
            block_duration = data.get('block_duration_hours', BLOCK_DURATION_HOURS)
            
            # Вычисляем время разблокировки
            unblock_datetime = block_datetime + timedelta(hours=block_duration)
            
            # Проверяем истекло ли время блокировки
            should_unblock = datetime.now() > unblock_datetime
            
            if should_unblock:
                logger.info(f"Block expired - blocked at {block_datetime}, duration {block_duration}h")
            
            return should_unblock
            
        except Exception as e:
            logger.debug(f"Error checking auto-unblock: {e}")
            return False
    
    def _get_current_hwid(self) -> str:
        """Получение текущего HWID"""
        try:
            from ..core.hwid import hwid_generator
            return hwid_generator.generate()
        except:
            return "unknown_hwid"
    
    def is_blocked(self) -> bool:
        """
        Проверка состояния блокировки
        
        Returns:
            bool: True если устройство заблокировано
        """
        data = self._load_data()
        blocked = data.get('is_blocked', False)
        
        if blocked:
            logger.debug("Device is currently blocked")
        
        return blocked
    
    def block_device(self, reason: str, duration_hours: Optional[int] = None):
        """
        Блокировка устройства
        
        Args:
            reason: Причина блокировки
            duration_hours: Продолжительность блокировки в часах (опционально)
        """
        try:
            data = self._load_data()
            
            # Устанавливаем блокировку
            data['is_blocked'] = True
            data['block_reason'] = reason
            data['block_time'] = datetime.now().isoformat()
            data['unblock_time'] = None
            
            # Устанавливаем продолжительность
            if duration_hours:
                data['block_duration_hours'] = duration_hours
            
            # Добавляем запись о нарушении
            violation = {
                'reason': reason,
                'timestamp': data['block_time'],
                'hwid': self._get_current_hwid(),
                'severity': 'critical'
            }
            
            violations = data.get('violations', [])
            violations.append(violation)
            data['violations'] = violations
            
            # Сохраняем
            self._save_data(data)
            
            duration = data.get('block_duration_hours', BLOCK_DURATION_HOURS)
            logger.critical(f"Device blocked for {duration}h: {reason}")
            
        except Exception as e:
            logger.error(f"Failed to block device: {e}")
    
    def unblock_device(self, manual: bool = True):
        """
        Разблокировка устройства
        
        Args:
            manual: True если разблокировка ручная, False если автоматическая
        """
        try:
            data = self._load_data()
            
            if not data.get('is_blocked', False):
                logger.info("Device is not blocked")
                return
            
            # Разблокировка
            data = self._unblock_data(data)
            
            # Записываем кто разблокировал
            if manual:
                data['unblock_method'] = 'manual'
                logger.info("Device manually unblocked")
            else:
                data['unblock_method'] = 'automatic'
                logger.info("Device automatically unblocked")
            
            self._save_data(data)
            
        except Exception as e:
            logger.error(f"Failed to unblock device: {e}")
    
    def add_violation(self, reason: str, severity: str = 'warning'):
        """
        Добавление нарушения без немедленной блокировки
        
        Args:
            reason: Причина нарушения
            severity: Уровень серьезности ('warning', 'critical')
        """
        try:
            data = self._load_data()
            
            # Создаем запись о нарушении
            violation = {
                'reason': reason,
                'timestamp': datetime.now().isoformat(),
                'hwid': self._get_current_hwid(),
                'severity': severity
            }
            
            violations = data.get('violations', [])
            violations.append(violation)
            data['violations'] = violations
            
            # Проверяем накопление нарушений
            recent_violations = self._count_recent_violations(violations)
            
            # Автоблокировка при накоплении критических нарушений
            if severity == 'critical' or recent_violations >= 5:
                data['is_blocked'] = True
                data['block_reason'] = f"Multiple violations ({recent_violations} recent violations)"
                data['block_time'] = datetime.now().isoformat()
                
                logger.critical(f"Device auto-blocked due to {recent_violations} violations")
            
            self._save_data(data)
            
            if severity == 'critical':
                logger.warning(f"Critical violation recorded: {reason}")
            else:
                logger.info(f"Violation recorded: {reason}")
            
        except Exception as e:
            logger.error(f"Failed to add violation: {e}")
    
    def _count_recent_violations(self, violations: List[Dict]) -> int:
        """Подсчет недавних нарушений (за последние 24 часа)"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=24)
            recent_count = 0
            
            for violation in violations:
                try:
                    violation_time = datetime.fromisoformat(violation['timestamp'])
                    if violation_time > cutoff_time:
                        recent_count += 1
                except:
                    continue
            
            return recent_count
            
        except Exception:
            return 0
    
    def get_block_info(self) -> Dict[str, Any]:
        """
        Получение подробной информации о блокировке
        
        Returns:
            Dict: Информация о состоянии блокировки
        """
        data = self._load_data()
        
        block_info = {
            'is_blocked': data.get('is_blocked', False),
            'reason': data.get('block_reason'),
            'block_time': data.get('block_time'),
            'unblock_time': data.get('unblock_time'),
            'unblock_method': data.get('unblock_method'),
            'violations_count': len(data.get('violations', [])),
            'block_duration_hours': data.get('block_duration_hours', BLOCK_DURATION_HOURS),
            'created': data.get('created')
        }
        
        # Вычисляем время до разблокировки
        if block_info['is_blocked'] and block_info['block_time']:
            try:
                block_datetime = datetime.fromisoformat(block_info['block_time'])
                duration_hours = block_info['block_duration_hours']
                unblock_datetime = block_datetime + timedelta(hours=duration_hours)
                
                now = datetime.now()
                if now < unblock_datetime:
                    remaining_seconds = (unblock_datetime - now).total_seconds()
                    block_info['remaining_hours'] = remaining_seconds / 3600
                    block_info['unblock_at'] = unblock_datetime.isoformat()
                else:
                    block_info['remaining_hours'] = 0
                    block_info['unblock_at'] = "expired"
            except:
                block_info['remaining_hours'] = 0
                block_info['unblock_at'] = "unknown"
        
        return block_info
    
    def get_violations(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Получение списка нарушений
        
        Args:
            limit: Максимальное количество нарушений (None = все)
            
        Returns:
            List: Список нарушений (новые сначала)
        """
        data = self._load_data()
        violations = data.get('violations', [])
        
        # Сортируем по времени (новые сначала)
        violations.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        if limit:
            violations = violations[:limit]
        
        return violations
    
    def clear_violations(self):
        """Очистка всех нарушений"""
        try:
            data = self._load_data()
            data['violations'] = []
            self._save_data(data)
            
            logger.info("All violations cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear violations: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики нарушений и блокировок
        
        Returns:
            Dict: Статистика
        """
        data = self._load_data()
        violations = data.get('violations', [])
        
        # Подсчитываем статистику
        total_violations = len(violations)
        critical_violations = sum(1 for v in violations if v.get('severity') == 'critical')
        warning_violations = total_violations - critical_violations
        
        recent_violations = self._count_recent_violations(violations)
        
        return {
            'total_violations': total_violations,
            'critical_violations': critical_violations,
            'warning_violations': warning_violations,
            'recent_violations_24h': recent_violations,
            'currently_blocked': data.get('is_blocked', False),
            'block_count': 1 if data.get('block_time') else 0,
            'file_size_bytes': self.block_file.stat().st_size if self.block_file.exists() else 0,
            'created': data.get('created'),
            'last_violation': violations[0]['timestamp'] if violations else None
        }

# Глобальный экземпляр состояния блокировки
block_state = BlockState()

# Удобные функции
def is_device_blocked() -> bool:
    """Быстрая проверка блокировки"""
    return block_state.is_blocked()

def block_device(reason: str, duration_hours: int = None):
    """Быстрая блокировка устройства"""
    block_state.block_device(reason, duration_hours)

def unblock_device():
    """Быстрая разблокировка устройства"""
    block_state.unblock_device()

def add_security_violation(reason: str, severity: str = 'warning'):
    """Быстрое добавление нарушения"""
    block_state.add_violation(reason, severity)

def get_block_status() -> Dict[str, Any]:
    """Быстрое получение статуса блокировки"""
    return block_state.get_block_info()