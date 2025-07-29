# ============================================================================
# 1. Обновленный Kil0p3/__init__.py с автоматическим баннером
# ============================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3 - Advanced Python Application Protection Library
========================================================

АВТОМАТИЧЕСКАЯ ЗАЩИТА И ДЕМО-БАННЕР:
    import Kil0p3  # Добавляет демо-баннер в любое приложение!

Библиотека обеспечивает:
- Автоматический демо-баннер сверху окна
- 30-секундный триальный период с таймером
- Защиту от обмана с системой предупреждений
- Автоматическое закрытие при истечении демо
"""

__version__ = "1.0.3"
__author__ = "Kil0p3 Security Team"
__license__ = "Proprietary"
__copyright__ = "Copyright (c) 2025 Kil0p3 Security"

import os
import sys
import threading
import time
import tkinter as tk
from typing import Optional, Dict, Any

# Проверка минимальной версии Python
if sys.version_info < (3, 8):
    raise RuntimeError("Kil0p3 requires Python 3.8 or higher")

# Глобальные переменные
_protection_active = False
_license_key: Optional[str] = None
_validation_result = None
_initialization_complete = False
_trial_active = False
_demo_banner = None
_banner_thread = None

class DemoBanner:
    """Демо-баннер который показывается поверх всех окон"""
    
    def __init__(self):
        self.banner_window = None
        self.time_label = None
        self.active = False
        self.violation_count = 0
        self.last_check_time = time.time()
        
    def create_banner(self):
        """Создание баннера"""
        try:
            if self.banner_window:
                return
                
            # Создаем toplevel окно для баннера
            self.banner_window = tk.Toplevel()
            self.banner_window.title("Demo")
            
            # Настройка окна баннера
            screen_width = self.banner_window.winfo_screenwidth()
            banner_height = 35
            
            # Размещаем сверху экрана
            self.banner_window.geometry(f"{screen_width}x{banner_height}+0+0")
            
            # Стиль окна
            self.banner_window.configure(bg='black')
            self.banner_window.overrideredirect(True)  # Убираем рамку
            self.banner_window.attributes('-topmost', True)  # Поверх всех окон
            self.banner_window.attributes('-alpha', 0.9)  # Полупрозрачность
            
            # На Windows дополнительные настройки
            try:
                self.banner_window.attributes('-toolwindow', True)
            except:
                pass
            
            # Основной фрейм
            main_frame = tk.Frame(self.banner_window, bg='black')
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Левая часть - демо информация
            left_frame = tk.Frame(main_frame, bg='black')
            left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
            
            demo_label = tk.Label(
                left_frame,
                text="🎮 ДЕМО ВЕРСИЯ",
                bg='black',
                fg='yellow',
                font=('Arial', 12, 'bold')
            )
            demo_label.pack(side=tk.LEFT, pady=5)
            
            # Центр - таймер
            center_frame = tk.Frame(main_frame, bg='black')
            center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            
            self.time_label = tk.Label(
                center_frame,
                text="Осталось: 30.0 сек",
                bg='black',
                fg='yellow',
                font=('Arial', 12, 'bold')
            )
            self.time_label.pack(expand=True)
            
            # Правая часть - кнопки
            right_frame = tk.Frame(main_frame, bg='black')
            right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
            
            license_btn = tk.Button(
                right_frame,
                text="🔑 Купить",
                bg='#FFD700',
                fg='black',
                font=('Arial', 9, 'bold'),
                command=self.open_purchase,
                relief=tk.FLAT,
                padx=10
            )
            license_btn.pack(side=tk.RIGHT, pady=3, padx=5)
            
            activate_btn = tk.Button(
                right_frame,
                text="🎯 Активировать",
                bg='#32CD32',
                fg='black',
                font=('Arial', 9, 'bold'),
                command=self.activate_license,
                relief=tk.FLAT,
                padx=10
            )
            activate_btn.pack(side=tk.RIGHT, pady=3, padx=5)
            
            # Запускаем обновление таймера
            self.active = True
            self.update_timer()
            
            print("🎮 Демо-баннер активирован")
            
        except Exception as e:
            print(f"Ошибка создания баннера: {e}")
    
    def update_timer(self):
        """Обновление таймера"""
        try:
            if not self.active or not self.banner_window:
                return
                
            # Получаем время из библиотеки
            remaining = get_trial_time_remaining()
            
            # Проверяем на попытки обмана
            self.check_for_cheating()
            
            if remaining > 0:
                # Обновляем текст
                if remaining < 10:
                    self.time_label.configure(
                        text=f"⚠️ Осталось: {remaining:.1f} сек",
                        fg='red'
                    )
                else:
                    self.time_label.configure(
                        text=f"Осталось: {remaining:.1f} сек",
                        fg='yellow'
                    )
                
                # Следующее обновление
                self.banner_window.after(100, self.update_timer)
            else:
                # Демо истекло
                self.time_label.configure(
                    text="❌ ДЕМО ИСТЕКЛО",
                    fg='red'
                )
                
                # Закрываем через 2 секунды
                self.banner_window.after(2000, self.on_demo_expired)
                
        except Exception as e:
            print(f"Ошибка обновления таймера: {e}")
    
    def check_for_cheating(self):
        """Проверка на попытки обмана"""
        try:
            current_time = time.time()
            
            # Проверка на откат времени
            if current_time < self.last_check_time - 2:  # Допуск 2 секунды
                self.violation_count += 1
                self.show_violation_warning("Обнаружен откат системного времени!")
            
            self.last_check_time = current_time
            
            # Проверка других нарушений через библиотеку
            if not check_trial_access():
                # Дополнительные проверки...
                pass
                
        except Exception as e:
            print(f"Ошибка проверки обмана: {e}")
    
    def show_violation_warning(self, reason: str):
        """Показ предупреждения о нарушении"""
        try:
            print(f"⚠️ ПРЕДУПРЕЖДЕНИЕ: {reason}")
            print(f"📊 Нарушений: {self.violation_count}/3")
            
            if self.violation_count >= 3:
                self.ban_user(reason)
            else:
                # Показываем предупреждение в баннере
                if self.time_label:
                    self.time_label.configure(
                        text=f"⚠️ ПРЕДУПРЕЖДЕНИЕ {self.violation_count}/3",
                        fg='red'
                    )
                    # Возвращаем таймер через 3 секунды
                    self.banner_window.after(3000, lambda: self.time_label.configure(fg='yellow'))
                    
        except Exception as e:
            print(f"Ошибка показа предупреждения: {e}")
    
    def ban_user(self, reason: str):
        """Блокировка пользователя"""
        try:
            print(f"🚫 ПОЛЬЗОВАТЕЛЬ ЗАБЛОКИРОВАН: {reason}")
            
            # Блокируем через библиотеку
            from .runtime.block_state import block_state
            block_state.block_device(f"Cheating detected: {reason}")
            
            # Обновляем баннер
            if self.time_label:
                self.time_label.configure(
                    text="🚫 ЗАБЛОКИРОВАНО",
                    fg='red'
                )
            
            # Закрываем через 3 секунды
            self.banner_window.after(3000, self.close_application)
            
        except Exception as e:
            print(f"Ошибка блокировки: {e}")
            self.close_application()
    
    def open_purchase(self):
        """Открытие страницы покупки"""
        try:
            import webbrowser
            webbrowser.open("https://kil0p3.dev/purchase")
            print("🌐 Открыта страница покупки")
        except Exception as e:
            print(f"Ошибка открытия страницы: {e}")
    
    def activate_license(self):
        """Активация лицензии"""
        try:
            from .ui.auth_window import show_activation_window
            
            # Скрываем баннер временно
            if self.banner_window:
                self.banner_window.withdraw()
            
            result = show_activation_window()
            
            if result.get('success'):
                print("✅ Лицензия активирована!")
                self.close_banner()
            else:
                # Показываем баннер обратно
                if self.banner_window:
                    self.banner_window.deiconify()
                    
        except Exception as e:
            print(f"Ошибка активации: {e}")
            # Показываем баннер обратно
            if self.banner_window:
                self.banner_window.deiconify()
    
    def on_demo_expired(self):
        """Обработка истечения демо"""
        try:
            print("⏰ Демо период истек!")
            
            # Показываем окно истечения
            self.show_expired_window()
            
            # Закрываем приложение
            self.close_application()
            
        except Exception as e:
            print(f"Ошибка обработки истечения: {e}")
            self.close_application()
    
    def show_expired_window(self):
        """Показ окна истечения демо"""
        try:
            # Создаем окно истечения
            expired_window = tk.Toplevel()
            expired_window.title("Демо период истек")
            expired_window.geometry("500x300")
            expired_window.configure(bg='white')
            expired_window.attributes('-topmost', True)
            
            # Контент
            main_frame = tk.Frame(expired_window, bg='white', padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Заголовок
            title_label = tk.Label(
                main_frame,
                text="⏰ Демо период истек!",
                font=('Arial', 18, 'bold'),
                fg='red',
                bg='white'
            )
            title_label.pack(pady=(0, 20))
            
            # Описание
            desc_text = (
                "Вы использовали 30 секунд бесплатного демо-периода.\n\n"
                "Для продолжения работы приобретите полную версию\n"
                "или активируйте лицензионный ключ."
            )
            desc_label = tk.Label(
                main_frame,
                text=desc_text,
                font=('Arial', 12),
                bg='white',
                justify=tk.CENTER
            )
            desc_label.pack(pady=(0, 30))
            
            # Кнопки
            btn_frame = tk.Frame(main_frame, bg='white')
            btn_frame.pack()
            
            buy_btn = tk.Button(
                btn_frame,
                text="💳 Купить полную версию",
                font=('Arial', 12, 'bold'),
                bg='#FFD700',
                fg='black',
                padx=20,
                pady=10,
                command=lambda: [self.open_purchase(), expired_window.destroy()]
            )
            buy_btn.pack(side=tk.LEFT, padx=10)
            
            activate_btn = tk.Button(
                btn_frame,
                text="🔑 У меня есть ключ",
                font=('Arial', 12, 'bold'),
                bg='#32CD32',
                fg='black',
                padx=20,
                pady=10,
                command=lambda: [expired_window.destroy(), self.activate_license()]
            )
            activate_btn.pack(side=tk.LEFT, padx=10)
            
            close_btn = tk.Button(
                btn_frame,
                text="❌ Закрыть",
                font=('Arial', 12),
                bg='#FF6B6B',
                fg='white',
                padx=20,
                pady=10,
                command=lambda: [expired_window.destroy(), self.close_application()]
            )
            close_btn.pack(side=tk.LEFT, padx=10)
            
            # Центрируем окно
            expired_window.update_idletasks()
            x = (expired_window.winfo_screenwidth() // 2) - (500 // 2)
            y = (expired_window.winfo_screenheight() // 2) - (300 // 2)
            expired_window.geometry(f"500x300+{x}+{y}")
            
        except Exception as e:
            print(f"Ошибка показа окна истечения: {e}")
    
    def close_banner(self):
        """Закрытие баннера"""
        try:
            self.active = False
            if self.banner_window:
                self.banner_window.destroy()
                self.banner_window = None
            print("🎮 Демо-баннер закрыт")
        except Exception as e:
            print(f"Ошибка закрытия баннера: {e}")
    
    def close_application(self):
        """Закрытие приложения"""
        try:
            self.close_banner()
            
            # Закрываем все Tkinter окна
            if tk._default_root:
                tk._default_root.quit()
                tk._default_root.destroy()
            
            print("🔒 Приложение закрыто")
            sys.exit(0)
            
        except Exception as e:
            print(f"Ошибка закрытия приложения: {e}")
            sys.exit(1)

def create_demo_banner():
    """Создание демо-баннера"""
    global _demo_banner, _banner_thread
    
    try:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print("🛠️ DEV MODE: Демо-баннер отключен")
            return
        
        if check_license():
            print("🔐 Лицензия активна - баннер не нужен")
            return
        
        def banner_thread():
            try:
                # Ждем пока появится основное окно Tkinter
                max_wait = 10  # 10 секунд
                wait_count = 0
                
                while wait_count < max_wait:
                    try:
                        if tk._default_root and tk._default_root.winfo_exists():
                            break
                    except:
                        pass
                    time.sleep(1)
                    wait_count += 1
                
                # Создаем баннер
                _demo_banner = DemoBanner()
                _demo_banner.create_banner()
                
            except Exception as e:
                print(f"Ошибка создания баннера в потоке: {e}")
        
        # Запускаем в отдельном потоке
        _banner_thread = threading.Thread(target=banner_thread, daemon=True)
        _banner_thread.start()
        
    except Exception as e:
        print(f"Ошибка запуска демо-баннера: {e}")

# Существующие функции...
def get_version() -> str:
    return __version__

def get_status() -> Dict[str, Any]:
    global _protection_active, _validation_result, _license_key, _trial_active
    
    status = {
        'version': __version__,
        'protection_active': _protection_active,
        'license_valid': _validation_result.is_valid if _validation_result else False,
        'license_key': _license_key[-8:] + '...' if _license_key else None,
        'dev_mode': os.getenv('KIL0P3_DEV_MODE', '0') == '1',
        'initialized': _initialization_complete,
        'trial_active': _trial_active,
        'demo_banner_active': _demo_banner.active if _demo_banner else False
    }
    
    try:
        from .core.trial import trial_manager
        trial_info = trial_manager.get_trial_info()
        status['trial'] = trial_info
    except:
        status['trial'] = {'error': 'Trial manager not available'}
    
    return status

def set_license(license_key: str) -> bool:
    global _license_key
    try:
        from .core.license import license_manager
        
        if license_manager.validate_license_key(license_key):
            _license_key = license_key
            license_manager.save_license(license_key)
            
            # Закрываем баннер если лицензия активна
            if _demo_banner:
                _demo_banner.close_banner()
            
            return True
        else:
            return False
            
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error setting license: {e}")
        return False

def check_license() -> bool:
    try:
        from .core.validator import system_validator
        
        result = system_validator.validate_full()
        
        global _validation_result
        _validation_result = result
        
        return result.is_valid
        
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error checking license: {e}")
        return False

def get_hwid() -> str:
    try:
        from .core.hwid import hwid_generator
        return hwid_generator.generate()
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error getting HWID: {e}")
        return "ERROR"

def is_protected() -> bool:
    return _protection_active

def is_trial_active() -> bool:
    try:
        from .core.trial import trial_manager
        return not trial_manager.is_trial_expired()
    except:
        return False

def get_trial_time_remaining() -> float:
    try:
        from .core.trial import trial_manager
        return trial_manager.get_remaining_time()
    except:
        return 0.0

def get_trial_info() -> Dict[str, Any]:
    try:
        from .core.trial import trial_manager
        return trial_manager.get_trial_info()
    except Exception as e:
        return {'error': str(e)}

def check_trial_access() -> bool:
    try:
        # В DEV режиме всегда разрешаем
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            return True
        
        # Проверяем лицензию
        if check_license():
            return True
        
        # Если нет лицензии - проверяем триал
        from .core.trial import trial_manager
        
        if trial_manager.check_continuous_usage():
            global _trial_active
            _trial_active = True
            return True
        else:
            _trial_active = False
            return False
            
    except Exception as e:
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print(f"Error checking trial access: {e}")
        return False

def _initialize_protection():
    """Инициализация защиты при импорте"""
    global _protection_active, _initialization_complete, _trial_active
    
    try:
        # DEV режим
        if os.getenv('KIL0P3_DEV_MODE') == '1':
            print("🛠️ Kil0p3 DEV MODE - Protection disabled for development")
            _protection_active = False
            _trial_active = True
            _initialization_complete = True
            return
        
        print(f"🔐 Kil0p3 v{__version__} - Initializing protection with demo banner...")
        
        # Проверяем лицензию
        if check_license():
            print("✅ Valid license found - full access granted")
            _protection_active = True
            _trial_active = False
            _initialization_complete = True
            return
        
        # Если нет лицензии - запускаем триал с баннером
        from .core.trial import trial_manager
        
        if trial_manager.start_trial_session():
            remaining = trial_manager.get_remaining_time()
            print(f"🎮 Demo period active - {remaining:.1f} seconds remaining")
            _trial_active = True
            _protection_active = True
            _initialization_complete = True
            
            # Создаем демо-баннер (с задержкой для Tkinter)
            def delayed_banner():
                time.sleep(2)  # Ждем 2 секунды
                create_demo_banner()
            
            threading.Thread(target=delayed_banner, daemon=True).start()
            
        else:
            print("🔒 Demo period expired - access denied")
            _trial_active = False
            _protection_active = False
            _initialization_complete = True
            
    except Exception as e:
        print(f"💥 Kil0p3: Protection initialization error: {e}")
        _protection_active = False
        _initialization_complete = True

# Экспорт функций
__all__ = [
    'get_version', 'get_status', 'set_license', 'check_license', 'get_hwid',
    'is_protected', 'is_trial_active', 'get_trial_time_remaining', 
    'get_trial_info', 'check_trial_access', 'create_demo_banner',
    '__version__', '__author__'
]

# Автоматический запуск защиты при импорте
try:
    _initialize_protection()
except Exception as e:
    print(f"💥 Kil0p3: Fatal initialization error: {e}")
    if not os.getenv('KIL0P3_DEV_MODE'):
        sys.exit(1)

# Финальное сообщение
if os.getenv('KIL0P3_DEV_MODE') == '1':
    print(f"🛠️ Kil0p3 v{__version__} loaded in DEV MODE")
else:
    status = "LICENSED" if check_license() else ("DEMO" if _trial_active else "EXPIRED")
    print(f"🔐 Kil0p3 v{__version__} - Status: {status}")

# ============================================================================
# 2. Пример приложения с автоматическим баннером
# ============================================================================

# test_app.py
import os
import sys
import tkinter as tk
from tkinter import ttk

# Для тестирования включите DEV режим
# os.environ['KIL0P3_DEV_MODE'] = '1'

# Импорт защиты (баннер создастся автоматически)
import Kil0p3

class TestApplication:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎮 Тестовое приложение")
        self.window.geometry("600x400")
        
        # Отступ сверху для баннера (если не DEV режим)
        if not Kil0p3.get_status()['dev_mode']:
            self.window.geometry("600x400+100+50")  # Сдвигаем вниз
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="🎮 Защищенное приложение",
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Информация о защите
        info_frame = ttk.LabelFrame(main_frame, text="Информация о защите", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        status = Kil0p3.get_status()
        
        info_text = f"""
