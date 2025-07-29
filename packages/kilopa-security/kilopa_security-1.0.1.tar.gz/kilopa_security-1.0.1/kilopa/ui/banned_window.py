"""
Окна блокировки и различных ошибок безопасности
"""

import sys
import tkinter as tk
from tkinter import ttk
from ..tools.logger import log_info, log_error

class BannedWindow:
    """Окно блокировки пользователя"""
    
    def __init__(self, validation_result=None, window_type="banned"):
        self.validation_result = validation_result
        self.window_type = window_type
        self.root = None
        
    def show(self):
        """Показать окно блокировки"""
        try:
            self.root = tk.Tk()
            self._setup_window()
            self._create_widgets()
            self._center_window()
            
            log_info(f"Отображено окно блокировки типа: {self.window_type}")
            
            # Запускаем главный цикл
            self.root.mainloop()
            
        except Exception as e:
            log_error(f"Ошибка отображения окна блокировки: {e}")
            self._fallback_console_message()
    
    def _setup_window(self):
        """Настроить главное окно"""
        titles = {
            "banned": "Kilopa - Доступ заблокирован",
            "security_violation": "Kilopa - Нарушение безопасности", 
            "license_error": "Kilopa - Ошибка лицензии",
            "generic_error": "Kilopa - Ошибка"
        }
        
        self.root.title(titles.get(self.window_type, "Kilopa - Ошибка"))
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Цвет фона в зависимости от типа
        bg_colors = {
            "banned": "#ffebee",
            "security_violation": "#fff3e0", 
            "license_error": "#f3e5f5",
            "generic_error": "#fafafa"
        }
        
        self.root.configure(bg=bg_colors.get(self.window_type, "#fafafa"))
        
        # Обработчик закрытия
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Делаем окно всегда наверху
        self.root.attributes("-topmost", True)
    
    def _create_widgets(self):
        """Создать виджеты интерфейса"""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Иконка и заголовок
        self._create_header(main_frame)
        
        # Основное сообщение
        self._create_message(main_frame)
        
        # Дополнительная информация
        self._create_details(main_frame)
        
        # Кнопки
        self._create_buttons(main_frame)
        
        # Настройка веса
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _create_header(self, parent):
        """Создать заголовок"""
        # Иконки для разных типов
        icons = {
            "banned": "🚫",
            "security_violation": "⚠️",
            "license_error": "🔒",
            "generic_error": "❌"
        }
        
        titles = {
            "banned": "ДОСТУП ЗАБЛОКИРОВАН",
            "security_violation": "НАРУШЕНИЕ БЕЗОПАСНОСТИ",
            "license_error": "ОШИБКА ЛИЦЕНЗИИ", 
            "generic_error": "ОШИБКА"
        }
        
        icon = icons.get(self.window_type, "❌")
        title = titles.get(self.window_type, "ОШИБКА")
        
        # Иконка
        icon_label = ttk.Label(parent, text=icon, font=("Arial", 48))
        icon_label.grid(row=0, column=0, pady=(0, 10))
        
        # Заголовок
        title_label = ttk.Label(
            parent, 
            text=title,
            font=("Arial", 16, "bold"),
            foreground="red"
        )
        title_label.grid(row=1, column=0, pady=(0, 20))
    
    def _create_message(self, parent):
        """Создать основное сообщение"""
        messages = {
            "banned": self._get_banned_message(),
            "security_violation": self._get_security_message(),
            "license_error": self._get_license_error_message(),
            "generic_error": self._get_generic_error_message()
        }
        
        message = messages.get(self.window_type, "Произошла ошибка.")
        
        message_label = ttk.Label(
            parent,
            text=message,
            font=("Arial", 11),
            justify=tk.CENTER,
            wraplength=400
        )
        message_label.grid(row=2, column=0, pady=(0, 20))
    
    def _create_details(self, parent):
        """Создать детали ошибки"""
        details_frame = ttk.LabelFrame(parent, text="Подробности", padding="10")
        details_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        details_text = self._get_details_text()
        
        details_label = ttk.Label(
            details_frame,
            text=details_text,
            font=("Courier", 9),
            justify=tk.LEFT,
            wraplength=400
        )
        details_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        details_frame.columnconfigure(0, weight=1)
    
    def _create_buttons(self, parent):
        """Создать кнопки"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        # Кнопка закрытия
        close_button = ttk.Button(
            button_frame,
            text="Закрыть",
            command=self._on_close,
            width=15
        )
        close_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Дополнительные кнопки в зависимости от типа
        if self.window_type == "license_error":
            retry_button = ttk.Button(
                button_frame,
                text="Повторить активацию",
                command=self._retry_activation,
                width=20
            )
            retry_button.pack(side=tk.LEFT)
    
    def _get_banned_message(self):
        """Получить сообщение о блокировке"""
        try:
            failure_type = self.validation_result.get('failure_type', 'unknown')
            
            if failure_type == 'user_banned':
                return ("Ваш аккаунт заблокирован из-за множественных нарушений.\n\n"
                       "Обратитесь к администратору для разблокировки.")
            
            elif failure_type == 'ip_blocked':
                return ("Ваш IP-адрес заблокирован.\n\n"
                       "Доступ запрещён с данного местоположения.")
            
            elif failure_type == 'too_many_warnings':
                return ("Превышено максимальное количество предупреждений.\n\n"
                       "Ваш аккаунт автоматически заблокирован.")
            
            else:
                return "Доступ к приложению заблокирован.\n\nОбратитесь к администратору."
                
        except:
            return "Доступ заблокирован по соображениям безопасности."
    
    def _get_security_message(self):
        """Получить сообщение о нарушении безопасности"""
        try:
            failure_type = self.validation_result.get('failure_type', 'unknown')
            
            if failure_type == 'tamper_detected':
                return ("Обнаружена попытка модификации защищённых файлов.\n\n"
                       "Работа приложения прекращена для обеспечения безопасности.")
            
            elif failure_type == 'time_rollback':
                return ("Обнаружен откат системного времени.\n\n"
                       "Это может указывать на попытку обхода защиты.")
            
            else:
                return ("Обнаружено нарушение безопасности.\n\n"
                       "Работа приложения прекращена.")
                
        except:
            return "Обнаружено критическое нарушение безопасности."
    
    def _get_license_error_message(self):
        """Получить сообщение об ошибке лицензии"""
        try:
            results = self.validation_result.get('results', {})
            license_result = results.get('license', {})
            license_status = license_result.get('status', 'unknown')
            
            if license_status == 'revoked':
                return ("Ваша лицензия была отозвана.\n\n"
                       "Обратитесь к поставщику для получения новой лицензии.")
            
            elif license_status == 'invalid':
                return ("Лицензия недействительна или повреждена.\n\n"
                       "Требуется повторная активация.")
            
            else:
                return ("Произошла ошибка при проверке лицензии.\n\n"
                       "Обратитесь в службу поддержки.")
                
        except:
            return "Ошибка лицензии. Обратитесь в службу поддержки."
    
    def _get_generic_error_message(self):
        """Получить общее сообщение об ошибке"""
        try:
            message = self.validation_result.get('message', 'Произошла неизвестная ошибка.')
            return f"Произошла критическая ошибка:\n\n{message