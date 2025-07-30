#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Numbers Validator
============================

Мощный и красивый валидатор для чисел
"""

import re
import math
from typing import Any, Union, Optional, List, Callable
from decimal import Decimal, InvalidOperation
from ..validators.base import BaseValidator
from ..decorators import create_validator_decorator
from ..exceptions import NumberValidationError, ValidationError
from ..utils import (
    extract_numbers_from_string, extract_first_number, colorize, add_emoji, 
    EmojiSet, Color, smart_round, parse_boolean
)

class NumberValidator(BaseValidator):
    """
    Продвинутый валидатор для чисел
    
    Поддерживает множество опций и автоматических исправлений
    """
    
    def __init__(self,
                 # === ОСНОВНЫЕ ОГРАНИЧЕНИЯ ===
                 min_value: Optional[Union[int, float, Decimal]] = None,
                 max_value: Optional[Union[int, float, Decimal]] = None,
                 
                 # === ТИПЫ ЧИСЕЛ ===
                 allow_integers: bool = True,
                 allow_floats: bool = True,
                 allow_negative: bool = True,
                 allow_zero: bool = True,
                 allow_decimals: bool = True,
                 
                 # === АВТОКОНВЕРТАЦИЯ ===
                 convert_strings: bool = True,
                 extract_from_text: bool = False,
                 strip_spaces: bool = True,
                 
                 # === ОКРУГЛЕНИЕ ===
                 round_floats: bool = False,
                 round_decimals: Optional[int] = None,
                 round_mode: str = "normal",  # "normal", "up", "down", "towards_zero"
                 
                 # === ФОРМАТИРОВАНИЕ ===
                 normalize_format: bool = False,
                 remove_leading_zeros: bool = True,
                 
                 # === ВАЛИДАЦИЯ ДИАПАЗОНОВ ===
                 step: Optional[Union[int, float]] = None,
                 multiple_of: Optional[Union[int, float]] = None,
                 
                 # === СПЕЦИАЛЬНЫЕ ЗНАЧЕНИЯ ===
                 forbidden_values: Optional[List[Union[int, float]]] = None,
                 allowed_values: Optional[List[Union[int, float]]] = None,
                 
                 # === ПОВЕДЕНИЕ ===
                 auto_suggest_range: bool = True,
                 suggest_closest: bool = True,
                 
                 **kwargs):
        """
        Инициализация валидатора чисел
        
        Args:
            min_value: Минимальное значение
            max_value: Максимальное значение
            allow_integers: Разрешить целые числа
            allow_floats: Разрешить дробные числа
            allow_negative: Разрешить отрицательные числа
            allow_zero: Разрешить ноль
            allow_decimals: Разрешить Decimal
            convert_strings: Конвертировать строки в числа
            extract_from_text: Извлекать числа из текста
            strip_spaces: Убирать пробелы
            round_floats: Округлять дробные до целых
            round_decimals: Количество знаков после запятой
            round_mode: Режим округления
            normalize_format: Нормализовать формат числа
            remove_leading_zeros: Убирать ведущие нули
            step: Шаг для валидации (число должно быть кратно шагу)
            multiple_of: Число должно быть кратно этому значению
            forbidden_values: Запрещенные значения
            allowed_values: Разрешенные значения (если указано, только эти)
            auto_suggest_range: Автоматически предлагать диапазон
            suggest_closest: Предлагать ближайшие валидные значения
        """
        super().__init__(**kwargs)
        
        # Основные ограничения
        self.min_value = min_value
        self.max_value = max_value
        
        # Типы
        self.allow_integers = allow_integers
        self.allow_floats = allow_floats
        self.allow_negative = allow_negative
        self.allow_zero = allow_zero
        self.allow_decimals = allow_decimals
        
        # Конвертация
        self.convert_strings = convert_strings
        self.extract_from_text = extract_from_text
        self.strip_spaces = strip_spaces
        
        # Округление
        self.round_floats = round_floats
        self.round_decimals = round_decimals
        self.round_mode = round_mode
        
        # Форматирование
        self.normalize_format = normalize_format
        self.remove_leading_zeros = remove_leading_zeros
        
        # Диапазоны
        self.step = step
        self.multiple_of = multiple_of
        
        # Специальные значения
        self.forbidden_values = set(forbidden_values) if forbidden_values else set()
        self.allowed_values = set(allowed_values) if allowed_values else None
        
        # Поведение
        self.auto_suggest_range = auto_suggest_range
        self.suggest_closest = suggest_closest
        
        # Валидация параметров
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Проверить корректность конфигурации"""
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                raise ValueError("min_value не может быть больше max_value")
        
        if self.round_decimals is not None and self.round_decimals < 0:
            raise ValueError("round_decimals не может быть отрицательным")
        
        if not (self.allow_integers or self.allow_floats):
            raise ValueError("Должен быть разрешен хотя бы один тип чисел")
    
    def _validate_value(self, value: Any) -> Union[int, float, Decimal]:
        """
        Основная логика валидации числа
        
        Args:
            value: Значение для валидации
            
        Returns:
            Валидированное число
            
        Raises:
            NumberValidationError: При ошибке валидации
        """
        original_value = value
        
        # 1. Конвертация в число
        number = self._convert_to_number(value)
        
        # 2. Проверка типа
        number = self._validate_number_type(number, original_value)
        
        # 3. Проверка знака
        self._validate_sign(number)
        
        # 4. Проверка диапазона
        self._validate_range(number)
        
        # 5. Проверка кратности
        self._validate_multiples(number)
        
        # 6. Проверка разрешенных/запрещенных значений
        self._validate_allowed_forbidden(number)
        
        # 7. Применение округления и форматирования
        number = self._apply_formatting(number)
        
        return number
    
    def _convert_to_number(self, value: Any) -> Union[int, float, Decimal]:
        """Конвертировать значение в число"""
        
        # Уже число
        if isinstance(value, (int, float, Decimal)):
            return value
        
        # Логические значения
        if isinstance(value, bool):
            return int(value)
        
        # Строки
        if isinstance(value, str):
            return self._convert_string_to_number(value)
        
        # Попытка конвертации других типов
        try:
            return float(value)
        except (ValueError, TypeError):
            raise self._create_number_error(
                f"Невозможно конвертировать {type(value).__name__} в число",
                value,
                suggestions=["Введите число", "Используйте числовое значение"]
            )
    
    def _convert_string_to_number(self, text: str) -> Union[int, float, Decimal]:
        """Конвертировать строку в число"""
        
        if not self.convert_strings:
            raise self._create_number_error(
                "Строки не разрешены",
                text,
                suggestions=["Введите числовое значение"]
            )
        
        # Убираем пробелы
        if self.strip_spaces:
            text = text.strip()
        
        if not text:
            raise self._create_number_error(
                "Пустая строка",
                text,
                suggestions=["Введите число"]
            )
        
        # Извлечение из текста
        if self.extract_from_text:
            number = extract_first_number(text)
            if number is None:
                raise self._create_number_error(
                    "В тексте не найдено чисел",
                    text,
                    suggestions=[
                        "Добавьте число в текст",
                        "Пример: 'возраст 25 лет' → 25"
                    ]
                )
            return number
        
        # Обработка специальных форматов
        text = self._normalize_number_string(text)
        
        # Попытка конвертации
        try:
            # Сначала пробуем как целое
            if '.' not in text and 'e' not in text.lower():
                return int(text)
            else:
                return float(text)
                
        except ValueError:
            # Пробуем как Decimal для высокой точности
            if self.allow_decimals:
                try:
                    return Decimal(text)
                except InvalidOperation:
                    pass
            
            # Предлагаем исправления
            suggestions = self._suggest_number_corrections(text)
            
            raise self._create_number_error(
                f"Неверный формат числа: '{text}'",
                text,
                suggestions=suggestions
            )
    
    def _normalize_number_string(self, text: str) -> str:
        """Нормализовать строку с числом"""
        
        # Убираем лишние символы
        text = re.sub(r'[^\d\-+.,eE]', '', text)
        
        # Заменяем запятые на точки
        text = text.replace(',', '.')
        
        # Убираем ведущие нули
        if self.remove_leading_zeros:
            text = re.sub(r'^0+(\d)', r'\1', text)
            if text.startswith('.'):
                text = '0' + text
        
        # Обработка множественных точек
        if text.count('.') > 1:
            # Оставляем только последнюю точку
            parts = text.split('.')
            text = ''.join(parts[:-1]) + '.' + parts[-1]
        
        return text
    
    def _suggest_number_corrections(self, text: str) -> List[str]:
        """Предложить исправления для неверного числа"""
        suggestions = []
        
        # Извлекаем числа из строки
        numbers = extract_numbers_from_string(text)
        if numbers:
            suggestions.append(f"Возможно, вы имели в виду: {numbers[0]}")
        
        # Общие предложения
        suggestions.extend([
            "Используйте только цифры и точку",
            "Пример: 42 или 3.14",
            "Не используйте пробелы и лишние символы"
        ])
        
        return suggestions
    
    def _validate_number_type(self, number: Union[int, float, Decimal], 
                             original_value: Any) -> Union[int, float, Decimal]:
        """Проверить тип числа"""
        
        # Проверка целых чисел
        if isinstance(number, int) or (isinstance(number, float) and number.is_integer()):
            if not self.allow_integers:
                if self.allow_floats:
                    return float(number)
                else:
                    raise self._create_number_error(
                        "Целые числа не разрешены",
                        original_value,
                        suggestions=["Введите дробное число"]
                    )
        
        # Проверка дробных чисел
        elif isinstance(number, (float, Decimal)) and not number.is_integer():
            if not self.allow_floats:
                if self.round_floats:
                    return self._round_number(number)
                else:
                    raise self._create_number_error(
                        "Дробные числа не разрешены",
                        original_value,
                        suggestions=[
                            "Введите целое число",
                            f"Округлить до {int(number)}?"
                        ]
                    )
        
        return number
    
    def _validate_sign(self, number: Union[int, float, Decimal]):
        """Проверить знак числа"""
        
        if number < 0 and not self.allow_negative:
            raise self._create_number_error(
                "Отрицательные числа не разрешены",
                number,
                suggestions=[
                    "Введите положительное число",
                    f"Возможно: {abs(number)}"
                ]
            )
        
        if number == 0 and not self.allow_zero:
            raise self._create_number_error(
                "Ноль не разрешен",
                number,
                suggestions=["Введите ненулевое число"]
            )
    
    def _validate_range(self, number: Union[int, float, Decimal]):
        """Проверить диапазон числа"""
        
        if self.min_value is not None and number < self.min_value:
            suggestions = []
            
            if self.auto_suggest_range:
                if self.max_value is not None:
                    suggestions.append(f"Введите число от {self.min_value} до {self.max_value}")
                else:
                    suggestions.append(f"Введите число больше или равно {self.min_value}")
            
            if self.suggest_closest:
                suggestions.append(f"Ближайшее допустимое: {self.min_value}")
            
            raise self._create_number_error(
                f"Число слишком маленькое (минимум: {self.min_value})",
                number,
                suggestions=suggestions
            )
        
        if self.max_value is not None and number > self.max_value:
            suggestions = []
            
            if self.auto_suggest_range:
                if self.min_value is not None:
                    suggestions.append(f"Введите число от {self.min_value} до {self.max_value}")
                else:
                    suggestions.append(f"Введите число меньше или равно {self.max_value}")
            
            if self.suggest_closest:
                suggestions.append(f"Ближайшее допустимое: {self.max_value}")
            
            raise self._create_number_error(
                f"Число слишком большое (максимум: {self.max_value})",
                number,
                suggestions=suggestions
            )
    
    def _validate_multiples(self, number: Union[int, float, Decimal]):
        """Проверить кратность числа"""
        
        if self.step is not None:
            if self.min_value is not None:
                base = self.min_value
            else:
                base = 0
            
            remainder = (number - base) % self.step
            if remainder != 0:
                # Находим ближайшие валидные значения
                lower = number - remainder
                upper = lower + self.step
                
                suggestions = [f"Шаг должен быть {self.step}"]
                
                if self.suggest_closest:
                    suggestions.extend([
                        f"Ближайшие допустимые: {lower} или {upper}"
                    ])
                
                raise self._create_number_error(
                    f"Число должно соответствовать шагу {self.step}",
                    number,
                    suggestions=suggestions
                )
        
        if self.multiple_of is not None:
            if number % self.multiple_of != 0:
                # Находим ближайшие кратные
                lower = (number // self.multiple_of) * self.multiple_of
                upper = lower + self.multiple_of
                
                suggestions = [f"Число должно быть кратно {self.multiple_of}"]
                
                if self.suggest_closest:
                    suggestions.extend([
                        f"Ближайшие кратные: {int(lower)} или {int(upper)}"
                    ])
                
                raise self._create_number_error(
                    f"Число должно быть кратно {self.multiple_of}",
                    number,
                    suggestions=suggestions
                )
    
    def _validate_allowed_forbidden(self, number: Union[int, float, Decimal]):
        """Проверить разрешенные и запрещенные значения"""
        
        if self.allowed_values is not None:
            if number not in self.allowed_values:
                allowed_list = sorted(list(self.allowed_values))
                suggestions = [f"Разрешенные значения: {allowed_list}"]
                
                if self.suggest_closest and len(allowed_list) <= 10:
                    # Находим ближайшее разрешенное значение
                    closest = min(allowed_list, key=lambda x: abs(x - number))
                    suggestions.append(f"Ближайшее разрешенное: {closest}")
                
                raise self._create_number_error(
                    f"Значение {number} не разрешено",
                    number,
                    suggestions=suggestions
                )
        
        if number in self.forbidden_values:
            suggestions = ["Выберите другое значение"]
            
            if self.suggest_closest:
                # Предлагаем соседние значения
                if isinstance(number, int):
                    suggestions.extend([
                        f"Попробуйте: {number - 1} или {number + 1}"
                    ])
                else:
                    suggestions.extend([
                        f"Попробуйте близкие значения"
                    ])
            
            raise self._create_number_error(
                f"Значение {number} запрещено",
                number,
                suggestions=suggestions
            )
    
    def _apply_formatting(self, number: Union[int, float, Decimal]) -> Union[int, float, Decimal]:
        """Применить форматирование к числу"""
        
        # Округление
        if self.round_decimals is not None:
            number = self._round_to_decimals(number, self.round_decimals)
        elif self.round_floats and isinstance(number, (float, Decimal)):
            number = self._round_number(number)
        
        return number
    
    def _round_number(self, number: Union[float, Decimal]) -> int:
        """Округлить число до целого"""
        if self.round_mode == "up":
            return math.ceil(number)
        elif self.round_mode == "down":
            return math.floor(number)
        elif self.round_mode == "towards_zero":
            return math.trunc(number)
        else:  # normal
            return round(number)
    
    def _round_to_decimals(self, number: Union[int, float, Decimal], 
                          decimals: int) -> Union[int, float]:
        """Округлить до указанного количества знаков"""
        rounded = round(float(number), decimals)
        
        # Возвращаем int если нет дробной части
        if decimals == 0 or rounded == int(rounded):
            return int(rounded)
        
        return rounded
    
    def _create_number_error(self, message: str, value: Any = None, 
                           suggestions: List[str] = None) -> NumberValidationError:
        """Создать ошибку валидации числа"""
        return NumberValidationError(
            message=message,
            original_value=value,
            min_value=self.min_value,
            max_value=self.max_value,
            suggestions=suggestions or [],
            field_name=self.field_name
        )

# === ПРЕДУСТАНОВЛЕННЫЕ ВАЛИДАТОРЫ ===

class PositiveNumberValidator(NumberValidator):
    """Валидатор для положительных чисел"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_value', 0)
        kwargs.setdefault('allow_negative', False)
        super().__init__(**kwargs)

class IntegerValidator(NumberValidator):
    """Валидатор для целых чисел"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('allow_floats', False)
        kwargs.setdefault('round_floats', True)
        super().__init__(**kwargs)

class PercentageValidator(NumberValidator):
    """Валидатор для процентов (0-100)"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_value', 0)
        kwargs.setdefault('max_value', 100)
        kwargs.setdefault('round_decimals', 1)
        super().__init__(**kwargs)

class AgeValidator(NumberValidator):
    """Валидатор для возраста"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_value', 0)
        kwargs.setdefault('max_value', 150)
        kwargs.setdefault('allow_floats', False)
        kwargs.setdefault('round_floats', True)
        super().__init__(**kwargs)

class ScoreValidator(NumberValidator):
    """Валидатор для оценок (0-10)"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_value', 0)
        kwargs.setdefault('max_value', 10)
        kwargs.setdefault('round_decimals', 1)
        super().__init__(**kwargs)

class PriceValidator(NumberValidator):
    """Валидатор для цен"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_value', 0)
        kwargs.setdefault('round_decimals', 2)
        kwargs.setdefault('allow_negative', False)
        super().__init__(**kwargs)

# === ДЕКОРАТОРЫ ===

# Основной декоратор
number = create_validator_decorator(NumberValidator)

# Специализированные декораторы
positive_number = create_validator_decorator(PositiveNumberValidator)
integer = create_validator_decorator(IntegerValidator)
percentage = create_validator_decorator(PercentageValidator)
age = create_validator_decorator(AgeValidator)
score = create_validator_decorator(ScoreValidator)
price = create_validator_decorator(PriceValidator)

# === ДОПОЛНИТЕЛЬНЫЕ УТИЛИТЫ ===

def create_range_validator(min_val: Union[int, float], max_val: Union[int, float], 
                          **kwargs) -> NumberValidator:
    """
    Быстро создать валидатор диапазона
    
    Args:
        min_val: Минимальное значение
        max_val: Максимальное значение
        **kwargs: Дополнительные параметры
        
    Returns:
        NumberValidator
    """
    return NumberValidator(min_value=min_val, max_value=max_val, **kwargs)

def create_step_validator(step: Union[int, float], start: Union[int, float] = 0,
                         **kwargs) -> NumberValidator:
    """
    Создать валидатор с шагом
    
    Args:
        step: Размер шага
        start: Начальное значение
        **kwargs: Дополнительные параметры
        
    Returns:
        NumberValidator
    """
    return NumberValidator(step=step, min_value=start, **kwargs)

def create_choices_validator(choices: List[Union[int, float]], **kwargs) -> NumberValidator:
    """
    Создать валидатор с выбором из списка
    
    Args:
        choices: Список разрешенных значений
        **kwargs: Дополнительные параметры
        
    Returns:
        NumberValidator
    """
    return NumberValidator(allowed_values=choices, **kwargs)

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

def demo_number_validators():
    """Демонстрация валидаторов чисел"""
    
    print(colorize("🔢 PyDefender Number Validators Demo", Color.BRIGHT_CYAN, bold=True))
    print("=" * 50)
    
    # Простой валидатор
    @number(min_value=0, max_value=100)
    def set_percentage(value):
        return f"Процент: {value}%"
    
    # Валидатор возраста
    @age()
    def set_age(age_value):
        return f"Возраст: {age_value} лет"
    
    # Валидатор с извлечением из текста
    @number(extract_from_text=True, min_value=0)
    def parse_number_from_text(text):
        return f"Найденное число: {text}"
    
    # Тестирование
    test_cases = [
        (set_percentage, ["50", "75.5", "101", "-10"]),
        (set_age, ["25", "30.5", "200", "abc"]),
        (parse_number_from_text, ["Мне 25 лет", "Цена 99.99 рублей", "без чисел"])
    ]
    
    for func, test_values in test_cases:
        print(f"\n{add_emoji(f'Тест функции: {func.__name__}', EmojiSet.ROCKET)}")
        print("-" * 30)
        
        for test_value in test_values:
            try:
                result = func(test_value)
                print(f"✅ '{test_value}' → {colorize(result, Color.GREEN)}")
            except Exception as e:
                print(f"❌ '{test_value}' → {colorize(str(e), Color.RED)}")
    
    # Статистика валидатора
    if hasattr(set_percentage, '_pydefender_validator'):
        validator = set_percentage._pydefender_validator
        stats = validator.get_statistics()
        print(f"\n{add_emoji('Статистика валидатора:', EmojiSet.INFO)}")
        print(f"  Всего проверок: {stats['total_validations']}")
        print(f"  Успешных: {stats['successful_validations']}")
        print(f"  Ошибок: {stats['failed_validations']}")
        print(f"  Процент успеха: {stats['success_rate']}%")

def demo_advanced_features():
    """Демонстрация продвинутых возможностей"""
    
    print(f"\n{add_emoji('Продвинутые возможности:', EmojiSet.MAGIC)}")
    print("=" * 40)
    
    # Валидатор с кратностью
    @number(multiple_of=5, min_value=0, max_value=100)
    def set_score_multiple_5(score):
        return f"Оценка (кратная 5): {score}"
    
    # Валидатор с разрешенными значениями
    @number(allowed_values=[1, 5, 10, 25, 50, 100])
    def set_denomination(value):
        return f"Номинал: {value}"
    
    # Валидатор с округлением
    @number(round_decimals=2, min_value=0)
    def set_price_precise(price):
        return f"Цена: {price:.2f} ₽"
    
    test_functions = [
        (set_score_multiple_5, ["15", "17", "20"]),
        (set_denomination, ["5", "7", "25"]),
        (set_price_precise, ["99.999", "10.1234", "5"])
    ]
    
    for func, test_values in test_functions:
        print(f"\n🎯 {func.__name__}:")
        for test_value in test_values:
            try:
                result = func(test_value)
                print(f"  ✅ {test_value} → {result}")
            except Exception as e:
                print(f"  ❌ {test_value} → {str(e)}")

if __name__ == "__main__":
    demo_number_validators()
    demo_advanced_features()