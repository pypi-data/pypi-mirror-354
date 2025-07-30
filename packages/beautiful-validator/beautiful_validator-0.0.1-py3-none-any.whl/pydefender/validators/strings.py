#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Strings Validator
============================

Простой и эффективный валидатор для строк
"""

import re
from typing import Any, List, Optional, Union
from ..validators.base import BaseValidator
from ..decorators import create_validator_decorator
from ..exceptions import StringValidationError, ValidationError
from ..utils import (
    clean_string, capitalize_words, colorize, add_emoji, 
    EmojiSet, Color, suggest_similar_strings
)

class StringValidator(BaseValidator):
    """
    Валидатор для строк с базовым функционалом
    """
    
    def __init__(self,
                 # === ДЛИНА ===
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 exact_length: Optional[int] = None,
                 
                 # === СОДЕРЖИМОЕ ===
                 allow_letters: bool = True,
                 allow_numbers: bool = True,
                 allow_spaces: bool = True,
                 allow_special_chars: bool = True,
                 allow_unicode: bool = True,
                 
                 # === АВТООБРАБОТКА ===
                 auto_trim: bool = True,
                 auto_capitalize: bool = False,
                 remove_extra_spaces: bool = True,
                 normalize_case: str = "none",  # "none", "lower", "upper", "title", "smart"
                 
                 # === ПАТТЕРНЫ ===
                 pattern: Optional[str] = None,
                 forbidden_patterns: Optional[List[str]] = None,
                 
                 # === СЛОВА ===
                 forbidden_words: Optional[List[str]] = None,
                 required_words: Optional[List[str]] = None,
                 
                 # === ВАЛИДАЦИЯ ===
                 case_sensitive: bool = False,
                 suggest_corrections: bool = True,
                 
                 **kwargs):
        """
        Args:
            min_length: Минимальная длина
            max_length: Максимальная длина  
            exact_length: Точная длина
            allow_letters: Разрешить буквы
            allow_numbers: Разрешить цифры
            allow_spaces: Разрешить пробелы
            allow_special_chars: Разрешить спецсимволы
            allow_unicode: Разрешить Unicode
            auto_trim: Автоматически убирать пробелы по краям
            auto_capitalize: Автоматически делать заглавную первую букву
            remove_extra_spaces: Убирать лишние пробелы
            normalize_case: Нормализация регистра
            pattern: Регулярное выражение для проверки
            forbidden_patterns: Запрещенные паттерны
            forbidden_words: Запрещенные слова
            required_words: Обязательные слова
            case_sensitive: Учитывать регистр
            suggest_corrections: Предлагать исправления
        """
        super().__init__(**kwargs)
        
        # Длина
        self.min_length = min_length
        self.max_length = max_length
        self.exact_length = exact_length
        
        # Содержимое
        self.allow_letters = allow_letters
        self.allow_numbers = allow_numbers
        self.allow_spaces = allow_spaces
        self.allow_special_chars = allow_special_chars
        self.allow_unicode = allow_unicode
        
        # Автообработка
        self.auto_trim = auto_trim
        self.auto_capitalize = auto_capitalize
        self.remove_extra_spaces = remove_extra_spaces
        self.normalize_case = normalize_case
        
        # Паттерны
        self.pattern = re.compile(pattern) if pattern else None
        self.forbidden_patterns = [re.compile(p) for p in (forbidden_patterns or [])]
        
        # Слова
        self.forbidden_words = set(forbidden_words or [])
        self.required_words = set(required_words or [])
        
        # Валидация
        self.case_sensitive = case_sensitive
        self.suggest_corrections = suggest_corrections
        
        # Валидация параметров
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Проверить корректность конфигурации"""
        if self.min_length is not None and self.min_length < 0:
            raise ValueError("min_length не может быть отрицательным")
        
        if self.max_length is not None and self.max_length < 0:
            raise ValueError("max_length не может быть отрицательным")
        
        if (self.min_length is not None and self.max_length is not None 
            and self.min_length > self.max_length):
            raise ValueError("min_length не может быть больше max_length")
        
        if self.exact_length is not None and self.exact_length < 0:
            raise ValueError("exact_length не может быть отрицательным")
    
    def _validate_value(self, value: Any) -> str:
        """
        Основная логика валидации строки
        
        Args:
            value: Значение для валидации
            
        Returns:
            Валидированная строка
            
        Raises:
            StringValidationError: При ошибке валидации
        """
        # 1. Конвертация в строку
        text = self._convert_to_string(value)
        
        # 2. Автообработка
        text = self._apply_auto_processing(text)
        
        # 3. Проверка длины
        self._validate_length(text)
        
        # 4. Проверка содержимого
        self._validate_content(text)
        
        # 5. Проверка паттернов
        self._validate_patterns(text)
        
        # 6. Проверка слов
        self._validate_words(text)
        
        return text
    
    def _convert_to_string(self, value: Any) -> str:
        """Конвертировать значение в строку"""
        if isinstance(value, str):
            return value
        
        if value is None:
            return ""
        
        try:
            return str(value)
        except Exception:
            raise self._create_string_error(
                f"Невозможно конвертировать {type(value).__name__} в строку",
                value
            )
    
    def _apply_auto_processing(self, text: str) -> str:
        """Применить автоматическую обработку"""
        original_text = text
        
        # Убираем пробелы по краям
        if self.auto_trim:
            text = text.strip()
        
        # Убираем лишние пробелы
        if self.remove_extra_spaces:
            text = re.sub(r'\s+', ' ', text)
        
        # Нормализация регистра
        if self.normalize_case == "lower":
            text = text.lower()
        elif self.normalize_case == "upper":
            text = text.upper()
        elif self.normalize_case == "title":
            text = text.title()
        elif self.normalize_case == "smart":
            text = capitalize_words(text, smart=True)
        
        # Автоматическая капитализация
        if self.auto_capitalize and text:
            if self.normalize_case in ["lower", "upper", "title", "smart"]:
                # Уже обработано выше
                pass
            else:
                text = text[0].upper() + text[1:]
        
        return text
    
    def _validate_length(self, text: str):
        """Проверить длину строки"""
        length = len(text)
        
        # Точная длина
        if self.exact_length is not None:
            if length != self.exact_length:
                suggestions = [f"Длина должна быть ровно {self.exact_length} символов"]
                
                if length < self.exact_length:
                    needed = self.exact_length - length
                    suggestions.append(f"Добавьте {needed} символов")
                else:
                    excess = length - self.exact_length
                    suggestions.append(f"Удалите {excess} символов")
                
                raise self._create_string_error(
                    f"Неверная длина: {length} (требуется {self.exact_length})",
                    text,
                    suggestions=suggestions
                )
        
        # Минимальная длина
        if self.min_length is not None and length < self.min_length:
            suggestions = []
            
            if self.max_length is not None:
                suggestions.append(f"Длина должна быть от {self.min_length} до {self.max_length} символов")
            else:
                suggestions.append(f"Минимальная длина: {self.min_length} символов")
            
            needed = self.min_length - length
            suggestions.append(f"Добавьте еще {needed} символов")
            
            raise self._create_string_error(
                f"Строка слишком короткая: {length} (минимум {self.min_length})",
                text,
                suggestions=suggestions
            )
        
        # Максимальная длина
        if self.max_length is not None and length > self.max_length:
            suggestions = []
            
            if self.min_length is not None:
                suggestions.append(f"Длина должна быть от {self.min_length} до {self.max_length} символов")
            else:
                suggestions.append(f"Максимальная длина: {self.max_length} символов")
            
            excess = length - self.max_length
            suggestions.append(f"Удалите {excess} символов")
            
            raise self._create_string_error(
                f"Строка слишком длинная: {length} (максимум {self.max_length})",
                text,
                suggestions=suggestions
            )
    
    def _validate_content(self, text: str):
        """Проверить содержимое строки"""
        
        # Проверка букв
        if not self.allow_letters:
            if re.search(r'[a-zA-Zа-яА-ЯёЁ]', text):
                raise self._create_string_error(
                    "Буквы не разрешены",
                    text,
                    suggestions=["Используйте только цифры и символы"]
                )
        
        # Проверка цифр
        if not self.allow_numbers:
            if re.search(r'\d', text):
                raise self._create_string_error(
                    "Цифры не разрешены",
                    text,
                    suggestions=["Удалите все цифры"]
                )
        
        # Проверка пробелов
        if not self.allow_spaces:
            if ' ' in text:
                raise self._create_string_error(
                    "Пробелы не разрешены",
                    text,
                    suggestions=["Удалите все пробелы"]
                )
        
        # Проверка спецсимволов
        if not self.allow_special_chars:
            if re.search(r'[^a-zA-Zа-яА-ЯёЁ0-9\s]', text):
                raise self._create_string_error(
                    "Специальные символы не разрешены",
                    text,
                    suggestions=["Используйте только буквы, цифры и пробелы"]
                )
        
        # Проверка Unicode
        if not self.allow_unicode:
            try:
                text.encode('ascii')
            except UnicodeEncodeError:
                raise self._create_string_error(
                    "Unicode символы не разрешены",
                    text,
                    suggestions=["Используйте только ASCII символы"]
                )
    
    def _validate_patterns(self, text: str):
        """Проверить паттерны"""
        
        # Основной паттерн
        if self.pattern:
            if not self.pattern.match(text):
                raise self._create_string_error(
                    f"Строка не соответствует требуемому формату",
                    text,
                    suggestions=["Проверьте формат ввода"]
                )
        
        # Запрещенные паттерны
        for forbidden_pattern in self.forbidden_patterns:
            if forbidden_pattern.search(text):
                raise self._create_string_error(
                    "Строка содержит запрещенный паттерн",
                    text,
                    suggestions=["Измените формат строки"]
                )
    
    def _validate_words(self, text: str):
        """Проверить слова"""
        
        # Подготавливаем текст для проверки
        check_text = text if self.case_sensitive else text.lower()
        words_in_text = set(re.findall(r'\w+', check_text))
        
        # Запрещенные слова
        for forbidden_word in self.forbidden_words:
            check_word = forbidden_word if self.case_sensitive else forbidden_word.lower()
            
            if check_word in check_text:
                suggestions = ["Удалите запрещенное слово"]
                
                if self.suggest_corrections:
                    # Предлагаем замены (можно расширить)
                    suggestions.append("Используйте другие слова")
                
                raise self._create_string_error(
                    f"Содержит запрещенное слово: '{forbidden_word}'",
                    text,
                    suggestions=suggestions
                )
        
        # Обязательные слова
        for required_word in self.required_words:
            check_word = required_word if self.case_sensitive else required_word.lower()
            
            if check_word not in check_text:
                raise self._create_string_error(
                    f"Должно содержать слово: '{required_word}'",
                    text,
                    suggestions=[f"Добавьте слово '{required_word}'"]
                )
    
    def _create_string_error(self, message: str, value: Any = None, 
                           suggestions: List[str] = None) -> StringValidationError:
        """Создать ошибку валидации строки"""
        return StringValidationError(
            message=message,
            original_value=value,
            min_length=self.min_length,
            max_length=self.max_length,
            suggestions=suggestions or [],
            field_name=self.field_name
        )

