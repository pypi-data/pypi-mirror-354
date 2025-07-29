"""
Настройки системы защиты Kilopa
"""

import os
import json
from .constants import CONFIG_FILE, TEMP_DIR

class Settings:
    """Менеджер настроек системы защиты"""
    
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.temp_dir = TEMP_DIR
        self._settings = self._load_default_settings()
        self._load_from_file()
    
    def _load_default_settings(self):
        """Загрузка настроек по умолчанию"""
        return {
            # Основные настройки
            'strict_mode': True,
            'auto_update': True,
            'logging_enabled': True,
            'ui_enabled': True,
            
            # Настройки проверок
            'check_hwid': True,
            'check_ip': True,
            'check_time': True,
            'check_tamper': True,
            'check_debugger': True,
            
            # Сетевые настройки
            'online_validation': True,
            'offline_grace_period': 24,  # часов
            'api_timeout': 10,
            
            # Настройки безопасности
            'max_warnings': 3,
            'warning_reset_days': 30,
            'ban_duration_days': 365,
            'auto_delete_on_ban': False,
            
            # UI настройки
            'ui_theme': 'dark',
            'show_warnings': True,
            'show_debug_info': False,
            
            # Расширенные настройки
            'encryption_level': 'high',
            'signature_required': True,
            'time_tolerance_minutes': 5,
            'license_cache_hours': 1,
            
            # Антиотладочные настройки
            'anti_debug': {
                'enabled': True,
                'fake_responses': True,
                'crash_on_debug': False,
                'obfuscate_errors': True
            }
        }
    
    def _load_from_file(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_settings = json.load(f)
                    self._settings.update(file_settings)
        except Exception:
            # Если файл повреждён, используем настройки по умолчанию
            pass
    
    def save_to_file(self):
        """Сохранение настроек в файл"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get(self, key, default=None):
        """Получить значение настройки"""
        keys = key.split('.')
        value = self._settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Установить значение настройки"""
        keys = key.split('.')
        current = self._settings
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save_to_file()
    
    def is_enabled(self, feature):
        """Проверить, включена ли функция"""
        return self.get(feature, False)
    
    def get_all(self):
        """Получить все настройки"""
        return self._settings.copy()
    
    def reset_to_default(self):
        """Сброс к настройкам по умолчанию"""
        self._settings = self._load_default_settings()
        self.save_to_file()

# Глобальный экземпляр настроек
settings = Settings()

# Функции для быстрого доступа
def get_setting(key, default=None):
    """Получить настройку"""
    return settings.get(key, default)

def set_setting(key, value):
    """Установить настройку"""
    settings.set(key, value)

def is_feature_enabled(feature):
    """Проверить, включена ли функция"""
    return settings.is_enabled(feature)