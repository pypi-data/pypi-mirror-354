#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Configuration System
===============================

Система конфигурации для красивой и умной валидации
"""

from typing import Dict, Any, Optional, Union
import os
from enum import Enum

class Language(Enum):
    """Поддерживаемые языки"""
    RUSSIAN = "ru"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    FRENCH = "fr"
    CHINESE = "zh"

class MessageStyle(Enum):
    """Стили сообщений"""
    FRIENDLY = "friendly"      # Дружелюбный стиль
    STRICT = "strict"          # Строгий стиль
    MINIMAL = "minimal"        # Минимальный стиль
    PROFESSIONAL = "professional"  # Профессиональный стиль

class ColorTheme(Enum):
    """Цветовые темы"""
    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    COLORFUL = "colorful"
    MONOCHROME = "monochrome"

class PyDefenderConfig:
    """
    Главный класс конфигурации PyDefender
    
    Управляет всеми настройками поведения библиотеки
    """
    
    def __init__(self):
        """Инициализация с настройками по умолчанию"""
        
        # === ОСНОВНЫЕ НАСТРОЙКИ ===
        self.language = Language.RUSSIAN
        self.message_style = MessageStyle.FRIENDLY
        self.color_theme = ColorTheme.DEFAULT
        
        # === ПОВЕДЕНИЕ ===
        self.show_colors = True           # Показывать цвета в сообщениях
        self.show_emojis = True           # Показывать эмодзи
        self.auto_retry = True            # Автоматически переспрашивать при ошибках
        self.max_attempts = 3             # Максимум попыток ввода
        self.suggest_corrections = True   # Предлагать исправления
        
        # === АВТОИСПРАВЛЕНИЯ ===
        self.auto_trim = True             # Автоматически убирать пробелы
        self.auto_capitalize = True       # Автоматически делать заглавные буквы
        self.auto_convert_types = True    # Автоматически конвертировать типы
        self.extract_numbers = True       # Извлекать числа из текста
        
        # === UI И ОТОБРАЖЕНИЕ ===
        self.console_width = 80           # Ширина консоли для форматирования
        self.show_progress = True         # Показывать прогресс валидации
        self.animation_speed = 0.1        # Скорость анимации (секунды)
        
        # === БЕЗОПАСНОСТЬ ===
        self.sanitize_input = True        # Очищать входные данные
        self.log_attempts = False         # Логировать попытки валидации
        self.strict_mode = False          # Строгий режим (больше проверок)
        
        # === ПРОИЗВОДИТЕЛЬНОСТЬ ===
        self.cache_validators = True      # Кешировать валидаторы
        self.async_validation = False     # Асинхронная валидация
        self.batch_size = 100            # Размер пакета для массовой валидации
        
        # === ИНТЕГРАЦИИ ===
        self.web_framework = None         # Flask, Django, FastAPI
        self.ui_framework = None          # Tkinter, Qt, Web
        self.database_integration = False # Интеграция с БД
    
    def set_language(self, language: Union[Language, str]) -> 'PyDefenderConfig':
        """
        Установить язык сообщений
        
        Args:
            language: Язык (Language enum или строка)
            
        Returns:
            self для цепочки вызовов
        """
        if isinstance(language, str):
            try:
                language = Language(language.lower())
            except ValueError:
                raise ValueError(f"Неподдерживаемый язык: {language}")
        
        self.language = language
        return self
    
    def set_style(self, style: Union[MessageStyle, str]) -> 'PyDefenderConfig':
        """
        Установить стиль сообщений
        
        Args:
            style: Стиль сообщений
            
        Returns:
            self для цепочки вызовов
        """
        if isinstance(style, str):
            try:
                style = MessageStyle(style.lower())
            except ValueError:
                raise ValueError(f"Неподдерживаемый стиль: {style}")
        
        self.message_style = style
        return self
    
    def set_colors(self, enabled: bool) -> 'PyDefenderConfig':
        """
        Включить/выключить цвета
        
        Args:
            enabled: Показывать ли цвета
            
        Returns:
            self для цепочки вызовов
        """
        self.show_colors = enabled
        return self
    
    def set_emojis(self, enabled: bool) -> 'PyDefenderConfig':
        """
        Включить/выключить эмодзи
        
        Args:
            enabled: Показывать ли эмодзи
            
        Returns:
            self для цепочки вызовов
        """
        self.show_emojis = enabled
        return self
    
    def set_auto_retry(self, enabled: bool, max_attempts: int = 3) -> 'PyDefenderConfig':
        """
        Настроить автоматические повторы
        
        Args:
            enabled: Включить автоповторы
            max_attempts: Максимум попыток
            
        Returns:
            self для цепочки вызовов
        """
        self.auto_retry = enabled
        self.max_attempts = max_attempts
        return self
    
    def set_auto_corrections(self, 
                           trim: bool = True,
                           capitalize: bool = True, 
                           convert_types: bool = True,
                           extract_numbers: bool = True) -> 'PyDefenderConfig':
        """
        Настроить автоисправления
        
        Args:
            trim: Убирать пробелы
            capitalize: Делать заглавные буквы
            convert_types: Конвертировать типы
            extract_numbers: Извлекать числа
            
        Returns:
            self для цепочки вызовов
        """
        self.auto_trim = trim
        self.auto_capitalize = capitalize
        self.auto_convert_types = convert_types
        self.extract_numbers = extract_numbers
        return self
    
    def enable_strict_mode(self) -> 'PyDefenderConfig':
        """
        Включить строгий режим (больше проверок)
        
        Returns:
            self для цепочки вызовов
        """
        self.strict_mode = True
        self.sanitize_input = True
        self.log_attempts = True
        self.suggest_corrections = False
        return self
    
    def enable_developer_mode(self) -> 'PyDefenderConfig':
        """
        Включить режим разработчика (максимум информации)
        
        Returns:
            self для цепочки вызовов
        """
        self.show_colors = True
        self.show_emojis = True
        self.show_progress = True
        self.log_attempts = True
        self.suggest_corrections = True
        return self
    
    def enable_production_mode(self) -> 'PyDefenderConfig':
        """
        Включить продакшн режим (оптимизированный)
        
        Returns:
            self для цепочки вызовов
        """
        self.show_colors = False
        self.show_emojis = False
        self.show_progress = False
        self.animation_speed = 0
        self.cache_validators = True
        self.log_attempts = False
        return self
    
    def reset_to_defaults(self) -> 'PyDefenderConfig':
        """
        Сбросить все настройки к значениям по умолчанию
        
        Returns:
            self для цепочки вызовов
        """
        self.__init__()
        return self
    
    def load_from_env(self) -> 'PyDefenderConfig':
        """
        Загрузить настройки из переменных окружения
        
        Поддерживаемые переменные:
        - PYDEFENDER_LANGUAGE
        - PYDEFENDER_STYLE
        - PYDEFENDER_COLORS
        - PYDEFENDER_EMOJIS
        - PYDEFENDER_STRICT_MODE
        
        Returns:
            self для цепочки вызовов
        """
        # Язык
        env_lang = os.getenv('PYDEFENDER_LANGUAGE')
        if env_lang:
            try:
                self.set_language(env_lang)
            except ValueError:
                pass  # Игнорируем неверные значения
        
        # Стиль
        env_style = os.getenv('PYDEFENDER_STYLE')
        if env_style:
            try:
                self.set_style(env_style)
            except ValueError:
                pass
        
        # Цвета
        env_colors = os.getenv('PYDEFENDER_COLORS')
        if env_colors:
            self.show_colors = env_colors.lower() in ('true', '1', 'yes', 'on')
        
        # Эмодзи
        env_emojis = os.getenv('PYDEFENDER_EMOJIS')
        if env_emojis:
            self.show_emojis = env_emojis.lower() in ('true', '1', 'yes', 'on')
        
        # Строгий режим
        env_strict = os.getenv('PYDEFENDER_STRICT_MODE')
        if env_strict and env_strict.lower() in ('true', '1', 'yes', 'on'):
            self.enable_strict_mode()
        
        return self
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Получить все текущие настройки
        
        Returns:
            Словарь со всеми настройками
        """
        return {
            # Основные
            'language': self.language.value,
            'message_style': self.message_style.value,
            'color_theme': self.color_theme.value,
            
            # Поведение
            'show_colors': self.show_colors,
            'show_emojis': self.show_emojis,
            'auto_retry': self.auto_retry,
            'max_attempts': self.max_attempts,
            'suggest_corrections': self.suggest_corrections,
            
            # Автоисправления
            'auto_trim': self.auto_trim,
            'auto_capitalize': self.auto_capitalize,
            'auto_convert_types': self.auto_convert_types,
            'extract_numbers': self.extract_numbers,
            
            # UI
            'console_width': self.console_width,
            'show_progress': self.show_progress,
            'animation_speed': self.animation_speed,
            
            # Безопасность
            'sanitize_input': self.sanitize_input,
            'log_attempts': self.log_attempts,
            'strict_mode': self.strict_mode,
            
            # Производительность
            'cache_validators': self.cache_validators,
            'async_validation': self.async_validation,
            'batch_size': self.batch_size,
        }
    
    def __str__(self) -> str:
        """Строковое представление конфигурации"""
        settings = self.get_all_settings()
        lines = ["🛡️ PyDefender Configuration:"]
        
        for category, items in [
            ("Основные", ['language', 'message_style', 'color_theme']),
            ("Поведение", ['show_colors', 'show_emojis', 'auto_retry', 'max_attempts']),
            ("Автоисправления", ['auto_trim', 'auto_capitalize', 'auto_convert_types']),
            ("Безопасность", ['sanitize_input', 'strict_mode']),
        ]:
            lines.append(f"\n📁 {category}:")
            for item in items:
                if item in settings:
                    lines.append(f"  • {item}: {settings[item]}")
        
        return "\n".join(lines)

