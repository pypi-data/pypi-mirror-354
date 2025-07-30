#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Exceptions System
============================

Красивые и информативные исключения для валидации
"""

from typing import Any, List, Optional, Dict, Union
from enum import Enum

class ErrorSeverity(Enum):
    """Уровни серьезности ошибок"""
    INFO = "info"           # Информационное сообщение
    WARNING = "warning"     # Предупреждение
    ERROR = "error"         # Ошибка валидации
    CRITICAL = "critical"   # Критическая ошибка

class ErrorCategory(Enum):
    """Категории ошибок"""
    FORMAT = "format"               # Неверный формат
    RANGE = "range"                 # Выход за диапазон
    TYPE = "type"                   # Неверный тип данных
    LENGTH = "length"               # Неверная длина
    CONTENT = "content"             # Неверное содержимое
    SECURITY = "security"           # Проблемы безопасности
    CONVERSION = "conversion"       # Ошибки конвертации
    CONFIGURATION = "configuration" # Ошибки конфигурации

class PyDefenderError(Exception):
    """
    Базовое исключение PyDefender
    
    Все исключения библиотеки наследуются от этого класса
    """
    
    def __init__(self, 
                 message: str,
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 category: ErrorCategory = ErrorCategory.FORMAT,
                 code: Optional[str] = None):
        """
        Args:
            message: Сообщение об ошибке
            severity: Уровень серьезности
            category: Категория ошибки
            code: Код ошибки для программной обработки
        """
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.category = category
        self.code = code or f"{category.value}_error"
        self.timestamp = self._get_timestamp()
    
    def _get_timestamp(self) -> str:
        """Получить текущее время"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_error_info(self) -> Dict[str, Any]:
        """Получить полную информацию об ошибке"""
        return {
            'message': self.message,
            'severity': self.severity.value,
            'category': self.category.value,
            'code': self.code,
            'timestamp': self.timestamp,
            'type': self.__class__.__name__
        }
    
    def __str__(self) -> str:
        return self.message

class ValidationError(PyDefenderError):
    """
    Ошибка валидации входных данных
    
    Основной тип ошибок для неверных данных
    """
    
    def __init__(self, 
                 message: str,
                 suggestions: Optional[List[str]] = None,
                 original_value: Any = None,
                 expected_type: Optional[str] = None,
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 category: ErrorCategory = ErrorCategory.FORMAT,
                 field_name: Optional[str] = None):
        """
        Args:
            message: Сообщение об ошибке
            suggestions: Список предложений по исправлению
            original_value: Исходное значение, которое не прошло валидацию
            expected_type: Ожидаемый тип данных
            severity: Уровень серьезности
            category: Категория ошибки
            field_name: Имя поля (для форм)
        """
        super().__init__(message, severity, category)
        self.suggestions = suggestions or []
        self.original_value = original_value
        self.expected_type = expected_type
        self.field_name = field_name
    
    def add_suggestion(self, suggestion: str) -> 'ValidationError':
        """
        Добавить предложение по исправлению
        
        Args:
            suggestion: Текст предложения
            
        Returns:
            self для цепочки вызовов
        """
        self.suggestions.append(suggestion)
        return self
    
    def with_field(self, field_name: str) -> 'ValidationError':
        """
        Установить имя поля
        
        Args:
            field_name: Имя поля
            
        Returns:
            self для цепочки вызовов
        """
        self.field_name = field_name
        return self
    
    def get_detailed_message(self) -> str:
        """Получить детальное сообщение с предложениями"""
        lines = [self.message]
        
        if self.field_name:
            lines[0] = f"Поле '{self.field_name}': {self.message}"
        
        if self.original_value is not None:
            lines.append(f"Получено: {repr(self.original_value)}")
        
        if self.expected_type:
            lines.append(f"Ожидается: {self.expected_type}")
        
        if self.suggestions:
            lines.append("💡 Предложения:")
            for suggestion in self.suggestions:
                lines.append(f"  • {suggestion}")
        
        return "\n".join(lines)

