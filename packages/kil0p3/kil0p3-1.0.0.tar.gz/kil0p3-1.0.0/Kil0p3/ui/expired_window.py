# === Kilopa/Kil0p3/ui/expired_window.py ===
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Expired License Window
=============================

Окно уведомления об истечении лицензии
"""

import tkinter as tk
from tkinter import ttk
import sys

class ExpiredWindow:
    """Окно истечения лицензии"""
    
    def __init__(self):
        self.window = None
    
    def show(self):
        """Показать окно истечения"""
        try:
            self.window = tk.Tk()
            self.window.title("Лицензия истекла")
            self.window.geometry("400x300")
            self.window.resizable(False, False)
            
            # Создаем интерфейс
            main_frame = ttk.Frame(self.window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Заголовок
            title_label = ttk.Label(
                main_frame,
                text="Срок действия лицензии истек",
                font=('Arial', 14, 'bold'),
                foreground='red'
            )
            title_label.pack(pady=(0, 20))
            
            # Описание
            desc_label = ttk.Label(
                main_frame,
                text="Для продолжения работы необходимо\nобновить лицензию или приобрести новую.",
                justify=tk.CENTER
            )
            desc_label.pack(pady=(0, 20))
            
            # Кнопка закрытия
            close_btn = ttk.Button(
                main_frame,
                text="Закрыть",
                command=self._close
            )
            close_btn.pack()
            
            # Центрируем окно
            self._center_window()
            
            # Делаем окно модальным
            self.window.transient()
            self.window.grab_set()
            
            # Обработчик закрытия
            self.window.protocol("WM_DELETE_WINDOW", self._close)
            
            # Запускаем главный цикл
            self.window.mainloop()
            
        except Exception as e:
            print(f"Error showing expired window: {e}")
    
    def _center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _close(self):
        """Закрытие окна"""
        if self.window:
            self.window.destroy()
        sys.exit(1)

# === Kilopa/Kil0p3/ui/banned_window.py ===
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Banned Window
====================

Окно блокировки
"""

import tkinter as tk
from tkinter import ttk
import sys

class BannedWindow:
    """Окно блокировки"""
    
    def __init__(self, reason="Security violation"):
        self.window = None
        self.reason = reason
    
    def show(self):
        """Показать окно блокировки"""
        try:
            self.window = tk.Tk()
            self.window.title("Устройство заблокировано")
            self.window.geometry("450x350")
            self.window.resizable(False, False)
            
            # Создаем интерфейс
            main_frame = ttk.Frame(self.window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Заголовок
            title_label = ttk.Label(
                main_frame,
                text="⚠ УСТРОЙСТВО ЗАБЛОКИРОВАНО ⚠",
                font=('Arial', 16, 'bold'),
                foreground='red'
            )
            title_label.pack(pady=(0, 20))
            
            # Причина
            reason_label = ttk.Label(
                main_frame,
                text=f"Причина: {self.reason}",
                font=('Arial', 12),
                foreground='red'
            )
            reason_label.pack(pady=(0, 20))
            
            # Описание
            desc_text = (
                "Обнаружено нарушение условий использования.\n\n"
                "Для разблокировки обратитесь к поставщику\n"
                "программного обеспечения.\n\n"
                "Приложение будет закрыто."
            )
            desc_label = ttk.Label(
                main_frame,
                text=desc_text,
                justify=tk.CENTER
            )
            desc_label.pack(pady=(0, 20))
            
            # Кнопка закрытия
            close_btn = ttk.Button(
                main_frame,
                text="Закрыть",
                command=self._close
            )
            close_btn.pack()
            
            # Центрируем окно
            self._center_window()
            
            # Делаем окно модальным
            self.window.transient()
            self.window.grab_set()
            
            # Обработчик закрытия
            self.window.protocol("WM_DELETE_WINDOW", self._close)
            
            # Запускаем главный цикл
            self.window.mainloop()
            
        except Exception as e:
            print(f"Error showing banned window: {e}")
    
    def _center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _close(self):
        """Закрытие окна"""
        if self.window:
            self.window.destroy()
        sys.exit(1)

# === Kilopa/Kil0p3/runtime/watchdog.py ===
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Runtime Watchdog
=======================

Мониторинг защиты
"""

import threading
import time

class ProtectionWatchdog:
    """Сторожевой таймер защиты"""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Запуск watchdog"""
        self.running = True
        
    def stop(self):
        """Остановка watchdog"""
        self.running = False