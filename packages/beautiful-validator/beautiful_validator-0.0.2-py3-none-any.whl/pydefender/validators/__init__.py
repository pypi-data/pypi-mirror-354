#!/usr/bin/env python3
"""
PyDefender Validators Package
=============================

Валидаторы для различных типов данных
"""

# Базовый валидатор
from .base import BaseValidator

# Валидаторы чисел
from .numbers import (
    NumberValidator, PositiveNumberValidator, IntegerValidator,
    PercentageValidator, AgeValidator, ScoreValidator, PriceValidator,
    number, positive_number, integer, percentage, age, score, price
)

# Валидаторы строк
from .strings import (
    StringValidator, NameValidator, UsernameValidator, CommentValidator,
    string, text, name, username, comment
)

__all__ = [
    # Базовый
    "BaseValidator",
    
    # Числа - классы
    "NumberValidator", "PositiveNumberValidator", "IntegerValidator",
    "PercentageValidator", "AgeValidator", "ScoreValidator", "PriceValidator",
    
    # Числа - декораторы
    "number", "positive_number", "integer", "percentage", "age", "score", "price",
    
    # Строки - классы
    "StringValidator", "NameValidator", "UsernameValidator", "CommentValidator",
    
    # Строки - декораторы
    "string", "text", "name", "username", "comment",
]