class NumberValidationError(ValidationError):
    """Ошибка валидации чисел"""
    
    def __init__(self, 
                 message: str,
                 min_value: Optional[Union[int, float]] = None,
                 max_value: Optional[Union[int, float]] = None,
                 **kwargs):
        super().__init__(message, category=ErrorCategory.RANGE, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        
        # Автоматические предложения для чисел
        if min_value is not None and max_value is not None:
            self.add_suggestion(f"Введите число от {min_value} до {max_value}")
        elif min_value is not None:
            self.add_suggestion(f"Введите число больше {min_value}")
        elif max_value is not None:
            self.add_suggestion(f"Введите число меньше {max_value}")

class StringValidationError(ValidationError):
    """Ошибка валидации строк"""
    
    def __init__(self, 
                 message: str,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 **kwargs):
        super().__init__(message, category=ErrorCategory.LENGTH, **kwargs)
        self.min_length = min_length
        self.max_length = max_length
        
        # Автоматические предложения для строк
        if min_length is not None and max_length is not None:
            self.add_suggestion(f"Длина должна быть от {min_length} до {max_length} символов")
        elif min_length is not None:
            self.add_suggestion(f"Минимальная длина: {min_length} символов")
        elif max_length is not None:
            self.add_suggestion(f"Максимальная длина: {max_length} символов")

class EmailValidationError(ValidationError):
    """Ошибка валидации email"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.FORMAT, **kwargs)
        self.add_suggestion("Используйте формат: name@example.com")

class PhoneValidationError(ValidationError):
    """Ошибка валидации телефона"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.FORMAT, **kwargs)
        self.add_suggestion("Используйте формат: +7-XXX-XXX-XX-XX")

class ConversionError(PyDefenderError):
    """
    Ошибка конвертации типов данных
    """
    
    def __init__(self, 
                 message: str,
                 from_type: Optional[str] = None,
                 to_type: Optional[str] = None,
                 original_value: Any = None):
        super().__init__(message, ErrorSeverity.ERROR, ErrorCategory.CONVERSION)
        self.from_type = from_type
        self.to_type = to_type
        self.original_value = original_value

class ConfigurationError(PyDefenderError):
    """
    Ошибка конфигурации валидатора
    """
    
    def __init__(self, message: str, parameter: Optional[str] = None):
        super().__init__(message, ErrorSeverity.CRITICAL, ErrorCategory.CONFIGURATION)
        self.parameter = parameter

class SecurityError(PyDefenderError):
    """
    Ошибка безопасности (потенциально опасные данные)
    """
    
    def __init__(self, message: str, threat_type: Optional[str] = None):
        super().__init__(message, ErrorSeverity.CRITICAL, ErrorCategory.SECURITY)
        self.threat_type = threat_type

class RetryLimitError(PyDefenderError):
    """
    Превышен лимит попыток ввода
    """
    
    def __init__(self, message: str, attempts: int, max_attempts: int):
        super().__init__(message, ErrorSeverity.WARNING, ErrorCategory.FORMAT)
        self.attempts = attempts
        self.max_attempts = max_attempts

# === ФАБРИКИ ОШИБОК ===

def create_number_error(message: str, 
                       value: Any = None,
                       min_val: Optional[Union[int, float]] = None,
                       max_val: Optional[Union[int, float]] = None) -> NumberValidationError:
    """
    Создать ошибку валидации числа
    
    Args:
        message: Сообщение об ошибке
        value: Исходное значение
        min_val: Минимальное значение
        max_val: Максимальное значение
        
    Returns:
        NumberValidationError
    """
    return NumberValidationError(
        message=message,
        original_value=value,
        min_value=min_val,
        max_value=max_val,
        expected_type="число"
    )

def create_string_error(message: str,
                       value: Any = None,
                       min_len: Optional[int] = None,
                       max_len: Optional[int] = None) -> StringValidationError:
    """
    Создать ошибку валидации строки
    
    Args:
        message: Сообщение об ошибке
        value: Исходное значение
        min_len: Минимальная длина
        max_len: Максимальная длина
        
    Returns:
        StringValidationError
    """
    return StringValidationError(
        message=message,
        original_value=value,
        min_length=min_len,
        max_length=max_len,
        expected_type="строка"
    )

def create_format_error(message: str, 
                       value: Any = None,
                       expected_format: Optional[str] = None) -> ValidationError:
    """
    Создать ошибку формата
    
    Args:
        message: Сообщение об ошибке
        value: Исходное значение
        expected_format: Ожидаемый формат
        
    Returns:
        ValidationError
    """
    error = ValidationError(
        message=message,
        original_value=value,
        category=ErrorCategory.FORMAT
    )
    
    if expected_format:
        error.add_suggestion(f"Используйте формат: {expected_format}")
    
    return error

# === ДЕКОРАТОРЫ ДЛЯ ОБРАБОТКИ ОШИБОК ===

def handle_validation_errors(func):
    """
    Декоратор для красивой обработки ошибок валидации
    
    Перехватывает исключения и форматирует их для пользователя
    """
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            # Показываем красивое сообщение
            from .utils import format_error_message
            formatted_message = format_error_message(e)
            print(formatted_message)
            raise
        except Exception as e:
            # Оборачиваем неожиданные ошибки
            wrapped_error = PyDefenderError(
                f"Неожиданная ошибка: {str(e)}",
                severity=ErrorSeverity.CRITICAL
            )
            raise wrapped_error from e
    
    return wrapper

# === УТИЛИТЫ ДЛЯ РАБОТЫ С ОШИБКАМИ ===

def collect_errors(*errors: PyDefenderError) -> List[PyDefenderError]:
    """
    Собрать несколько ошибок в список
    
    Args:
        *errors: Ошибки для сбора
        
    Returns:
        Список ошибок
    """
    return list(errors)

def format_error_summary(errors: List[PyDefenderError]) -> str:
    """
    Форматировать сводку ошибок
    
    Args:
        errors: Список ошибок
        
    Returns:
        Отформатированная строка
    """
    if not errors:
        return "✅ Ошибок не найдено"
    
    lines = [f"❌ Найдено ошибок: {len(errors)}", ""]
    
    for i, error in enumerate(errors, 1):
        lines.append(f"{i}. {error.message}")
        if isinstance(error, ValidationError) and error.suggestions:
            for suggestion in error.suggestions[:2]:  # Показываем только первые 2
                lines.append(f"   💡 {suggestion}")
        lines.append("")
    
    return "\n".join(lines)

def get_error_by_code(errors: List[PyDefenderError], code: str) -> Optional[PyDefenderError]:
    """
    Найти ошибку по коду
    
    Args:
        errors: Список ошибок
        code: Код ошибки
        
    Returns:
        Ошибка или None
    """
    for error in errors:
        if error.code == code:
            return error
    return None

def filter_errors_by_severity(errors: List[PyDefenderError], 
                             severity: ErrorSeverity) -> List[PyDefenderError]:
    """
    Фильтровать ошибки по уровню серьезности
    
    Args:
        errors: Список ошибок
        severity: Уровень серьезности
        
    Returns:
        Отфильтрованный список
    """
    return [error for error in errors if error.severity == severity]

def has_critical_errors(errors: List[PyDefenderError]) -> bool:
    """
    Проверить наличие критических ошибок
    
    Args:
        errors: Список ошибок
        
    Returns:
        True если есть критические ошибки
    """
    return any(error.severity == ErrorSeverity.CRITICAL for error in errors)

# === КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ ===

class ValidationContext:
    """
    Контекстный менеджер для сбора ошибок валидации
    
    Позволяет собирать несколько ошибок и обрабатывать их вместе
    """
    
    def __init__(self, continue_on_error: bool = True):
        """
        Args:
            continue_on_error: Продолжать ли выполнение при ошибках
        """
        self.continue_on_error = continue_on_error
        self.errors: List[PyDefenderError] = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.errors:
            # Есть накопленные ошибки
            if has_critical_errors(self.errors):
                # Поднимаем первую критическую ошибку
                critical_errors = filter_errors_by_severity(self.errors, ErrorSeverity.CRITICAL)
                raise critical_errors[0]
            elif not self.continue_on_error:
                # Поднимаем первую ошибку
                raise self.errors[0]
        
        # Подавляем исключения если настроено продолжение
        return self.continue_on_error and exc_type is not None
    
    def add_error(self, error: PyDefenderError):
        """Добавить ошибку в контекст"""
        self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Проверить наличие ошибок"""
        return len(self.errors) > 0
    
    def get_error_summary(self) -> str:
        """Получить сводку ошибок"""
        return format_error_summary(self.errors)

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

def example_usage():
    """Примеры использования системы исключений"""
    
    # Простая ошибка валидации
    try:
        raise ValidationError("Неверное значение")
    except ValidationError as e:
        print(f"Ошибка: {e}")
    
    # Ошибка с предложениями
    try:
        error = NumberValidationError(
            "Число слишком большое",
            max_value=100,
            original_value=150
        )
        error.add_suggestion("Попробуйте ввести число меньше 100")
        raise error
    except NumberValidationError as e:
        print(e.get_detailed_message())
    
    # Использование контекста
    with ValidationContext() as ctx:
        try:
            # Какая-то валидация
            raise ValidationError("Первая ошибка")
        except ValidationError as e:
            ctx.add_error(e)
        
        try:
            # Еще одна валидация
            raise StringValidationError("Вторая ошибка")
        except StringValidationError as e:
            ctx.add_error(e)
        
        if ctx.has_errors():
            print(ctx.get_error_summary())

if __name__ == "__main__":
    example_usage()