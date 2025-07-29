#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/core/trial.py
====================

Менеджер триального периода
"""

import os
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

# Импорт констант
try:
    from ..config.constants import APP_DATA_DIR
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback если модули недоступны
    APP_DATA_DIR = Path.home() / ".kil0p3"
    
    import logging
    logger = logging.getLogger(__name__)

class TrialManager:
    """Менеджер триального периода"""
    
    def __init__(self, trial_duration_seconds: int = 30):
        self.trial_duration = trial_duration_seconds
        self.trial_file = APP_DATA_DIR / "trial.dat"
        self._trial_data = None
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Создание файла триала если не существует"""
        try:
            # Создаем директорию
            self.trial_file.parent.mkdir(exist_ok=True)
            
            if not self.trial_file.exists():
                # Создаем новый триал
                self._create_new_trial()
                
        except Exception as e:
            logger.error(f"Failed to create trial file: {e}")
    
    def _create_new_trial(self):
        """Создание нового триального периода"""
        try:
            trial_data = {
                'started_at': datetime.now().isoformat(),
                'duration_seconds': self.trial_duration,
                'first_run': True,
                'usage_count': 0,
                'last_access': datetime.now().isoformat(),
                'created': datetime.now().isoformat(),
                'hwid': self._get_current_hwid()
            }
            
            self._save_trial_data(trial_data)
            self._trial_data = trial_data
            
            logger.info(f"New trial period created: {self.trial_duration} seconds")
            
        except Exception as e:
            logger.error(f"Failed to create new trial: {e}")
    
    def _load_trial_data(self) -> Dict[str, Any]:
        """Загрузка данных триала"""
        try:
            if self.trial_file.exists():
                with open(self.trial_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Проверяем HWID
                current_hwid = self._get_current_hwid()
                if data.get('hwid') != current_hwid:
                    logger.warning("HWID mismatch - creating new trial")
                    self._create_new_trial()
                    return self._trial_data
                
                return data
            else:
                self._create_new_trial()
                return self._trial_data
                
        except Exception as e:
            logger.error(f"Failed to load trial data: {e}")
            self._create_new_trial()
            return self._trial_data
    
    def _save_trial_data(self, data: Dict[str, Any]):
        """Сохранение данных триала"""
        try:
            # Создаем директорию если не существует
            self.trial_file.parent.mkdir(exist_ok=True)
            
            with open(self.trial_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # На Windows делаем файл скрытым
            if os.name == 'nt':
                try:
                    os.system(f'attrib +h "{self.trial_file}"')
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Failed to save trial data: {e}")
    
    def _get_current_hwid(self) -> str:
        """Получение текущего HWID"""
        try:
            from ..core.hwid import hwid_generator
            return hwid_generator.generate()
        except:
            return "unknown_hwid"
    
    def start_trial_session(self) -> bool:
        """
        Запуск триальной сессии
        
        Returns:
            bool: True если триал активен, False если истек
        """
        try:
            # Загружаем данные триала
            trial_data = self._load_trial_data()
            
            # Проверяем не истек ли триал
            if self.is_trial_expired():
                logger.warning("Trial period expired")
                return False
            
            # Обновляем статистику использования
            trial_data['usage_count'] = trial_data.get('usage_count', 0) + 1
            trial_data['last_access'] = datetime.now().isoformat()
            trial_data['first_run'] = False
            
            self._save_trial_data(trial_data)
            self._trial_data = trial_data
            
            remaining = self.get_remaining_time()
            logger.info(f"Trial session started - {remaining:.1f}s remaining")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start trial session: {e}")
            return False
    
    def is_trial_expired(self) -> bool:
        """
        Проверка истечения триального периода
        
        Returns:
            bool: True если триал истек
        """
        try:
            trial_data = self._load_trial_data()
            
            start_time = datetime.fromisoformat(trial_data['started_at'])
            duration = trial_data['duration_seconds']
            
            elapsed = (datetime.now() - start_time).total_seconds()
            expired = elapsed >= duration
            
            if expired:
                logger.info(f"Trial expired: {elapsed:.1f}s >= {duration}s")
            
            return expired
            
        except Exception as e:
            logger.error(f"Error checking trial expiration: {e}")
            return True  # В случае ошибки считаем что истек
    
    def get_remaining_time(self) -> float:
        """
        Получение оставшегося времени триала
        
        Returns:
            float: Оставшееся время в секундах
        """
        try:
            trial_data = self._load_trial_data()
            
            start_time = datetime.fromisoformat(trial_data['started_at'])
            duration = trial_data['duration_seconds']
            
            elapsed = (datetime.now() - start_time).total_seconds()
            remaining = max(0, duration - elapsed)
            
            return remaining
            
        except Exception as e:
            logger.error(f"Error getting remaining time: {e}")
            return 0.0
    
    def get_trial_info(self) -> Dict[str, Any]:
        """
        Получение полной информации о триале
        
        Returns:
            Dict: Информация о триальном периоде
        """
        try:
            trial_data = self._load_trial_data()
            
            start_time = datetime.fromisoformat(trial_data['started_at'])
            duration = trial_data['duration_seconds']
            elapsed = (datetime.now() - start_time).total_seconds()
            remaining = max(0, duration - elapsed)
            
            return {
                'is_trial': True,
                'started_at': trial_data['started_at'],
                'duration_seconds': duration,
                'elapsed_seconds': elapsed,
                'remaining_seconds': remaining,
                'remaining_percent': (remaining / duration) * 100 if duration > 0 else 0,
                'is_expired': remaining <= 0,
                'usage_count': trial_data.get('usage_count', 0),
                'last_access': trial_data.get('last_access'),
                'hwid': trial_data.get('hwid', 'unknown')[:8] + '...'
            }
            
        except Exception as e:
            logger.error(f"Error getting trial info: {e}")
            return {
                'is_trial': True,
                'is_expired': True,
                'error': str(e)
            }
    
    def reset_trial(self):
        """Сброс триального периода (только для DEV режима)"""
        try:
            if os.getenv('KIL0P3_DEV_MODE') == '1':
                if self.trial_file.exists():
                    os.remove(self.trial_file)
                    logger.info("Trial period reset (DEV MODE)")
                    self._create_new_trial()
                else:
                    logger.info("No trial file to reset")
            else:
                logger.warning("Trial reset denied - not in DEV mode")
                
        except Exception as e:
            logger.error(f"Failed to reset trial: {e}")
    
    def check_continuous_usage(self) -> bool:
        """
        Проверка на непрерывное использование триала
        Блокирует если приложение работает дольше триального периода
        
        Returns:
            bool: True если использование допустимо
        """
        try:
            if self.is_trial_expired():
                return False
            
            # Дополнительная проверка на манипуляции со временем
            trial_data = self._load_trial_data()
            last_access = trial_data.get('last_access')
            
            if last_access:
                last_time = datetime.fromisoformat(last_access)
                current_time = datetime.now()
                
                # Если время пошло назад - подозрительно
                if current_time < last_time:
                    logger.warning("Time manipulation detected in trial")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in continuous usage check: {e}")
            return False

# Глобальный экземпляр менеджера триала
trial_manager = TrialManager()

# Удобные функции
def start_trial() -> bool:
    """Быстрый запуск триала"""
    return trial_manager.start_trial_session()

def is_trial_active() -> bool:
    """Быстрая проверка активности триала"""
    return not trial_manager.is_trial_expired()

def get_trial_time_remaining() -> float:
    """Быстрое получение оставшегося времени"""
    return trial_manager.get_remaining_time()

def get_trial_status() -> Dict[str, Any]:
    """Быстрое получение статуса триала"""
    return trial_manager.get_trial_info()

def reset_trial_period():
    """Быстрый сброс триала (только DEV режим)"""
    trial_manager.reset_trial()