📦 Версия: Kil0p3 v{status['version']}
🛡️ Защита активна: {status['protection_active']}
🔑 Лицензия: {'Валидна' if status['license_valid'] else 'Демо режим'}
🛠️ DEV режим: {status['dev_mode']}
🎮 Демо-баннер: {'Активен' if status.get('demo_banner_active') else 'Неактивен'}
        """
        
        info_label = ttk.Label(info_frame, text=info_text.strip(), justify=tk.LEFT)
        info_label.pack()
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(
            btn_frame,
            text="📊 Показать статус",
            command=self.show_status
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔑 Активировать лицензию",
            command=self.activate_license
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="⏰ Время демо",
            command=self.show_demo_time
        ).pack(side=tk.LEFT, padx=5)
        
        # Область контента
        content_frame = ttk.LabelFrame(main_frame, text="Основной функционал", padding="15")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        content_text = tk.Text(content_frame, height=8, wrap=tk.WORD)
        content_text.pack(fill=tk.BOTH, expand=True)
        
        demo_info = """
🎮 Это демо-версия приложения!

⏰ У вас есть 30 секунд для тестирования функционала.

🔝 Сверху экрана должен появиться черный баннер с желтым текстом и таймером.

🔑 Для получения полной версии:
   • Нажмите "Купить" в баннере
   • Или "Активировать" если у вас есть ключ

