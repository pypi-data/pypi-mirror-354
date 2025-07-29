"""
Загрузчик пользовательского интерфейса
"""

import sys
from ..config import get_setting
from ..tools.logger import log_info, log_warning, log_error

def show_ui_based_on_result(validation_result):
    """Показать соответствующий UI на основе результата валидации"""
    try:
        if not get_setting('ui_enabled', True):
            log_info("UI отключён в настройках")
            return
        
        if not validation_result:
            log_error("Нет результата валидации для отображения UI")
            sys.exit(1)
        
        status = validation_result.get('status')
        failure_type = validation_result.get('failure_type')
        
        if status == 'success':
            # Всё в порядке, UI не нужен
            log_info("Валидация прошла успешно, UI не требуется")
            return
        
        elif status == 'failure':
            # Определяем тип ошибки и показываем соответствующее окно
            if failure_type == 'license_invalid':
                _handle_license_issues(validation_result)
            
            elif failure_type in ['user_banned', 'ip_blocked', 'too_many_warnings']:
                _show_banned_window(validation_result)
            
            elif failure_type in ['tamper_detected', 'time_rollback']:
                _show_security_violation_window(validation_result)
            
            else:
                _show_generic_error_window(validation_result)
        
        else:
            log_error(f"Неизвестный статус валидации: {status}")
            sys.exit(1)
            
    except Exception as e:
        log_error(f"Ошибка отображения UI: {e}")
        sys.exit(1)

def _handle_license_issues(validation_result):
    """Обработать проблемы с лицензией"""
    try:
        # Анализируем детали проблемы с лицензией
        results = validation_result.get('results', {})
        license_result = results.get('license', {})
        license_status = license_result.get('status')
        
        if license_status == 'no_license':
            _show_activation_window(validation_result)
        
        elif license_status == 'expired':
            _show_expired_window(validation_result)
        
        elif license_status in ['invalid', 'revoked']:
            _show_license_error_window(validation_result)
        
        else:
            _show_activation_window(validation_result)
            
    except Exception as e:
        log_error(f"Ошибка обработки проблем с лицензией: {e}")
        _show_activation_window(validation_result)

def _show_activation_window(validation_result):
    """Показать окно активации"""
    try:
        log_info("Отображение окна активации лицензии")
        
        from .auth_window import show_activation_window
        show_activation_window(validation_result)
        
    except ImportError:
        log_error("Не удалось импортировать окно активации")
        _show_console_message("Требуется активация лицензии")
        sys.exit(1)
    except Exception as e:
        log_error(f"Ошибка отображения окна активации: {e}")
        _show_console_message("Требуется активация лицензии")
        sys.exit(1)

def _show_expired_window(validation_result):
    """Показать окно истечения лицензии"""
    try:
        log_info("Отображение окна истечения лицензии")
        
        from .expired_window import show_expired_window
        show_expired_window(validation_result)
        
    except ImportError:
        log_error("Не удалось импортировать окно истечения")
        _show_console_message("Срок действия лицензии истёк")
        sys.exit(1)
    except Exception as e:
        log_error(f"Ошибка отображения окна истечения: {e}")
        _show_console_message("Срок действия лицензии истёк")
        sys.exit(1)

def _show_banned_window(validation_result):
    """Показать окно блокировки"""
    try:
        log_info("Отображение окна блокировки")
        
        from .banned_window import show_banned_window
        show_banned_window(validation_result)
        
    except ImportError:
        log_error("Не удалось импортировать окно блокировки")
        _show_console_message("Доступ заблокирован")
        sys.exit(1)
    except Exception as e:
        log_error(f"Ошибка отображения окна блокировки: {e}")
        _show_console_message("Доступ заблокирован")
        sys.exit(1)

def _show_security_violation_window(validation_result):
    """Показать окно нарушения безопасности"""
    try:
        log_info("Отображение окна нарушения безопасности")
        
        # Используем окно блокировки для нарушений безопасности
        from .banned_window import show_security_violation_window
        show_security_violation_window(validation_result)
        
    except ImportError:
        log_error("Не удалось импортировать окно нарушения безопасности")
        _show_console_message("Обнаружено нарушение безопасности")
        sys.exit(1)
    except Exception as e:
        log_error(f"Ошибка отображения окна нарушения: {e}")
        _show_console_message("Обнаружено нарушение безопасности")
        sys.exit(1)

def _show_license_error_window(validation_result):
    """Показать окно ошибки лицензии"""
    try:
        log_info("Отображение окна ошибки лицензии")
        
        # Используем окно блокировки для ошибок лицензии
        from .banned_window import show_license_error_window
        show_license_error_window(validation_result)
        
    except ImportError:
        log_error("Не удалось импортировать окно ошибки лицензии")
        _show_console_message("Ошибка лицензии")
        sys.exit(1)
    except Exception as e:
        log_error(f"Ошибка отображения окна ошибки лицензии: {e}")
        _show_console_message("Ошибка лицензии")
        sys.exit(1)

def _show_generic_error_window(validation_result):
    """Показать общее окно ошибки"""
    try:
        log_info("Отображение общего окна ошибки")
        
        error_message = validation_result.get('message', 'Произошла ошибка')
        
        # Используем окно блокировки для общих ошибок
        from .banned_window import show_generic_error_window
        show_generic_error_window(validation_result)
        
    except ImportError:
        log_error("Не удалось импортировать окно ошибки")
        _show_console_message("Произошла ошибка")
        sys.exit(1)
    except Exception as e:
        log_error(f"Ошибка отображения окна ошибки: {e}")
        _show_console_message("Произ