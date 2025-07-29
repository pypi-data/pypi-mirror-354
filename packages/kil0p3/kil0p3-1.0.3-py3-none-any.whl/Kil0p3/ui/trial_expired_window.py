#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/ui/trial_expired_window.py
==================================

Окно истечения триального периода
"""

import tkinter as tk
from tkinter import ttk
import sys
import webbrowser

class TrialExpiredWindow:
    """Окно истечения триального периода"""
    
    def __init__(self):
        self.window = None
    
    def show(self):
        """Показать окно истечения триала"""
        try:
            self.window = tk.Tk()
            self.window.title("Триальный период истек")
            self.window.geometry("500x400")
            self.window.resizable(False, False)
            
            # Создаем интерфейс
            main_frame = ttk.Frame(self.window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Заголовок
            title_label = ttk.Label(
                main_frame,
                text="⏰ Триальный период истек",
                font=('Arial', 16, 'bold'),
                foreground='orange'
            )
            title_label.pack(pady=(0, 20))
            
            # Описание
            desc_text = (
                "Вы использовали все 30 секунд бесплатного триального периода.\n\n"
                "Для продолжения работы с приложением необходимо\n"
                "приобрести лицензию."
            )
            desc_label = ttk.Label(
                main_frame,
                text=desc_text,
                justify=tk.CENTER,
                font=('Arial', 10)
            )
            desc_label.pack(pady=(0, 20))
            
            # Информация о лицензии
            license_frame = ttk.LabelFrame(main_frame, text="Варианты лицензий", padding="15")
            license_frame.pack(fill=tk.X, pady=(0, 20))
            
            licenses_text = (
                "🔹 Базовая лицензия - $9.99\n"
                "   Доступ на 1 год для 1 устройства\n\n"
                "🔹 Расширенная лицензия - $19.99\n"
                "   Доступ на 1 год для 3 устройств\n\n"
                "🔹 Корпоративная лицензия - $49.99\n"
                "   Безлимитное использование"
            )
            
            licenses_label = ttk.Label(
                license_frame,
                text=licenses_text,
                justify=tk.LEFT,
                font=('Arial', 9)
            )
            licenses_label.pack()
            
            # Кнопки
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(pady=20)
            
            buy_btn = ttk.Button(
                button_frame,
                text="💳 Купить лицензию",
                command=self._open_purchase_page
            )
            buy_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            activate_btn = ttk.Button(
                button_frame,
                text="🔑 У меня есть ключ",
                command=self._show_activation
            )
            activate_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            close_btn = ttk.Button(
                button_frame,
                text="❌ Закрыть",
                command=self._close
            )
            close_btn.pack(side=tk.LEFT)
            
            # Дополнительная информация
            info_text = (
                "💡 Лицензионный ключ привязывается к вашему устройству\n"
                "🔒 Все данные защищены и остаются конфиденциальными\n"
                "📧 Поддержка: support@kil0p3.dev"
            )
            
            info_label = ttk.Label(
                main_frame,
                text=info_text,
                justify=tk.CENTER,
                font=('Arial', 8),
                foreground='gray'
            )
            info_label.pack(pady=(10, 0))
            
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
            print(f"Error showing trial expired window: {e}")
    
    def _center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _open_purchase_page(self):
        """Открытие страницы покупки"""
        try:
            # В реальном проекте здесь будет ссылка на ваш магазин
            url = "https://kil0p3.dev/purchase"
            webbrowser.open(url)
            
            print("🌐 Открыта страница покупки лицензии")
            
        except Exception as e:
            print(f"Error opening purchase page: {e}")
    
    def _show_activation(self):
        """Показать окно активации"""
        try:
            self.window.destroy()
            
            # Импортируем и показываем окно активации
            from .auth_window import AuthWindow
            auth_window = AuthWindow()
            result = auth_window.show()
            
            if result.get('success'):
                print("✅ Лицензия активирована успешно!")
            else:
                # Если активация не удалась, показываем окно снова
                self.show()
                
        except Exception as e:
            print(f"Error showing activation window: {e}")
            self._close()
    
    def _close(self):
        """Закрытие окна"""
        if self.window:
            self.window.destroy()
        print("🔒 Приложение завершено - триальный период истек")
        sys.exit(1)