⚠️ Попытки обмана (откат времени и т.д.) приведут к предупреждениям, 
   а затем к блокировке после 3 нарушений.

💡 Для тестирования установите переменную KIL0P3_DEV_MODE=1
        """
        
        content_text.insert(tk.END, demo_info.strip())
        content_text.configure(state='disabled')
        
        # Проверка доступа каждую секунду
        self.check_access()
    
    def check_access(self):
        """Проверка доступа к приложению"""
        try:
            if Kil0p3.check_trial_access():
                # Доступ есть, проверяем снова через секунду
                self.window.after(1000, self.check_access)
            else:
                # Доступ закончился
                print("🔒 Доступ к приложению закончился")
                self.window.quit()
        except Exception as e:
            print(f"Ошибка проверки доступа: {e}")
    
    def show_status(self):
        """Показать подробный статус"""
        status = Kil0p3.get_status()
        trial_info = Kil0p3.get_trial_info()
        
        message = f"""
🔐 Kil0p3 Protection Status:

📦 Version: {status['version']}
🛡️ Protection: {status['protection_active']}
🔑 License: {'Valid' if status['license_valid'] else 'Demo'}
🛠️ DEV Mode: {status['dev_mode']}

⏰ Demo Status:
• Active: {trial_info.get('is_trial', False)}
• Remaining: {trial_info.get('remaining_seconds', 0):.1f} sec
• Progress: {trial_info.get('remaining_percent', 0):.1f}%
• Usage Count: {trial_info.get('usage_count', 0)}