# === ГЛОБАЛЬНАЯ КОНФИГУРАЦИЯ ===
_global_config = PyDefenderConfig()

def configure(**kwargs) -> PyDefenderConfig:
    """
    Быстрая настройка PyDefender
    
    Args:
        **kwargs: Параметры конфигурации
            language: Язык ("ru", "en", etc.)
            style: Стиль сообщений ("friendly", "strict", etc.)
            colors: Показывать цвета (True/False)
            emojis: Показывать эмодзи (True/False)
            auto_retry: Автоповторы (True/False)
            max_attempts: Максимум попыток (int)
            strict_mode: Строгий режим (True/False)
    
    Returns:
        Объект конфигурации
        
    Examples:
        >>> configure(language="en", colors=False)
        >>> configure(strict_mode=True, max_attempts=5)
        >>> configure(style="minimal", emojis=False)
    """
    global _global_config
    
    # Основные настройки
    if 'language' in kwargs:
        _global_config.set_language(kwargs['language'])
    
    if 'style' in kwargs:
        _global_config.set_style(kwargs['style'])
    
    if 'colors' in kwargs:
        _global_config.set_colors(kwargs['colors'])
    
    if 'emojis' in kwargs:
        _global_config.set_emojis(kwargs['emojis'])
    
    # Поведение
    if 'auto_retry' in kwargs or 'max_attempts' in kwargs:
        auto_retry = kwargs.get('auto_retry', _global_config.auto_retry)
        max_attempts = kwargs.get('max_attempts', _global_config.max_attempts)
        _global_config.set_auto_retry(auto_retry, max_attempts)
    
    # Автоисправления
    auto_corrections = {}
    for key in ['auto_trim', 'auto_capitalize', 'auto_convert_types', 'extract_numbers']:
        if key in kwargs:
            auto_corrections[key.replace('auto_', '')] = kwargs[key]
    
    if auto_corrections:
        _global_config.set_auto_corrections(**auto_corrections)
    
    # Специальные режимы
    if kwargs.get('strict_mode'):
        _global_config.enable_strict_mode()
    
    if kwargs.get('developer_mode'):
        _global_config.enable_developer_mode()
    
    if kwargs.get('production_mode'):
        _global_config.enable_production_mode()
    
    # Прямые настройки
    for key, value in kwargs.items():
        if hasattr(_global_config, key):
            setattr(_global_config, key, value)
    
    return _global_config