# === ПРЕДУСТАНОВЛЕННЫЕ ВАЛИДАТОРЫ ===

class NameValidator(StringValidator):
    """Валидатор для имен людей"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_length', 2)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('auto_trim', True)
        kwargs.setdefault('normalize_case', 'smart')
        kwargs.setdefault('allow_numbers', False)
        kwargs.setdefault('allow_special_chars', False)
        super().__init__(**kwargs)

class UsernameValidator(StringValidator):
    """Валидатор для имен пользователей"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_length', 3)
        kwargs.setdefault('max_length', 30)
        kwargs.setdefault('auto_trim', True)
        kwargs.setdefault('normalize_case', 'lower')
        kwargs.setdefault('allow_spaces', False)
        kwargs.setdefault('pattern', r'^[a-zA-Z0-9_-]+$')
        super().__init__(**kwargs)

class CommentValidator(StringValidator):
    """Валидатор для комментариев"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('min_length', 1)
        kwargs.setdefault('max_length', 1000)
        kwargs.setdefault('auto_trim', True)
        kwargs.setdefault('remove_extra_spaces', True)
        super().__init__(**kwargs)

# === ДЕКОРАТОРЫ ===

# Основные декораторы
string = create_validator_decorator(StringValidator)
text = string  # Алиас

# Специализированные декораторы
name = create_validator_decorator(NameValidator)
username = create_validator_decorator(UsernameValidator)
comment = create_validator_decorator(CommentValidator)

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

def demo_string_validators():
    """Демонстрация валидаторов строк"""
    
    print(colorize("📝 PyDefender String Validators Demo", Color.BRIGHT_CYAN, bold=True))
    print("=" * 50)
    
    # Простой валидатор строк
    @string(min_length=2, max_length=20, auto_trim=True)
    def set_title(title):
        return f"Заголовок: {title}"
    
    # Валидатор имени
    @name()
    def set_name(person_name):
        return f"Имя: {person_name}"
    
    # Валидатор с запрещенными словами
    @string(forbidden_words=["спам", "реклама"], min_length=5)
    def set_message(message):
        return f"Сообщение: {message}"
    
    # Тестирование
    test_cases = [
        (set_title, ["Привет", "  Заголовок  ", "Очень длинный заголовок статьи"]),
        (set_name, ["иван", "  Мария Петрова  ", "X"]),
        (set_message, ["Привет всем", "спам сообщение", "Hi"])
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

if __name__ == "__main__":
    demo_string_validators()