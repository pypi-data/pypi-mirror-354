#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/tools/logger.py
======================

Система логирования
"""

import logging
import logging.handlers
import os
from pathlib import Path

def get_logger(name: str):
    """
    Получение настроенного логгера
    
    Args:
        name: Имя логгера (обычно __name__)
        
    Returns:
        logging.Logger: Настроенный логгер
    """
    logger = logging.getLogger(name)
    
    # Избегаем дублирования обработчиков
    if logger.handlers:
        return logger
    
    # Константы логирования (fallback если константы недоступны)
    try:
        LOG_FILE = Path.home() / ".kil0p3" / "protection.log"
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        LOG_LEVEL = "INFO"
        LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
        LOG_BACKUP_COUNT = 5
    except:
        LOG_FILE = Path.home() / ".kil0p3" / "protection.log"
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        LOG_LEVEL = "INFO"
        LOG_MAX_SIZE = 10 * 1024 * 1024
        LOG_BACKUP_COUNT = 5
    
    # Создаем форматтер
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Файловый обработчик с ротацией
    try:
        # Создаем директорию для логов
        LOG_FILE.parent.mkdir(exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_SIZE,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        
    except Exception as e:
        # Если не можем создать файловый логгер, продолжаем без него
        pass
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # В DEV режиме показываем все в консоли
    if os.getenv('KIL0P3_DEV_MODE') == '1':
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.WARNING)  # В продакшене только предупреждения и ошибки
    
    logger.addHandler(console_handler)
    
    # Устанавливаем уровень логирования
    try:
        level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    except:
        level = logging.INFO
    
    logger.setLevel(level)
    
    # Предотвращаем распространение в родительские логгеры
    logger.propagate = False
    
    return logger