💻 Hardware ID: {Kil0p3.get_hwid()[:16]}...
        """
        
        tk.messagebox.showinfo("Protection Status", message.strip())
    
    def activate_license(self):
        """Активация лицензии"""
        try:
            from Kil0p3.ui.auth_window import show_activation_window
            result = show_activation_window()
            
            if result.get('success'):
                tk.messagebox.showinfo("Успех", "Лицензия активирована успешно!")
                # Перезагружаем информацию
                self.setup_ui()
            else:
                tk.messagebox.showwarning("Отмена", "Активация лицензии отменена")
                
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка активации: {e}")
    
    def show_demo_time(self):
        """Показать оставшееся время демо"""
        remaining = Kil0p3.get_trial_time_remaining()
        trial_info = Kil0p3.get_trial_info()
        
        if remaining > 0:
            message = f"""
⏰ Демо период активен

🕐 Осталось времени: {remaining:.1f} секунд
📊 Процент использован: {100 - trial_info.get('remaining_percent', 0):.1f}%
🎯 Запусков: {trial_info.get('usage_count', 0)}

💡 Черный баннер сверху экрана показывает актуальное время.
            """
        else:
            message = """
❌ Демо период истек!

🔒 Для продолжения работы необходимо:
   • Купить полную версию
   • Активировать лицензионный ключ

