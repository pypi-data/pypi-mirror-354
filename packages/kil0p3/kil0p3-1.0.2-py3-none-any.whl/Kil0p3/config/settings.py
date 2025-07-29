#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/config/settings.py
==========================

Менеджер настроек конфигурации
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

from .constants import CONFIG_FILE, DEFAULT_CONFIG

class Settings:
    """Менеджер настроек системы"""
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self._settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Загрузка настроек из файла"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Объединяем с дефолтными настройками
                merged = DEFAULT_CONFIG.copy()
                merged.update(settings)
                return merged
            else:
                # Создаем файл с дефолтными настройками
                self._save_settings(DEFAULT_CONFIG)
                return DEFAULT_CONFIG.copy()
                
        except Exception as e:
            print(f"Settings load error: {e}")
            return DEFAULT_CONFIG.copy()
    
    def _save_settings(self, settings: Dict[str, Any] = None):
        """Сохранение настроек в файл"""
        try:
            if settings is None:
                settings = self._settings
            
            # Создаем директорию если не существует
            self.config_file.parent.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Settings save error: {e}")
    
    def get(self, key: str, default=None):
        """Получение значения настройки"""
        return self._settings.get(key, default)
    
    def set(self, key: str, value):
        """Установка значения настройки"""
        self._settings[key] = value
        self._save_settings()
    
    def update(self, new_settings: Dict[str, Any]):
        """Обновление нескольких настроек"""
        self._settings.update(new_settings)
        self._save_settings()
    
    def reset_to_defaults(self):
        """Сброс к настройкам по умолчанию"""
        self._settings = DEFAULT_CONFIG.copy()
        self._save_settings()
    
    def get_all(self) -> Dict[str, Any]:
        """Получение всех настроек"""
        return self._settings.copy()

# Глобальный экземпляр настроек
settings = Settings()