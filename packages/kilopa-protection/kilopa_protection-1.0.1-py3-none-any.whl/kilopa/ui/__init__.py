"""
Модуль пользовательского интерфейса Kilopa
"""

from .loader import (
    show_ui_based_on_result,
    check_ui_availability,
    show_warning_dialog,
    show_info_dialog,
    get_ui_theme,
    is_ui_enabled
)

from .auth_window import show_activation_window

from .banned_window import (
    show_banned_window,
    show_security_violation_window,
    show_license_error_window,
    show_generic_error_window
)

from .expired_window import show_expired_window

# Экспорт основных функций
__all__ = [
    # Основной загрузчик
    'show_ui_based_on_result',
    'check_ui_availability',
    'show_warning_dialog',
    'show_info_dialog',
    'get_ui_theme',
    'is_ui_enabled',
    
    # Окна
    'show_activation_window',
    'show_banned_window', 
    'show_security_violation_window',
    'show_license_error_window',
    'show_generic_error_window',
    'show_expired_window'
]