🛒 Нажмите кнопку "Купить" в баннере
            """
        
        tk.messagebox.showinfo("Демо время", message.strip())
    
    def run(self):
        """Запуск приложения"""
        print("🚀 Запуск тестового приложения...")
        print(f"📊 Статус: {Kil0p3.get_status()}")
        
        try:
            self.window.mainloop()
        except Exception as e:
            print(f"Ошибка приложения: {e}")

if __name__ == "__main__":
    app = TestApplication()
    app.run()

# ============================================================================
# 3. Обновленный trial.py с исправленными правами доступа
# ============================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kil0p3/core/trial.py
====================

Менеджер триального периода с защитой от обмана
"""

import os
import time
import json
import tempfile
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from ..config.constants import APP_DATA_DIR
    from ..tools.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    APP_DATA_DIR = Path.home() / ".kil0p3"
    import logging
    logger = logging.getLogger(__name__)

class TrialManager:
    """Менеджер триального периода с защитой от обмана"""
    
    def __init__(self, trial_duration_seconds: int = 30):
        self.trial_duration = trial_duration_seconds
        self.trial_file = self._get_safe_trial_path()
        self._trial_data = None
        self._start_time = None
        self._last_check_time = time.time()
        self._violation_count = 0
        self._ensure_file_exists()
    
    def _get_safe_trial_path(self) -> Optional[Path]:
        """Получение безопасного пути для файла триала"""
        paths_to_try = [
            # 1. Стандартная папка пользователя
            APP_DATA_DIR / "trial.dat",
            # 2. Временная папка
            Path(tempfile.gettempdir()) / ".kil0p3" / "trial.dat",
            # 3. Папка рядом с приложением
            Path(__file__).parent.parent.parent / ".kil0p3" / "trial.dat",
            # 4. Системная временная папка
            Path(tempfile.gettempdir()) / f"kil0p3_trial_{os.getpid()}.dat"
        ]
        
        for trial_path in paths_to_try:
            try:
                # Создаем директорию
                trial_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Тестируем запись
                test_file = trial_path.parent / f"test_{os.getpid()}.tmp"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                
                logger.debug(f"Using trial file: {trial_path}")
                return trial_path
                
            except (PermissionError, OSError) as e:
                logger.debug(f"Cannot use {trial_path}: {e}")
                continue
        
        # Если ничего не работает - используем память
        logger.warning("Using in-memory trial storage (not persistent)")
        return None
    
    def _ensure_file_exists(self):
        """Создание файла триала если не существует"""
        try:
            if self.trial_file is None or not self.trial_file.exists():
                self._create_new_trial()
        except Exception as e:
            logger.error(f"Failed to create trial file: {e}")
            self.trial_file = None
            self._create_new_trial()
    
    def _create_new_trial(self):
        """Создание нового триального периода"""
        try:
            self._start_time = time.time()
            
            trial_data = {
                'started_at': datetime.now().isoformat(),
                'duration_seconds': self.trial_duration,
                'start_timestamp': self._start_time,
                'usage_count': 0,
                'hwid': self._get_current_hwid(),
                'created': datetime.now().isoformat(),
                'violation_count': 0,
                'checksum': ''
            }
            
            # Добавляем контрольную сумму
            trial_data['checksum'] = self._calculate_checksum(trial_data)
            
            self._save_trial_data(trial_data)
            self._trial_data = trial_data
            
            logger.info(f"New trial period created: {self.trial_duration} seconds")
            
        except Exception as e:
            logger.error(f"Failed to create new trial: {e}")
            # Минимальные данные в памяти
            self._trial_data = {
                'start_timestamp': time.time(),
                'duration_seconds': self.trial_duration,
                'hwid': self._get_current_hwid(),
                'violation_count': 0
            }
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Вычисление контрольной суммы данных триала"""
        try:
            # Исключаем саму контрольную сумму
            clean_data = {k: v for k, v in data.items() if k != 'checksum'}
            data_str = json.dumps(clean_data, sort_keys=True)
            return hashlib.sha256(data_str.encode()).hexdigest()[:16]
        except:
            return "unknown"
    
    def _verify_checksum(self, data: Dict[str, Any]) -> bool:
        """Проверка контрольной суммы"""
        try:
            stored_checksum = data.get('checksum', '')
            calculated_checksum = self._calculate_checksum(data)
            return stored_checksum == calculated_checksum
        except:
            return False
    
    def _load_trial_data(self) -> Dict[str, Any]:
        """Загрузка данных триала с проверками безопасности"""
        try:
            if self.trial_file is None or not self.trial_file.exists():
                if self._trial_data is None:
                    self._create_new_trial()
                return self._trial_data
            
            with open(self.trial_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Проверка контрольной суммы
            if not self._verify_checksum(data):
                logger.warning("Trial data checksum mismatch - possible tampering")
                self._add_violation("Data integrity violation")
                self._create_new_trial()
                return self._trial_data
            
            # Проверка HWID
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
                self._trial_data = data
                return
            
            # Обновляем контрольную сумму
            data['checksum'] = self._calculate_checksum(data)
            
            # Создаем директорию если не существует
            self.trial_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Атомарная запись
            temp_file = self.trial_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Переименовываем
            temp_file.replace(self.trial_file)
            
            # На Windows делаем файл скрытым
            if os.name == 'nt':
                try:
                    os.system(f'attrib +h +s "{self.trial_file}"')
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Failed to save trial data: {e}")
            self._trial_data = data
    
    def _get_current_hwid(self) -> str:
        """Получение текущего HWID"""
        try:
            from ..core.hwid import hwid_generator
            return hwid_generator.generate()
        except:
            return "unknown_hwid"
    
    def _add_violation(self, reason: str):
        """Добавление нарушения"""
        try:
            self._violation_count += 1
            logger.warning(f"Security violation #{self._violation_count}: {reason}")
            
            # Сохраняем в данные триала
            trial_data = self._load_trial_data()
            trial_data['violation_count'] = trial_data.get('violation_count', 0) + 1
            trial_data['last_violation'] = reason
            trial_data['last_violation_time'] = datetime.now().isoformat()
            self._save_trial_data(trial_data)
            
            # Блокируем после 3 нарушений
            if self._violation_count >= 3:
                self._block_user(f"Multiple violations: {reason}")
                
        except Exception as e:
            logger.error(f"Error adding violation: {e}")
    
    def _block_user(self, reason: str):
        """Блокировка пользователя"""
        try:
            logger.critical(f"Blocking user: {reason}")
            
            from ..runtime.block_state import block_state
            block_state.block_device(f"Trial violations: {reason}")
            
            # Удаляем файл триала
            if self.trial_file and self.trial_file.exists():
                try:
                    os.remove(self.trial_file)
                except:
                    pass
            
        except Exception as e:
            logger.error(f"Error blocking user: {e}")
    
    def start_trial_session(self) -> bool:
        """Запуск триальной сессии с проверками безопасности"""
        try:
            trial_data = self._load_trial_data()
            
            # Устанавливаем время начала
            if not hasattr(self, '_start_time') or self._start_time is None:
                self._start_time = trial_data.get('start_timestamp', time.time())
            
            # Проверяем на попытки обмана
            self._check_for_cheating()
            
            # Проверяем не истек ли триал
            if self.is_trial_expired():
                logger.warning("Trial period expired")
                return False
            
            # Обновляем статистику
            trial_data['usage_count'] = trial_data.get('usage_count', 0) + 1
            trial_data['last_access'] = datetime.now().isoformat()
            
            self._save_trial_data(trial_data)
            self._trial_data = trial_data
            
            remaining = self.get_remaining_time()
            logger.info(f"Trial session started - {remaining:.1f}s remaining")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start trial session: {e}")
            return False
    
    def _check_for_cheating(self):
        """Проверка на попытки обмана"""
        try:
            current_time = time.time()
            
            # Проверка на откат времени
            if current_time < self._last_check_time - 2:  # Допуск 2 секунды
                self._add_violation("System time rollback detected")
            
            # Проверка на слишком быстрое время
            expected_min_time = self._last_check_time + 0.05  # Минимум 50мс между проверками
            if current_time < expected_min_time and self._last_check_time > 0:
                self._add_violation("Suspicious time acceleration")
            
            self._last_check_time = current_time
            
        except Exception as e:
            logger.debug(f"Error in cheating check: {e}")
    
    def is_trial_expired(self) -> bool:
        """Проверка истечения триального периода"""
        try:
            if not hasattr(self, '_start_time') or self._start_time is None:
                trial_data = self._load_trial_data()
                self._start_time = trial_data.get('start_timestamp', time.time())
            
            elapsed = time.time() - self._start_time
            expired = elapsed >= self.trial_duration
            
            if expired:
                logger.info(f"Trial expired: {elapsed:.1f}s >= {self.trial_duration}s")
            
            return expired
            
        except Exception as e:
            logger.error(f"Error checking trial expiration: {e}")
            return True
    
    def get_remaining_time(self) -> float:
        """Получение оставшегося времени триала"""
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
    
    def check_continuous_usage(self) -> bool:
        """Проверка на непрерывное использование с защитой от обмана"""
        try:
            # Проверяем на обман
            self._check_for_cheating()
            
            # Проверяем блокировку
            try:
                from ..runtime.block_state import block_state
                if block_state.is_blocked():
                    return False
            except:
                pass
            
            # Проверяем истечение
            if self.is_trial_expired():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in continuous usage check: {e}")
            return False
    
    def get_trial_info(self) -> Dict[str, Any]:
        """Получение полной информации о триале"""
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
                'violation_count': trial_data.get('violation_count', 0),
                'hwid': trial_data.get('hwid', 'unknown')[:8] + '...',
                'file_location': str(self.trial_file) if self.trial_file else 'memory',
                'last_violation': trial_data.get('last_violation'),
                'protection_active': self._violation_count < 3
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
                self._violation_count = 0
                logger.info("Trial period reset (DEV MODE)")
                self._create_new_trial()
            else:
                logger.warning("Trial reset denied - not in DEV mode")
                
        except Exception as e:
            logger.error(f"Failed to reset trial: {e}")

# Глобальный экземпляр менеджера триала
trial_manager = TrialManager()

# Удобные функции
def start_trial() -> bool:
    return trial_manager.start_trial_session()

def is_trial_active() -> bool:
    return not trial_manager.is_trial_expired()

def get_trial_time_remaining() -> float:
    return trial_manager.get_remaining_time()

def get_trial_status() -> Dict[str, Any]:
    return trial_manager.get_trial_info()

def reset_trial_period():
    trial_manager.reset_trial()