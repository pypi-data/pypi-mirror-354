"""
Окно истечения срока лицензии
"""

import sys
import tkinter as tk
from tkinter import ttk
from ..tools.logger import log_info, log_error

class ExpiredWindow:
    """Окно истечения лицензии"""
    
    def __init__(self, validation_result=None):
        self.validation_result = validation_result
        self.root = None
        
    def show(self):
        """Показать окно истечения"""
        try:
            self.root = tk.Tk()
            self._setup_window()
            self._create_widgets()
            self._center_window()
            
            log_info("Отображено окно истечения лицензии")
            
            # Запускаем главный цикл
            self.root.mainloop()
            
        except Exception as e:
            log_error(f"Ошибка отображения окна истечения: {e}")
            self._fallback_console_message()
    
    def _setup_window(self):
        """Настроить главное окно"""
        self.root.title("Kilopa - Лицензия истекла")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        
        # Цвет фона
        self.root.configure(bg="#fff8e1")
        
        # Обработчик закрытия
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Всегда наверху
        self.root.attributes("-topmost", True)
    
    def _create_widgets(self):
        """Создать виджеты интерфейса"""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Иконка
        icon_label = ttk.Label(main_frame, text="⏰", font=("Arial", 48))
        icon_label.grid(row=0, column=0, pady=(0, 10))
        
        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="СРОК ЛИЦЕНЗИИ ИСТЁК",
            font=("Arial", 16, "bold"),
            foreground="#f57c00"
        )
        title_label.grid(row=1, column=0, pady=(0, 20))
        
        # Основное сообщение
        message = self._get_expiration_message()
        message_label = ttk.Label(
            main_frame,
            text=message,
            font=("Arial", 11),
            justify=tk.CENTER,
            wraplength=350
        )
        message_label.grid(row=2, column=0, pady=(0, 20))
        
        # Информация о лицензии
        self._create_license_info(main_frame)
        
        # Кнопки
        self._create_buttons(main_frame)
        
        # Настройка веса
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _create_license_info(self, parent):
        """Создать информацию о лицензии"""
        info_frame = ttk.LabelFrame(parent, text="Информация о лицензии", padding="15")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        try:
            # Получаем информацию о лицензии
            results = self.validation_result.get('results', {}) if self.validation_result else {}
            license_result = results.get('license', {})
            license_info = license_result.get('license_info', {})
            license_data = license_info.get('data', {}) if license_info else {}
            
            # Информация
            info_text = []
            
            # Статус
            status = license_result.get('status', 'unknown')
            info_text.append(f"Статус: {self._get_status_text(status)}")
            
            # Дата истечения
            expires_at = license_data.get('expires_at')
            if expires_at:
                import datetime
                try:
                    expire_date = datetime.datetime.fromtimestamp(expires_at)
                    info_text.append(f"Истекла: {expire_date.strftime('%d.%m.%Y')}")
                    
                    # Сколько дней назад истекла
                    current_date = datetime.datetime.now()
                    days_expired = (current_date - expire_date).days
                    if days_expired > 0:
                        info_text.append(f"Дней назад: {days_expired}")
                except:
                    info_text.append("Дата истечения: Неизвестна")
            
            # Тип лицензии
            features = license_data.get('features', [])
            if features:
                info_text.append(f"Функции: {', '.join(features)}")
            
            # Пользователь
            user_info = license_data.get('user_info', {})
            if user_info.get('email'):
                info_text.append(f"Email: {user_info['email']}")
            
            info_label = ttk.Label(
                info_frame,
                text="\n".join(info_text),
                font=("Courier", 9),
                justify=tk.LEFT
            )
            info_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
        except Exception as e:
            error_label = ttk.Label(
                info_frame,
                text=f"Ошибка получения информации: {e}",
                foreground="red"
            )
            error_label.grid(row=0, column=0)
        
        info_frame.columnconfigure(0, weight=1)
    
    def _create_buttons(self, parent):
        """Создать кнопки"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        # Кнопка обновления лицензии
        renew_button = ttk.Button(
            button_frame,
            text="Обновить лицензию",
            command=self._renew_license,
            width=18
        )
        renew_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка выхода
        exit_button = ttk.Button(
            button_frame,
            text="Выход",
            command=self._on_close,
            width=12
        )
        exit_button.pack(side=tk.LEFT)
    
    def _get_expiration_message(self):
        """Получить сообщение об истечении"""
        try:
            # Основное сообщение
            message = ("Срок действия вашей лицензии истёк.\n\n"
                      "Для продолжения работы с приложением требуется "
                      "обновление лицензии.\n\n"
                      "Обратитесь к поставщику программного обеспечения "
                      "для получения новой лицензии.")
            
            return message
            
        except:
            return ("Срок действия лицензии истёк.\n\n"
                   "Требуется обновление лицензии.")
    
    def _get_status_text(self, status):
        """Получить текстовое описание статуса"""
        status_texts = {
            'expired': 'Истекла',
            'invalid': 'Недействительна',
            'revoked': 'Отозвана',
            'no_license': 'Отсутствует',
            'error': 'Ошибка'
        }
        
        return status_texts.get(status, 'Неизвестно')
    
    def _center_window(self):
        """Центрировать окно на экране"""
        try:
            self.root.update_idletasks()
            
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
        except Exception:
            pass
    
    def _renew_license(self):
        """Обновить лицензию"""
        try:
            log_info("Пользователь запросил обновление лицензии")
            
            # Закрываем текущее окно
            self.root.destroy()
            
            # Показываем окно активации
            from .auth_window import show_activation_window
            show_activation_window(self.validation_result)
            
        except Exception as e:
            log_error(f"Ошибка обновления лицензии: {e}")
            self._on_close()
    
    def _on_close(self):
        """Обработчик закрытия окна"""
        try:
            log_info("Окно истечения лицензии закрыто")
            
            self.root.quit()
            self.root.destroy()
            
            # Завершаем программу
            sys.exit(1)
            
        except Exception:
            sys.exit(1)
    
    def _fallback_console_message(self):
        """Консольное сообщение как fallback"""
        try:
            print(f"\n{'='*50}")
            print("KILOPA SECURITY SYSTEM")
            print(f"{'='*50}")
            print("⏰ СРОК ЛИЦЕНЗИИ ИСТЁК")
            print(f"{'='*50}")
            print("Срок действия вашей лицензии истёк.")
            print("Для продолжения работы требуется обновление.")
            print()
            
            # Показываем информацию о лицензии
            try:
                results = self.validation_result.get('results', {}) if self.validation_result else {}
                license_result = results.get('license', {})
                license_info = license_result.get('license_info', {})
                license_data = license_info.get('data', {}) if license_info else {}
                
                expires_at = license_data.get('expires_at')
                if expires_at:
                    import datetime
                    try:
                        expire_date = datetime.datetime.fromtimestamp(expires_at)
                        print(f"Дата истечения: {expire_date.strftime('%d.%m.%Y %H:%M')}")
                        
                        days_expired = (datetime.datetime.now() - expire_date).days
                        if days_expired > 0:
                            print(f"Истекла {days_expired} дней назад")
                    except:
                        print("Дата истечения: Неизвестна")
                
                user_info = license_data.get('user_info', {})
                if user_info.get('email'):
                    print(f"Пользователь: {user_info['email']}")
                    
            except:
                pass
            
            print(f"\n{'='*50}")
            print("Обратитесь к поставщику для получения новой лицензии.")
            print(f"{'='*50}\n")
            
        except Exception:
            print("⏰ СРОК ЛИЦЕНЗИИ ИСТЁК - Обратитесь к администратору")
        
        finally:
            sys.exit(1)

def show_expired_window(validation_result=None):
    """Показать окно истечения лицензии"""
    try:
        window = ExpiredWindow(validation_result)
        window.show()
    except Exception as e:
        log_error(f"Ошибка создания окна истечения: {e}")
        sys.exit(1)