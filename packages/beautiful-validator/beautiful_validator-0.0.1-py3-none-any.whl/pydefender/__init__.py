# Декораторы валидации (основной способ использования)
__all__ = [
    # === ОСНОВНЫЕ ДЕКОРАТОРЫ ===
    # Числа
    "number",           # Валидация чисел
    "positive_number",  # Положительные числа
    "integer",          # Целые числа
    "percentage",       # Проценты (0-100)
    "age",             # Возраст (0-150)
    "score",           # Оценки (0-10)
    "price",           # Цены (≥0, 2 знака)
    
    # Строки
    "string",           # Валидация строк
    "#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ PyDefender - Beautiful Smart Input Validation
=================================================

Самая красивая и умная библиотека валидации для Python!

Быстрый старт:
    import pydefender
    
    @pydefender.number(min_value=0, max_value=100)
    def set_score(score):
        return f"Счет: {score}"

Возможности:
    ✨ Красивые декораторы
    🧠 Умная валидация  
    🛠️ Автоисправления
    🌍 Мультиязычность
    🔧 Легкая интеграция
"""

__version__ = "0.0.1"
__author__ = "PyDefender Team"
__email__ = "team@pydefender.dev"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 PyDefender Team"

# === ИМПОРТЫ ===

# Конфигурация
from .config import (
    configure, get_config, reset_config,
    get_russian_config, get_english_config, 
    get_developer_config, get_production_config
)

# Исключения
from .exceptions import (
    PyDefenderError, ValidationError, NumberValidationError, 
    StringValidationError, EmailValidationError, PhoneValidationError,
    ConversionError, ConfigurationError, SecurityError, RetryLimitError
)

# Основные валидаторы
from .validators.numbers import (
    number, positive_number, integer, percentage, age, score, price,
    NumberValidator, PositiveNumberValidator, IntegerValidator,
    PercentageValidator, AgeValidator, ScoreValidator, PriceValidator
)

# Валидаторы строк
from .validators.strings import (
    string, text, name, username, comment,
    StringValidator, NameValidator, UsernameValidator, CommentValidator
)

# Декораторы
from .decorators import (
    ValidationDecorator, FormValidator, form_validator,
    ConditionalDecorator, conditional, RetryableDecorator, retryable,
    debug_validator, performance_monitor, silent_validator
)

# Утилиты
from .utils import (
    colorize, add_emoji, format_error_message, format_success_message,
    extract_numbers_from_string, extract_first_number, clean_string,
    suggest_similar_strings, Color, EmojiSet
)

# === ОСНОВНОЙ API ===

# Декораторы валидации (основной способ использования)
__all__ = [
    # === ОСНОВНЫЕ ДЕКОРАТОРЫ ===
    # Числа
    "number",           # Валидация чисел
    "positive_number",  # Положительные числа
    "integer",          # Целые числа
    "percentage",       # Проценты (0-100)
    "age",             # Возраст (0-150)
    "score",           # Оценки (0-10)
    "price",           # Цены (≥0, 2 знака)
    
    # Строки
    "string",           # Валидация строк
    "text",            # Алиас для string
    "name",            # Имена людей
    "username",        # Имена пользователей
    "comment",         # Комментарии
    
    # === КОНФИГУРАЦИЯ ===
    "configure",        # Настройка библиотеки
    "get_config",       # Получить текущие настройки
    "reset_config",     # Сбросить настройки
    "setup_for_beginners",     # Настройка для новичков
    "setup_for_professionals", # Настройка для профи
    "setup_for_production",    # Настройка для продакшена
    
    # === ИСКЛЮЧЕНИЯ ===
    "ValidationError",         # Основное исключение
    "NumberValidationError",   # Ошибки чисел
    "StringValidationError",   # Ошибки строк
    
    # === УТИЛИТЫ ===
    "colorize",         # Раскрашивание текста
    "add_emoji",        # Добавление эмодзи
    "extract_numbers_from_string",  # Извлечение чисел
    
    # === ИНФОРМАЦИЯ ===
    "__version__",      # Версия библиотеки
    "__author__",       # Автор
    "get_version",      # Получить версию
    "get_info",         # Информация о библиотеке
    "show_help",        # Показать справку
    "demo",            # Интерактивная демонстрация
]

# === УДОБНЫЕ ПСЕВДОНИМЫ ===

# Русские названия для русскоязычных пользователей
число = number
целое_число = integer
процент = percentage
возраст = age
оценка = score
цена = price
строка = string
текст = text
имя = name

# Короткие названия
num = number
int_val = integer
pct = percentage

# === ПРЕДУСТАНОВЛЕННЫЕ КОНФИГУРАЦИИ ===

def setup_for_beginners():
    """
    Настройка для начинающих - максимально простая
    
    Включает:
    - Русский язык
    - Яркие цвета и эмодзи
    - Автоисправления
    - Подсказки
    """
    configure(
        language="ru",
        style="friendly",
        colors=True,
        emojis=True,
        auto_retry=True,
        max_attempts=3,
        suggest_corrections=True
    )
    print("🎯 PyDefender настроен для начинающих!")

def setup_for_professionals():
    """
    Настройка для профессионалов - сбалансированная
    
    Включает:
    - Английский язык
    - Умеренные цвета
    - Быстрые подсказки
    - Логирование
    """
    configure(
        language="en", 
        style="professional",
        colors=True,
        emojis=False,
        auto_retry=False,
        suggest_corrections=True,
        log_attempts=True
    )
    print("💼 PyDefender настроен для профессионалов!")

def setup_for_production():
    """
    Настройка для продакшена - оптимизированная
    
    Включает:
    - Минимальный вывод
    - Высокая производительность
    - Строгие проверки
    - Кеширование
    """
    configure(
        colors=False,
        emojis=False,
        auto_retry=False,
        show_progress=False,
        cache_validators=True,
        strict_mode=True
    )
    print("🚀 PyDefender настроен для продакшена!")

# === ИНФОРМАЦИОННЫЕ ФУНКЦИИ ===

def get_version() -> str:
    """
    Получить версию библиотеки
    
    Returns:
        Строка с версией
    """
    return __version__

def get_info() -> dict:
    """
    Получить информацию о библиотеке
    
    Returns:
        Словарь с информацией
    """
    return {
        "name": "PyDefender",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "description": "Beautiful Smart Input Validation for Python",
        "features": [
            "🎨 Красивые декораторы",
            "🧠 Умная валидация", 
            "🛠️ Автоисправления",
            "🌍 Мультиязычность",
            "🔧 Легкая интеграция",
            "⚡ Высокая производительность"
        ],
        "supported_types": [
            "numbers", "strings", "emails", "phones", 
            "dates", "files", "urls", "passwords"
        ]
    }

def show_help():
    """Показать справку по использованию"""
    
    help_text = f"""
{colorize('🛡️ PyDefender Help', Color.BRIGHT_CYAN, bold=True)}
{'=' * 50}

{colorize('Быстрый старт:', Color.BRIGHT_YELLOW, bold=True)}

1. Базовое использование:
   {colorize('@pydefender.number(min_value=0, max_value=100)', Color.GREEN)}
   {colorize('def set_score(score):', Color.GREEN)}
   {colorize('    return f"Счет: {score}"', Color.GREEN)}

2. Настройка библиотеки:
   {colorize('pydefender.configure(language="ru", colors=True)', Color.GREEN)}

3. Готовые валидаторы:
   {colorize('@pydefender.age()          # 0-150 лет', Color.GREEN)}
   {colorize('@pydefender.percentage()   # 0-100%', Color.GREEN)}
   {colorize('@pydefender.price()        # Цены ≥0', Color.GREEN)}

{colorize('Доступные валидаторы:', Color.BRIGHT_YELLOW, bold=True)}

• {colorize('number', Color.CYAN)}       - Общая валидация чисел
• {colorize('integer', Color.CYAN)}      - Только целые числа  
• {colorize('positive_number', Color.CYAN)} - Положительные числа
• {colorize('percentage', Color.CYAN)}   - Проценты (0-100)
• {colorize('age', Color.CYAN)}          - Возраст (0-150)
• {colorize('score', Color.CYAN)}        - Оценки (0-10)
• {colorize('price', Color.CYAN)}        - Цены (≥0, 2 знака)

{colorize('Конфигурация:', Color.BRIGHT_YELLOW, bold=True)}

• {colorize('pydefender.setup_for_beginners()', Color.MAGENTA)}    - Для новичков
• {colorize('pydefender.setup_for_professionals()', Color.MAGENTA)} - Для профи
• {colorize('pydefender.setup_for_production()', Color.MAGENTA)}    - Для продакшена

{colorize('Примеры:', Color.BRIGHT_YELLOW, bold=True)}

{colorize('# Простая валидация', Color.DIM)}
{colorize('@pydefender.number(min_value=1, max_value=10)', Color.GREEN)}
{colorize('def rate_movie(rating): return f"Рейтинг: {rating}"', Color.GREEN)}

{colorize('# С автоисправлениями', Color.DIM)}
{colorize('@pydefender.number(extract_from_text=True)', Color.GREEN)}
{colorize('def parse_age(text): return f"Возраст: {text}"', Color.GREEN)}

{colorize('Документация:', Color.BRIGHT_YELLOW, bold=True)}
📖 Полная документация: https://pydefender.dev/docs
🐛 Сообщить об ошибке: https://github.com/pydefender/issues
💬 Поддержка: team@pydefender.dev
"""
    
    print(help_text)

def demo():
    """Запустить интерактивную демонстрацию"""
    
    print(colorize("🎮 PyDefender Interactive Demo", Color.BRIGHT_CYAN, bold=True))
    print("=" * 40)
    print()
    
    # Настройка для демо
    configure(language="ru", colors=True, emojis=True)
    
    @number(min_value=0, max_value=100, extract_from_text=True)
    def demo_validator(value):
        return f"✨ Результат: {value}"
    
    test_inputs = [
        "42",
        "75.5", 
        "Мне 25 лет",
        "abc",
        "150",
        "-10"
    ]
    
    print("🧪 Тестируем валидатор чисел (0-100) с извлечением из текста:")
    print()
    
    for test_input in test_inputs:
        print(f"📥 Ввод: {colorize(repr(test_input), Color.CYAN)}")
        try:
            result = demo_validator(test_input)
            print(f"   {colorize(result, Color.GREEN)}")
        except Exception as e:
            print(f"   {colorize(f'❌ {e}', Color.RED)}")
        print()
    
    print("🎯 Попробуйте сами:")
    print("   from pydefender import number")
    print("   @number(min_value=0, max_value=100)")
    print("   def my_function(value): return value")

# === АВТОМАТИЧЕСКАЯ ИНИЦИАЛИЗАЦИЯ ===

def _initialize():
    """Автоматическая инициализация при импорте"""
    try:
        # Загружаем конфигурацию из переменных окружения
        config = get_config()
        config.load_from_env()
        
        # Приветственное сообщение (только в интерактивном режиме)
        import sys
        if hasattr(sys, 'ps1'):  # Интерактивный режим
            welcome_msg = colorize("🛡️ PyDefender loaded!", Color.BRIGHT_GREEN, bold=True)
            tip_msg = colorize("💡 Tip: Run pydefender.show_help() for quick start", Color.CYAN)
            print(f"{welcome_msg} {tip_msg}")
        
    except Exception as e:
        # Не прерываем импорт из-за ошибок инициализации
        import warnings
        warnings.warn(f"PyDefender initialization warning: {e}")

# Запускаем инициализацию
_initialize()

# === ДОПОЛНИТЕЛЬНЫЕ АЛИАСЫ ДЛЯ СОВМЕСТИМОСТИ ===

# Для пользователей других библиотек валидации
validate_number = number
validate_integer = integer
validate_percentage = percentage

# Для пользователей marshmallow/WTForms стиля
Number = NumberValidator
Integer = IntegerValidator
Percentage = PercentageValidator

# === ЭКСПЕРИМЕНТАЛЬНЫЕ ВОЗМОЖНОСТИ ===

class ExperimentalFeatures:
    """Экспериментальные возможности (могут измениться)"""
    
    @staticmethod
    def batch_validate(validator_func, values_list):
        """
        Пакетная валидация списка значений
        
        Args:
            validator_func: Функция с валидатором
            values_list: Список значений
            
        Returns:
            Список результатов
        """
        results = []
        errors = []
        
        for i, value in enumerate(values_list):
            try:
                result = validator_func(value)
                results.append(result)
            except Exception as e:
                errors.append((i, value, e))
        
        if errors:
            print(f"⚠️ Ошибки в {len(errors)} из {len(values_list)} значений:")
            for i, value, error in errors[:3]:  # Показываем первые 3
                print(f"  [{i}] {value} → {error}")
        
        return results
    
    @staticmethod
    def create_custom_validator(validation_func, error_message="Валидация не пройдена"):
        """
        Создать кастомный валидатор из функции
        
        Args:
            validation_func: Функция валидации (value) -> bool
            error_message: Сообщение об ошибке
            
        Returns:
            Декоратор валидации
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Получаем первый аргумент
                if args:
                    value = args[0]
                    if not validation_func(value):
                        raise ValidationError(error_message, original_value=value)
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Добавляем экспериментальные функции в экспорт
experimental = ExperimentalFeatures()

# === ФИНАЛЬНЫЕ СООБЩЕНИЯ ===

# Информация о версии для отладки
_debug_info = {
    "version": __version__,
    "python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
    "features_loaded": ["numbers", "config", "decorators", "utils"],
    "ready": True
}

if __name__ == "__main__":
    # Если модуль запущен напрямую - показываем демо
    demo()