def get_config() -> PyDefenderConfig:
    """
    Получить текущую глобальную конфигурацию
    
    Returns:
        Объект конфигурации
    """
    return _global_config

def reset_config():
    """Сбросить конфигурацию к значениям по умолчанию"""
    global _global_config
    _global_config.reset_to_defaults()

# === ПРЕДУСТАНОВЛЕННЫЕ КОНФИГУРАЦИИ ===

def get_russian_config() -> PyDefenderConfig:
    """Конфигурация для русскоязычных пользователей"""
    config = PyDefenderConfig()
    config.set_language("ru")
    config.set_style("friendly")
    config.show_emojis = True
    config.show_colors = True
    return config

def get_english_config() -> PyDefenderConfig:
    """Конфигурация для англоязычных пользователей"""
    config = PyDefenderConfig()
    config.set_language("en")
    config.set_style("professional")
    config.show_emojis = False
    config.show_colors = True
    return config

def get_developer_config() -> PyDefenderConfig:
    """Конфигурация для разработчиков"""
    config = PyDefenderConfig()
    config.enable_developer_mode()
    config.log_attempts = True
    config.suggest_corrections = True
    return config

def get_production_config() -> PyDefenderConfig:
    """Конфигурация для продакшена"""
    config = PyDefenderConfig()
    config.enable_production_mode()
    config.strict_mode = True
    config.sanitize_input = True
    return config

# Автоматическая загрузка из переменных окружения при импорте
_global_config.load_from_env()