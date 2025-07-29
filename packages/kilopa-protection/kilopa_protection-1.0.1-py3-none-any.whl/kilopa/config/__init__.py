"""
Модуль конфигурации системы защиты Kilopa
"""

from .constants import *
from .settings import settings, get_setting, set_setting, is_feature_enabled

# Экспорт основных компонентов
__all__ = [
    # Константы
    'VERSION', 'LIBRARY_NAME', 'LICENSE_FORMAT', 'PUBLIC_KEY_PEM',
    'API_BASE_URL', 'MAX_WARNINGS', 'MAX_ATTEMPTS', 'MESSAGES', 
    'STATUS_CODES', 'EVENTS',
    
    # Настройки
    'settings', 'get_setting', 'set_setting', 'is_feature_enabled'
]