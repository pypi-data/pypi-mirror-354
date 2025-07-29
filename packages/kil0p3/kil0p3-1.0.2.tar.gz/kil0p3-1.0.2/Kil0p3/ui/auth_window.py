#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 Authentication Window
============================

Окно активации лицензии
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import threading
from typing import Dict, Any, Optional

from ..config.constants import *
from ..tools.logger import get_logger
from ..core.license import license_manager
from ..core.hwid import hwid_generator
from ..runtime.attempt_counter import AttemptCounter

logger = get_logger(__name__)

class AuthWindow:
    """Окно активации лицензии"""
    
    def __init__(self):
        self.window = None
        self.result = {'success': False, 'license_key': None}
        self.attempt_counter = AttemptCounter()
        
    def show(self) -> Dict[str, Any]:
        """
        Показать окно активации
        
        Returns:
            Dict: Результат активации
        """
        try:
            logger.info("Showing license activation window")
            
            # Создаем главное окно
            self.window = tk.Tk()
            self.window.title(WINDOW_TITLE)
            self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            self.window.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)
            
            # Устанавливаем иконку и стиль
            self._setup_window_style()
            
            # Создаем интерфейс
            self._create_interface()
            
            # Центрируем окно
            self._center_window()
            
            # Делаем окно модальным
            self.window.transient()
            self.window.grab_set()
            self.window.focus_force()
            
            # Обработчик закрытия
            self.window.protocol("WM_DELETE_WINDOW", self._on_close)
            
            # Запускаем главный цикл
            self.window.mainloop()
            
            return self.result
            
        except Exception as e:
            logger.error(f"Error showing auth window: {e}")
            return {'success': False, 'error': str(e)}
    
    def _setup_window_style(self):
        """Настройка стиля окна"""
        try:
            # Настройка темы
            style = ttk.Style()
            
            # Пытаемся установить современную тему
            available_themes = style.theme_names()
            modern_themes = ['vista', 'xpnative', 'winnative', 'clam']
            
            for theme in modern_themes:
                if theme in available_themes:
                    style.theme_use(theme)
                    break
            
            # Настройка цветов
            self.window.configure(bg=COLORS['background'])
            
            # Запрещаем изменение размера
            self.window.resizable(False, False)
            
            # Устанавливаем иконку окна (если есть)
            try:
                self.window.iconbitmap('icon.ico')  # Добавьте иконку при необходимости
            except:
                pass
                
        except Exception as e:
            logger.debug(f"Window style setup error: {e}")
    
    def _create_interface(self):
        """Создание пользовательского интерфейса"""
        try:
            # Главный фрейм
            main_frame = ttk.Frame(self.window, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Заголовок
            title_label = ttk.Label(
                main_frame, 
                text="Активация лицензии",
                font=('Arial', 16, 'bold')
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
            
            # Описание
            desc_text = (
                "Для продолжения работы необходимо активировать лицензию.\n"
                "Введите ваш лицензионный ключ в формате:\n"
                "KLP-XXXX-XXXX-XXXX-XXXX"
            )
            desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
            desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
            
            # Информация о системе
            system_frame = ttk.LabelFrame(main_frame, text="Информация о системе", padding="10")
            system_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
            
            # HWID
            hwid = hwid_generator.generate()
            hwid_display = f"{hwid[:8]}...{hwid[-8:]}"
            
            ttk.Label(system_frame, text="Hardware ID:").grid(row=0, column=0, sticky=tk.W)
            hwid_label = ttk.Label(system_frame, text=hwid_display, font=('Courier', 10))
            hwid_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
            
            # Кнопка копирования HWID
            copy_hwid_btn = ttk.Button(
                system_frame, 
                text="Копировать HWID",
                command=lambda: self._copy_to_clipboard(hwid)
            )
            copy_hwid_btn.grid(row=0, column=2, padx=(10, 0))
            
            # Попытки активации
            attempts = self.attempt_counter.get_attempts()
            attempts_text = f"Попытки активации: {attempts}/{MAX_ACTIVATION_ATTEMPTS}"
            
            ttk.Label(system_frame, text=attempts_text).grid(row=1, column=0, columnspan=3, pady=(10, 0))
            
            if attempts >= MAX_ACTIVATION_ATTEMPTS - 1:
                warning_label = ttk.Label(
                    system_frame, 
                    text="⚠ Внимание: При следующей неудачной попытке устройство будет заблокировано!",
                    foreground='red'
                )
                warning_label.grid(row=2, column=0, columnspan=3, pady=(5, 0))
            
            # Ввод лицензионного ключа
            license_frame = ttk.LabelFrame(main_frame, text="Лицензионный ключ", padding="10")
            license_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
            
            # Поле ввода с автоформатированием
            self.license_var = tk.StringVar()
            self.license_var.trace('w', self._format_license_key)
            
            self.license_entry = ttk.Entry(
                license_frame, 
                textvariable=self.license_var,
                font=('Courier', 12),
                width=30,
                justify=tk.CENTER
            )
            self.license_entry.grid(row=0, column=0, columnspan=2, pady=(0, 10))
            self.license_entry.focus()
            
            # Кнопка вставки из буфера
            paste_btn = ttk.Button(
                license_frame,
                text="Вставить из буфера",
                command=self._paste_from_clipboard
            )
            paste_btn.grid(row=1, column=0, sticky=tk.W)
            
            # Прогресс бар (скрытый)
            self.progress_var = tk.StringVar(value="")
            self.progress_label = ttk.Label(license_frame, textvariable=self.progress_var)
            self.progress_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))
            
            self.progress_bar = ttk.Progressbar(
                license_frame, 
                mode='indeterminate'
            )
            
            # Кнопки управления
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=4, column=0, columnspan=2, pady=20)
            
            self.activate_btn = ttk.Button(
                button_frame,
                text="Активировать",
                command=self._activate_license,
                width=15
            )
            self.activate_btn.grid(row=0, column=0, padx=(0, 10))
            
            self.cancel_btn = ttk.Button(
                button_frame,
                text="Отмена", 
                command=self._on_close,
                width=15
            )
            self.cancel_btn.grid(row=0, column=1, padx=(10, 0))
            
            # Привязка Enter к активации
            self.window.bind('<Return>', lambda e: self._activate_license())
            self.window.bind('<Escape>', lambda e: self._on_close())
            
            # Дополнительная информация
            info_frame = ttk.Frame(main_frame)
            info_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
            
            help_text = "Для получения лицензии обратитесь к поставщику программного обеспечения"
            help_label = ttk.Label(info_frame, text=help_text, font=('Arial', 8), foreground='gray')
            help_label.grid(row=0, column=0)
            
        except Exception as e:
            logger.error(f"Interface creation error: {e}")
    
    def _format_license_key(self, *args):
        """Автоматическое форматирование лицензионного ключа"""
        try:
            current_value = self.license_var.get().upper()
            
            # Удаляем все кроме букв и цифр
            clean_value = ''.join(c for c in current_value if c.isalnum())
            
            # Добавляем дефисы каждые 4 символа
            if len(clean_value) > 3:
                formatted = []
                for i in range(0, len(clean_value), 4):
                    chunk = clean_value[i:i+4]
                    formatted.append(chunk)
                
                formatted_value = '-'.join(formatted)
                
                # Добавляем префикс если нужно
                if not formatted_value.startswith('KLP-'):
                    if len(clean_value) >= 3:
                        formatted_value = f"KLP-{'-'.join(formatted[1:])}"
                
                # Ограничиваем длину
                if len(formatted_value) > LICENSE_LENGTH:
                    formatted_value = formatted_value[:LICENSE_LENGTH]
                
                # Обновляем значение без вызова события
                self.license_var.trace_vdelete('w', self.license_var.trace_info()[0][1])
                self.license_var.set(formatted_value)
                self.license_var.trace('w', self._format_license_key)
            
        except Exception as e:
            logger.debug(f"License formatting error: {e}")
    
    def _copy_to_clipboard(self, text: str):
        """Копирование текста в буфер обмена"""
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(text)
            self.window.update()
            
            # Показываем уведомление
            messagebox.showinfo("Успех", "HWID скопирован в буфер обмена")
            
        except Exception as e:
            logger.error(f"Clipboard copy error: {e}")
            messagebox.showerror("Ошибка", "Не удалось скопировать в буфер обмена")
    
    def _paste_from_clipboard(self):
        """Вставка из буфера обмена"""
        try:
            clipboard_text = self.window.clipboard_get()
            
            # Очищаем и форматируем
            clean_text = ''.join(c for c in clipboard_text if c.isalnum() or c == '-')
            
            self.license_var.set(clean_text)
            
        except tk.TclError:
            messagebox.showwarning("Предупреждение", "Буфер обмена пуст")
        except Exception as e:
            logger.error(f"Clipboard paste error: {e}")
            messagebox.showerror("Ошибка", "Не удалось вставить из буфера обмена")
    
    def _activate_license(self):
        """Активация лицензии"""
        try:
            license_key = self.license_var.get().strip()
            
            if not license_key:
                messagebox.showwarning("Внимание", "Введите лицензионный ключ")
                return
            
            # Проверка формата
            if not license_manager.validate_license_key(license_key):
                messagebox.showerror("Ошибка", "Неверный формат лицензионного ключа")
                return
            
            # Отключаем кнопки
            self._set_ui_state(False)
            
            # Показываем прогресс
            self.progress_var.set("Активация лицензии...")
            self.progress_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
            self.progress_bar.start()
            
            # Запускаем активацию в отдельном потоке
            thread = threading.Thread(
                target=self._perform_activation,
                args=(license_key,),
                daemon=True
            )
            thread.start()
            
        except Exception as e:
            logger.error(f"License activation error: {e}")
            self._activation_failed(f"Ошибка активации: {e}")
    
    def _perform_activation(self, license_key: str):
        """Выполнение активации в отдельном потоке"""
        try:
            import time
            
            # Имитация проверки на сервере
            self.window.after(0, lambda: self.progress_var.set("Подключение к серверу..."))
            time.sleep(1)
            
            self.window.after(0, lambda: self.progress_var.set("Проверка лицензии..."))
            time.sleep(1)
            
            # Попытка активации
            success = license_manager.save_license(license_key)
            
            if success:
                # Проверяем валидность
                is_valid, error_msg = license_manager.validate_license()
                
                if is_valid:
                    self.window.after(0, self._activation_successful)
                else:
                    self.window.after(0, lambda: self._activation_failed(error_msg))
            else:
                self.window.after(0, lambda: self._activation_failed("Не удалось сохранить лицензию"))
                
        except Exception as e:
            logger.error(f"Activation thread error: {e}")
            self.window.after(0, lambda: self._activation_failed(f"Ошибка активации: {e}"))
    
    def _activation_successful(self):
        """Успешная активация"""
        try:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self.progress_var.set("")
            
            # Сбрасываем счетчик попыток
            self.attempt_counter.reset()
            
            # Показываем сообщение об успехе
            messagebox.showinfo(
                "Успех", 
                "Лицензия успешно активирована!\n\nПрограмма готова к работе."
            )
            
            # Сохраняем результат
            self.result = {
                'success': True,
                'license_key': self.license_var.get()
            }
            
            # Закрываем окно
            self._close_window()
            
        except Exception as e:
            logger.error(f"Activation success handler error: {e}")
    
    def _activation_failed(self, error_message: str):
        """Неудачная активация"""
        try:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self.progress_var.set("")
            
            # Увеличиваем счетчик попыток
            self.attempt_counter.increment()
            attempts = self.attempt_counter.get_attempts()
            
            # Включаем кнопки обратно
            self._set_ui_state(True)
            
            # Показываем ошибку
            if attempts >= MAX_ACTIVATION_ATTEMPTS:
                messagebox.showerror(
                    "Блокировка",
                    f"Превышено максимальное количество попыток активации.\n"
                    f"Устройство заблокировано.\n\n"
                    f"Ошибка: {error_message}"
                )
                
                # Блокируем устройство
                from ..runtime.block_state import BlockState
                block_state = BlockState()
                block_state.block_device("Too many activation attempts")
                
                self._close_window()
            else:
                remaining = MAX_ACTIVATION_ATTEMPTS - attempts
                messagebox.showerror(
                    "Ошибка активации",
                    f"{error_message}\n\n"
                    f"Осталось попыток: {remaining}"
                )
                
                # Обновляем информацию о попытках
                self._update_attempts_display()
            
        except Exception as e:
            logger.error(f"Activation failure handler error: {e}")
    
    def _update_attempts_display(self):
        """Обновление отображения попыток"""
        try:
            attempts = self.attempt_counter.get_attempts()
            
            # Находим и обновляем лейбл с попытками
            for widget in self.window.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.LabelFrame) and "система" in child.cget("text").lower():
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ttk.Label) and "попытки" in grandchild.cget("text").lower():
                                    grandchild.config(text=f"Попытки активации: {attempts}/{MAX_ACTIVATION_ATTEMPTS}")
                                    break
                            break
                    break
            
        except Exception as e:
            logger.debug(f"Attempts display update error: {e}")
    
    def _set_ui_state(self, enabled: bool):
        """Включение/отключение элементов UI"""
        try:
            state = 'normal' if enabled else 'disabled'
            
            self.license_entry.config(state=state)
            self.activate_btn.config(state=state)
            
            if enabled:
                self.license_entry.focus()
                
        except Exception as e:
            logger.debug(f"UI state change error: {e}")
    
    def _center_window(self):
        """Центрирование окна на экране"""
        try:
            self.window.update_idletasks()
            
            # Получаем размеры экрана
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            # Вычисляем позицию
            x = (screen_width - WINDOW_WIDTH) // 2
            y = (screen_height - WINDOW_HEIGHT) // 2
            
            self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
            
        except Exception as e:
            logger.debug(f"Window centering error: {e}")
    
    def _on_close(self):
        """Обработчик закрытия окна"""
        try:
            # Подтверждение закрытия
            if messagebox.askquestion(
                "Подтверждение",
                "Закрыть окно активации?\n\nБез активной лицензии программа не сможет работать.",
                icon='warning'
            ) == 'yes':
                
                self.result = {'success': False, 'cancelled': True}
                self._close_window()
                
        except Exception as e:
            logger.error(f"Close handler error: {e}")
            self._close_window()
    
    def _close_window(self):
        """Закрытие окна"""
        try:
            if self.window:
                self.window.grab_release()
                self.window.destroy()
                
        except Exception as e:
            logger.debug(f"Window close error: {e}")

def show_activation_window() -> Dict[str, Any]:
    """
    Быстрое отображение окна активации
    
    Returns:
        Dict: Результат активации
    """
    try:
        window = AuthWindow()
        return window.show()
        
    except Exception as e:
        logger.error(f"Failed to show activation window: {e}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Тестирование окна
    import os
    os.environ['KIL0P3_DEV_MODE'] = '1'
    
    result = show_activation_window()
    print(f"Activation result: {result}")