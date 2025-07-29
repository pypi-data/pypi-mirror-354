"""
Kilopa - Библиотека защиты Python-приложений
Автоматически запускает защиту при импорте
"""

import os
import sys

# Проверка режима разработки
DEV_MODE = os.getenv('KILO_DEV_MODE', '0') == '1'

if not DEV_MODE:
    # Импорт и автоматический запуск защиты
    try:
        from .run import auto_protect
        auto_protect()
    except Exception as e:
        # Если защита не прошла - завершаем программу
        print(f"Ошибка инициализации защиты: {e}")
        sys.exit(1)

# Экспорт публичных функций (если нужно)
__version__ = "1.0.0"
__author__ = "Kilopa Security"

# Минимальный публичный API
def get_version():
    """Получить версию библиотеки"""
    return __version__

def is_protected():
    """Проверить, активирована ли защита"""
    return not DEV_MODE