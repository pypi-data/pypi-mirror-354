"""
Главный модуль запуска системы защиты
"""

import sys
from .core.validator import validate_all
from .ui.loader import show_ui_based_on_result
from .tools.logger import log_event
from .runtime.watchdog import check_import_presence
from .security.safe_exec import execute_safely

def auto_protect():
    """
    Главная функция защиты, запускается автоматически при импорте kilopa
    """
    try:
        log_event("INFO", "Запуск системы защиты Kilopa")
        
        # Проверка наличия импорта в основном коде
        if not check_import_presence():
            log_event("WARNING", "Не найден импорт kilopa в основном коде")
            from .runtime.attempt_counter import add_warning
            add_warning("missing_import")
        
        # Безопасное выполнение всех проверок
        def protection_logic():
            # Главная валидация всех компонентов
            result = validate_all()
            
            # Отображение соответствующего UI
            show_ui_based_on_result(result)
            
            return result
        
        # Выполняем защищённо
        result = execute_safely(protection_logic)
        
        if result and result.get('status') == 'success':
            log_event("INFO", "Защита пройдена успешно")
            return True
        else:
            log_event("ERROR", f"Защита не пройдена: {result}")
            sys.exit(1)
            
    except Exception as e:
        log_event("CRITICAL", f"Критическая ошибка в системе защиты: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Прямой запуск для тестирования
    auto_protect()