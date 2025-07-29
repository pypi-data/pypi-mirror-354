#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/runtime/attempt_counter.py
==================================

Счетчик попыток активации лицензии
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Импорт констант
try:
    from ..config.constants import ATTEMPT_FILE, MAX_ACTIVATION_ATTEMPTS, ATTEMPT_RESET_HOURS
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback если модули недоступны
    ATTEMPT_FILE = Path.home() / ".kil0p3" / "attempts.dat"
    MAX_ACTIVATION_ATTEMPTS = 3
    ATTEMPT_RESET_HOURS = 24
    
    import logging
    logger = logging.getLogger(__name__)

class AttemptCounter:
    """Счетчик попыток активации с автосбросом"""
    
    def __init__(self):
        self.attempts_file = ATTEMPT_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Создание файла счетчика если не существует"""
        try:
            if not self.attempts_file.exists():
                # Создаем директорию
                self.attempts_file.parent.mkdir(exist_ok=True)
                
                # Создаем файл с начальными данными
                initial_data = {
                    'attempts': 0,
                    'first_attempt': None,
                    'last_attempt': None,
                    'reset_time': None,
                    'created': datetime.now().isoformat()
                }
                self._save_data(initial_data)
                
        except Exception as e:
            logger.error(f"Failed to create attempts file: {e}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Загрузка данных о попытках"""
        try:
            if self.attempts_file.exists():
                with open(self.attempts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Проверяем нужен ли автосброс
                if self._should_auto_reset(data):
                    logger.info("Auto-resetting attempt counter due to time threshold")
                    data = self._reset_data()
                    self._save_data(data)
                
                return data
            else:
                # Файл не существует, создаем новый
                return self._reset_data()
                
        except Exception as e:
            logger.error(f"Failed to load attempts data: {e}")
            # Возвращаем безопасные значения по умолчанию
            return self._reset_data()
    
    def _save_data(self, data: Dict[str, Any]):
        """Сохранение данных о попытках"""
        try:
            # Создаем директорию если не существует
            self.attempts_file.parent.mkdir(exist_ok=True)
            
            with open(self.attempts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # На Windows делаем файл скрытым
            if os.name == 'nt':
                try:
                    os.system(f'attrib +h "{self.attempts_file}"')
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Failed to save attempts data: {e}")
    
    def _reset_data(self) -> Dict[str, Any]:
        """Создание данных для сброса"""
        return {
            'attempts': 0,
            'first_attempt': None,
            'last_attempt': None,
            'reset_time': datetime.now().isoformat(),
            'created': datetime.now().isoformat()
        }
    
    def _should_auto_reset(self, data: Dict[str, Any]) -> bool:
        """Проверка необходимости автоматического сброса"""
        try:
            last_attempt = data.get('last_attempt')
            if not last_attempt:
                return False
            
            # Парсим время последней попытки
            last_time = datetime.fromisoformat(last_attempt)
            
            # Вычисляем время для сброса
            reset_threshold = datetime.now() - timedelta(hours=ATTEMPT_RESET_HOURS)
            
            # Если последняя попытка была давно - сбрасываем
            should_reset = last_time < reset_threshold
            
            if should_reset:
                logger.info(f"Attempt counter will be reset - last attempt was {last_time}")
            
            return should_reset
            
        except Exception as e:
            logger.debug(f"Error checking auto-reset: {e}")
            return False
    
    def get_attempts(self) -> int:
        """
        Получение текущего количества попыток
        
        Returns:
            int: Количество попыток активации
        """
        data = self._load_data()
        return data.get('attempts', 0)
    
    def increment(self) -> int:
        """
        Увеличение счетчика попыток
        
        Returns:
            int: Новое количество попыток
        """
        try:
            data = self._load_data()
            
            # Увеличиваем счетчик
            current_attempts = data.get('attempts', 0)
            new_attempts = current_attempts + 1
            
            # Обновляем данные
            data['attempts'] = new_attempts
            data['last_attempt'] = datetime.now().isoformat()
            
            # Устанавливаем время первой попытки если это первая попытка
            if current_attempts == 0:
                data['first_attempt'] = data['last_attempt']
            
            # Сохраняем
            self._save_data(data)
            
            logger.warning(f"Activation attempt #{new_attempts}/{MAX_ACTIVATION_ATTEMPTS}")
            
            return new_attempts
            
        except Exception as e:
            logger.error(f"Failed to increment attempts: {e}")
            return 0
    
    def reset(self):
        """Принудительный сброс счетчика попыток"""
        try:
            data = self._reset_data()
            self._save_data(data)
            
            logger.info("Attempt counter manually reset")
            
        except Exception as e:
            logger.error(f"Failed to reset attempts: {e}")
    
    def is_limit_exceeded(self) -> bool:
        """
        Проверка превышения лимита попыток
        
        Returns:
            bool: True если лимит превышен
        """
        attempts = self.get_attempts()
        exceeded = attempts >= MAX_ACTIVATION_ATTEMPTS
        
        if exceeded:
            logger.warning(f"Attempt limit exceeded: {attempts}/{MAX_ACTIVATION_ATTEMPTS}")
        
        return exceeded
    
    def get_remaining_attempts(self) -> int:
        """
        Получение количества оставшихся попыток
        
        Returns:
            int: Количество оставшихся попыток (минимум 0)
        """
        attempts = self.get_attempts()
        remaining = max(0, MAX_ACTIVATION_ATTEMPTS - attempts)
        return remaining
    
    def get_detailed_info(self) -> Dict[str, Any]:
        """
        Получение подробной информации о попытках
        
        Returns:
            Dict: Подробная информация
        """
        data = self._load_data()
        attempts = data.get('attempts', 0)
        
        return {
            'current_attempts': attempts,
            'max_attempts': MAX_ACTIVATION_ATTEMPTS,
            'remaining_attempts': self.get_remaining_attempts(),
            'limit_exceeded': self.is_limit_exceeded(),
            'first_attempt': data.get('first_attempt'),
            'last_attempt': data.get('last_attempt'),
            'reset_time': data.get('reset_time'),
            'created': data.get('created'),
            'auto_reset_hours': ATTEMPT_RESET_HOURS,
            'file_path': str(self.attempts_file)
        }

# Глобальный экземпляр счетчика
attempt_counter = AttemptCounter()

# Удобные функции
def get_current_attempts() -> int:
    """Быстрое получение текущих попыток"""
    return attempt_counter.get_attempts()

def increment_attempts() -> int:
    """Быстрое увеличение счетчика"""
    return attempt_counter.increment()

def reset_attempts():
    """Быстрый сброс счетчика"""
    attempt_counter.reset()

def is_attempts_limit_exceeded() -> bool:
    """Быстрая проверка лимита"""
    return attempt_counter.is_limit_exceeded()