# ============================================================================
# 1. Исправление в Kil0p3/core/trial.py
# ============================================================================

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
import tempfile
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
    
    def __init__(self, trial_duration_seconds: int = 60):
        self.trial_duration = trial_duration_seconds
        
        # Попробуем создать файл в разных местах
        self.trial_file = self._get_trial_file_path()
        self._trial_data = None
        self._start_time = None
        self._ensure_file_exists()
    
    def _get_trial_file_path(self) -> Path:
        """Получение безопасного пути для файла триала"""
        try:
            # Сначала пробуем стандартную папку
            trial_dir = APP_DATA_DIR
            trial_dir.mkdir(exist_ok=True)
            
            trial_file = trial_dir / "trial.dat"
            
            # Проверяем можем ли мы писать
            test_file = trial_dir / "test_write.tmp"
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                logger.debug(f"Using trial file: {trial_file}")
                return trial_file
            except PermissionError:
                logger.warning(f"No write permission to {trial_dir}")
        except Exception as e:
            logger.debug(f"Error with standard directory: {e}")
        
        # Fallback 1: Временная папка
        try:
            temp_dir = Path(tempfile.gettempdir()) / ".kil0p3"
            temp_dir.mkdir(exist_ok=True)
            trial_file = temp_dir / "trial.dat"
            logger.debug(f"Using temp trial file: {trial_file}")
            return trial_file
        except:
            pass
        
        # Fallback 2: Папка с приложением
        try:
            app_dir = Path(__file__).parent.parent.parent / ".kil0p3"
            app_dir.mkdir(exist_ok=True)
            trial_file = app_dir / "trial.dat"
            logger.debug(f"Using app dir trial file: {trial_file}")
            return trial_file
        except:
            pass
        
        # Fallback 3: В памяти (не сохраняется)
        logger.warning("Using in-memory trial (not persistent)")
        return None
    
    def _ensure_file_exists(self):
        """Создание файла триала если не существует"""
        try:
            if self.trial_file is None:
                # В памяти
                self._create_new_trial()
                return
                
            if not self.trial_file.exists():
                # Создаем новый триал
                self._create_new_trial()
                
        except Exception as e:
            logger.error(f"Failed to create trial file: {e}")
            # Переключаемся на режим в памяти
            self.trial_file = None
            self._create_new_trial()
    
    def _create_new_trial(self):
        """Создание нового триального периода"""
        try:
            self._start_time = time.time()
            
            trial_data = {
                'started_at': datetime.now().isoformat(),
                'duration_seconds': self.trial_duration,
                'first_run': True,
                'usage_count': 0,
                'last_access': datetime.now().isoformat(),
                'created': datetime.now().isoformat(),
                'hwid': self._get_current_hwid(),
                'start_timestamp': self._start_time  # Добавляем timestamp для точности
            }
            
            self._save_trial_data(trial_data)
            self._trial_data = trial_data
            
            logger.info(f"New trial period created: {self.trial_duration} seconds")
            
        except Exception as e:
            logger.error(f"Failed to create new trial: {e}")
            # Минимальные данные в памяти
            self._trial_data = {
                'started_at': datetime.now().isoformat(),
                'duration_seconds': self.trial_duration,
                'start_timestamp': time.time(),
                'hwid': self._get_current_hwid()
            }
    
    def _load_trial_data(self) -> Dict[str, Any]:
        """Загрузка данных триала"""
        try:
            if self.trial_file is None or not self.trial_file.exists():
                if self._trial_data is None:
                    self._create_new_trial()
                return self._trial_data
            
            with open(self.trial_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Проверяем HWID
            current_hwid = self._get_current_hwid()
            if data.get('hwid') != current_hwid:
                logger.warning("HWID mismatch - creating new trial")
                self._create_new_trial()
                return self._trial_data
            
            return data
                
        except Exception as e:
            logger.error(f"Failed to load trial data: {e}")
            if self._trial_data is None:
                self._create_new_trial()
            return self._trial_data
    
    def _save_trial_data(self, data: Dict[str, Any]):
        """Сохранение данных триала"""
        try:
            if self.trial_file is None:
                # Только в памяти
                self._trial_data = data
                return
                
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
            logger.debug(f"Failed to save trial data: {e}")
            # Сохраняем в памяти
            self._trial_data = data
    
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
            
            # Устанавливаем время начала если его нет
            if not hasattr(self, '_start_time') or self._start_time is None:
                self._start_time = trial_data.get('start_timestamp', time.time())
            
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
            if not hasattr(self, '_start_time') or self._start_time is None:
                trial_data = self._load_trial_data()
                self._start_time = trial_data.get('start_timestamp')
                
                if self._start_time is None:
                    # Используем время из ISO строки
                    start_time_str = trial_data.get('started_at')
                    if start_time_str:
                        start_time = datetime.fromisoformat(start_time_str)
                        self._start_time = start_time.timestamp()
                    else:
                        self._start_time = time.time()
            
            # Используем реальное время для точности
            elapsed = time.time() - self._start_time
            expired = elapsed >= self.trial_duration
            
            if expired:
                logger.info(f"Trial expired: {elapsed:.1f}s >= {self.trial_duration}s")
            
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
            if not hasattr(self, '_start_time') or self._start_time is None:
                trial_data = self._load_trial_data()
                self._start_time = trial_data.get('start_timestamp', time.time())
            
            elapsed = time.time() - self._start_time
            remaining = max(0, self.trial_duration - elapsed)
            
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
            
            if not hasattr(self, '_start_time') or self._start_time is None:
                self._start_time = trial_data.get('start_timestamp', time.time())
            
            elapsed = time.time() - self._start_time
            remaining = max(0, self.trial_duration - elapsed)
            
            return {
                'is_trial': True,
                'started_at': trial_data.get('started_at'),
                'duration_seconds': self.trial_duration,
                'elapsed_seconds': elapsed,
                'remaining_seconds': remaining,
                'remaining_percent': (remaining / self.trial_duration) * 100 if self.trial_duration > 0 else 0,
                'is_expired': remaining <= 0,
                'usage_count': trial_data.get('usage_count', 0),
                'last_access': trial_data.get('last_access'),
                'hwid': trial_data.get('hwid', 'unknown')[:8] + '...',
                'file_location': str(self.trial_file) if self.trial_file else 'memory'
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
                if self.trial_file and self.trial_file.exists():
                    os.remove(self.trial_file)
                
                self._start_time = None
                self._trial_data = None
                logger.info("Trial period reset (DEV MODE)")
                self._create_new_trial()
            else:
                logger.warning("Trial reset denied - not in DEV mode")
                
        except Exception as e:
            logger.error(f"Failed to reset trial: {e}")

# ============================================================================
# 2. Исправление пример приложения с правильным таймером
# ============================================================================

import tkinter as tk
from tkinter import ttk
import threading
import time

class ProtectedCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Защищенный калькулятор")
        self.window.geometry("400x500")
        
        # Переменные для таймера
        self.timer_active = False
        self.timer_thread = None
        
        self.setup_ui()
        self.start_trial_monitor()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        # Заголовок
        title_frame = ttk.Frame(self.window, padding="10")
        title_frame.pack(fill=tk.X)
        
        ttk.Label(title_frame, text="🔐 Защищенный калькулятор", 
                 font=('Arial', 16, 'bold')).pack()
        
        # Статус защиты
        self.status_frame = ttk.LabelFrame(self.window, text="Статус защиты", padding="10")
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Переменные для статуса
        self.version_var = tk.StringVar()
        self.trial_var = tk.StringVar()
        self.remaining_var = tk.StringVar()
        
        ttk.Label(self.status_frame, text="Версия:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.status_frame, textvariable=self.version_var).grid(row=0, column=1, sticky=tk.W, padx=(10,0))
        
        ttk.Label(self.status_frame, text="Режим:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.status_frame, textvariable=self.trial_var).grid(row=1, column=1, sticky=tk.W, padx=(10,0))
        
        ttk.Label(self.status_frame, text="Осталось:").grid(row=2, column=0, sticky=tk.W)
        self.remaining_label = ttk.Label(self.status_frame, textvariable=self.remaining_var, 
                                        font=('Arial', 10, 'bold'), foreground='red')
        self.remaining_label.grid(row=2, column=1, sticky=tk.W, padx=(10,0))
        
        # Прогресс бар триала
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, 
                                           maximum=100, length=200)
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=(10,0), sticky=(tk.W, tk.E))
        
        # Калькулятор
        calc_frame = ttk.LabelFrame(self.window, text="Калькулятор", padding="10")
        calc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Дисплей
        self.display_var = tk.StringVar(value="0")
        display = ttk.Entry(calc_frame, textvariable=self.display_var, 
                           font=('Arial', 14), justify='right', state='readonly')
        display.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопки
        buttons_frame = ttk.Frame(calc_frame)
        buttons_frame.pack()
        
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if btn_text == '0':
                    btn = ttk.Button(buttons_frame, text=btn_text, width=10,
                                   command=lambda x=btn_text: self.on_button_click(x))
                    btn.grid(row=i, column=j, columnspan=2, padx=1, pady=1, sticky='ew')
                elif btn_text == '.':
                    btn = ttk.Button(buttons_frame, text=btn_text, width=5,
                                   command=lambda x=btn_text: self.on_button_click(x))
                    btn.grid(row=i, column=j+1, padx=1, pady=1)
                else:
                    btn = ttk.Button(buttons_frame, text=btn_text, width=5,
                                   command=lambda x=btn_text: self.on_button_click(x))
                    btn.grid(row=i, column=j, padx=1, pady=1)
        
        # Кнопки управления
        control_frame = ttk.Frame(self.window, padding="10")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="📊 Статус защиты", 
                  command=self.show_status).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="🔑 Активировать лицензию", 
                  command=self.activate_license).pack(side=tk.LEFT)
        
        # Обновляем начальный статус
        self.update_status()
    
    def start_trial_monitor(self):
        """Запуск мониторинга триала"""
        self.timer_active = True
        self.timer_thread = threading.Thread(target=self.trial_monitor_loop, daemon=True)
        self.timer_thread.start()
    
    def trial_monitor_loop(self):
        """Цикл мониторинга триала"""
        while self.timer_active:
            try:
                # Обновляем UI через after() для безопасности потоков
                self.window.after(0, self.update_trial_display)
                
                # Проверяем доступ
                if not Kil0p3.check_trial_access():
                    self.window.after(0, self.on_trial_expired)
                    break
                
                time.sleep(0.1)  # Обновление каждые 100мс
                
            except Exception as e:
                print(f"Monitor error: {e}")
                break
    
    def update_trial_display(self):
        """Обновление отображения триала (вызывается из главного потока)"""
        try:
            trial_info = Kil0p3.get_trial_info()
            
            if trial_info.get('is_trial'):
                remaining = trial_info.get('remaining_seconds', 0)
                percent = trial_info.get('remaining_percent', 0)
                
                # Обновляем текст
                if remaining > 0:
                    self.remaining_var.set(f"{remaining:.1f} сек")
                    self.remaining_label.configure(foreground='orange' if remaining < 10 else 'green')
                else:
                    self.remaining_var.set("ИСТЕК")
                    self.remaining_label.configure(foreground='red')
                
                # Обновляем прогресс бар
                self.progress_var.set(max(0, percent))
                
                # Меняем цвет прогресс бара
                if percent < 25:
                    self.progress_bar.configure(style='red.Horizontal.TProgressbar')
                elif percent < 50:
                    self.progress_bar.configure(style='orange.Horizontal.TProgressbar')
                else:
                    self.progress_bar.configure(style='green.Horizontal.TProgressbar')
                    
        except Exception as e:
            print(f"Display update error: {e}")
    
    def update_status(self):
        """Обновление общего статуса"""
        try:
            status = Kil0p3.get_status()
            
            self.version_var.set(f"Kil0p3 v{status['version']}")
            
            if status['dev_mode']:
                self.trial_var.set("🛠️ DEV режим")
                self.remaining_var.set("Без ограничений")
                self.remaining_label.configure(foreground='blue')
            elif status['license_valid']:
                self.trial_var.set("🔐 Лицензия")
                self.remaining_var.set("Активна")
                self.remaining_label.configure(foreground='green')
            elif status['trial_active']:
                self.trial_var.set("⏱️ Триал")
                # remaining будет обновляться в trial_monitor_loop
            else:
                self.trial_var.set("❌ Истек")
                self.remaining_var.set("Требуется лицензия")
                self.remaining_label.configure(foreground='red')
                
        except Exception as e:
            print(f"Status update error: {e}")
    
    def on_button_click(self, value):
        """Обработка нажатий кнопок калькулятора"""
        try:
            # Проверяем доступ перед выполнением операций
            if not Kil0p3.check_trial_access():
                self.on_trial_expired()
                return
            
            current = self.display_var.get()
            
            if value == 'C':
                self.display_var.set("0")
            elif value == '=':
                try:
                    # Заменяем символы для eval
                    expression = current.replace('×', '*').replace('÷', '/')
                    result = eval(expression)
                    self.display_var.set(str(result))
                except:
                    self.display_var.set("Ошибка")
            elif value in ['×', '÷', '+', '-']:
                if current != "0" and current[-1] not in ['×', '÷', '+', '-']:
                    self.display_var.set(current + value)
            else:
                if current == "0":
                    self.display_var.set(value)
                else:
                    self.display_var.set(current + value)
                    
        except Exception as e:
            print(f"Button click error: {e}")
    
    def show_status(self):
        """Показать подробный статус"""
        status = Kil0p3.get_status()
        trial_info = Kil0p3.get_trial_info()
        
        message = f"""
🔐 Статус защиты Kil0p3:

📦 Версия: {status['version']}
🛡️ Защита активна: {status['protection_active']}
🔑 Лицензия: {'Валидна' if status['license_valid'] else 'Нет'}
🛠️ DEV режим: {status['dev_mode']}

⏱️ Триальный период:
📅 Статус: {'Активен' if trial_info.get('is_trial') else 'Неактивен'}
⏰ Осталось: {trial_info.get('remaining_seconds', 0):.1f} сек
📊 Процент: {trial_info.get('remaining_percent', 0):.1f}%
🎯 Использований: {trial_info.get('usage_count', 0)}

💻 Hardware ID: {Kil0p3.get_hwid()[:16]}...
        """
        
        tk.messagebox.showinfo("Статус защиты", message.strip())
    
    def activate_license(self):
        """Активация лицензии"""
        try:
            from Kil0p3.ui.auth_window import show_activation_window
            result = show_activation_window()
            
            if result.get('success'):
                self.update_status()
                tk.messagebox.showinfo("Успех", "Лицензия активирована успешно!")
            else:
                tk.messagebox.showwarning("Отмена", "Активация лицензии отменена")
                
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка активации: {e}")
    
    def on_trial_expired(self):
        """Обработка истечения триала"""
        self.timer_active = False
        
        tk.messagebox.showwarning(
            "Триальный период истек",
            "30-секундный триальный период истек!\n\n"
            "Для продолжения работы необходимо приобрести лицензию."
        )
        
        try:
            Kil0p3.show_trial_expired_message()
        except:
            pass
        
        self.window.quit()
    
    def run(self):
        """Запуск приложения"""
        try:
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.window.mainloop()
        except Exception as e:
            print(f"Application error: {e}")
    
    def on_closing(self):
        """Обработка закрытия окна"""
        self.timer_active = False
        self.window.quit()

# ============================================================================
# Пример использования:
# ============================================================================

if __name__ == "__main__":
    import os
    import sys
    
    # Для тестирования можно включить DEV режим
    if '--dev' in sys.argv:
        os.environ['KIL0P3_DEV_MODE'] = '1'
    
    # Импорт защиты
    import Kil0p3
    
    print("🚀 Запуск защищенного калькулятора...")
    print(f"📊 Статус защиты: {Kil0p3.get_status()}")
    
    # Запуск приложения
    app = ProtectedCalculator()
    app.run()