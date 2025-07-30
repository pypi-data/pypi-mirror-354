#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Utils
================

Утилиты для красивого форматирования и обработки данных
"""

import re
import math
import difflib
from typing import Any, List, Optional, Union, Dict, Tuple
from enum import Enum

class Color(Enum):
    """ANSI цвета для консоли"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Основные цвета
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Яркие цвета
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Фоновые цвета
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"

class EmojiSet:
    """Набор эмодзи для разных ситуаций"""
    
    # Статусы
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    QUESTION = "❓"
    
    # Действия
    SEARCH = "🔍"
    EDIT = "✏️"
    DELETE = "🗑️"
    SAVE = "💾"
    COPY = "📋"
    
    # Типы данных
    NUMBER = "🔢"
    TEXT = "📝"
    EMAIL = "📧"
    PHONE = "📱"
    DATE = "📅"
    FILE = "📁"
    
    # Процессы
    LOADING = "⏳"
    THINKING = "🤔"
    ROCKET = "🚀"
    MAGIC = "✨"
    SHIELD = "🛡️"
    
    # Категории
    SECURITY = "🔒"
    PERFORMANCE = "⚡"
    BUG = "🐛"
    FEATURE = "🎯"

def colorize(text: str, color: Union[Color, str], bold: bool = False) -> str:
    """
    Раскрасить текст для консоли
    
    Args:
        text: Текст для раскрашивания
        color: Цвет (Color enum или строка)
        bold: Сделать жирным
        
    Returns:
        Раскрашенный текст
    """
    from .config import get_config
    
    config = get_config()
    if not config.show_colors:
        return text
    
    # Конвертируем строку в Color
    if isinstance(color, str):
        color_map = {
            'red': Color.RED,
            'green': Color.GREEN,
            'yellow': Color.YELLOW,
            'blue': Color.BLUE,
            'magenta': Color.MAGENTA,
            'cyan': Color.CYAN,
            'white': Color.WHITE,
            'bright_red': Color.BRIGHT_RED,
            'bright_green': Color.BRIGHT_GREEN,
            'bright_yellow': Color.BRIGHT_YELLOW,
            'bright_blue': Color.BRIGHT_BLUE,
        }
        color = color_map.get(color.lower(), Color.WHITE)
    
    # Собираем ANSI код
    ansi_code = color.value
    if bold:
        ansi_code += Color.BOLD.value
    
    return f"{ansi_code}{text}{Color.RESET.value}"

def add_emoji(text: str, emoji: str) -> str:
    """
    Добавить эмодзи к тексту
    
    Args:
        text: Исходный текст
        emoji: Эмодзи для добавления
        
    Returns:
        Текст с эмодзи
    """
    from .config import get_config
    
    config = get_config()
    if not config.show_emojis:
        return text
    
    return f"{emoji} {text}"

def format_error_message(error) -> str:
    """
    Форматировать сообщение об ошибке
    
    Args:
        error: Объект ошибки
        
    Returns:
        Красиво отформатированное сообщение
    """
    from .exceptions import ValidationError
    
    lines = []
    
    # Заголовок ошибки
    error_text = colorize(error.message, Color.BRIGHT_RED, bold=True)
    lines.append(add_emoji(error_text, EmojiSet.ERROR))
    
    # Дополнительная информация для ValidationError
    if isinstance(error, ValidationError):
        if error.original_value is not None:
            value_text = colorize(f"Получено: {repr(error.original_value)}", Color.DIM)
            lines.append(f"  {value_text}")
        
        if error.expected_type:
            expected_text = colorize(f"Ожидается: {error.expected_type}", Color.CYAN)
            lines.append(f"  {expected_text}")
        
        # Предложения
        if error.suggestions:
            suggestions_header = colorize("Предложения:", Color.BRIGHT_YELLOW, bold=True)
            lines.append(f"\n{add_emoji(suggestions_header, EmojiSet.INFO)}")
            
            for suggestion in error.suggestions:
                suggestion_text = colorize(f"• {suggestion}", Color.YELLOW)
                lines.append(f"  {suggestion_text}")
    
    return "\n".join(lines)

def format_success_message(message: str, value: Any = None) -> str:
    """
    Форматировать сообщение об успехе
    
    Args:
        message: Сообщение
        value: Значение (опционально)
        
    Returns:
        Красиво отформатированное сообщение
    """
    success_text = colorize(message, Color.BRIGHT_GREEN, bold=True)
    result = add_emoji(success_text, EmojiSet.SUCCESS)
    
    if value is not None:
        value_text = colorize(f"Значение: {repr(value)}", Color.GREEN)
        result += f"\n  {value_text}"
    
    return result

def extract_numbers_from_string(text: str) -> List[Union[int, float]]:
    """
    Извлечь все числа из строки
    
    Args:
        text: Исходная строка
        
    Returns:
        Список найденных чисел
    """
    # Паттерн для поиска чисел (включая отрицательные и дробные)
    pattern = r'-?\d+(?:\.\d+)?'
    matches = re.findall(pattern, str(text))
    
    numbers = []
    for match in matches:
        try:
            # Пробуем сначала как int, потом как float
            if '.' in match:
                numbers.append(float(match))
            else:
                numbers.append(int(match))
        except ValueError:
            continue
    
    return numbers

def extract_first_number(text: str) -> Optional[Union[int, float]]:
    """
    Извлечь первое число из строки
    
    Args:
        text: Исходная строка
        
    Returns:
        Первое найденное число или None
    """
    numbers = extract_numbers_from_string(text)
    return numbers[0] if numbers else None

def clean_string(text: str, 
                 strip_spaces: bool = True,
                 remove_extra_spaces: bool = True,
                 normalize_case: bool = False) -> str:
    """
    Очистить строку от лишних символов
    
    Args:
        text: Исходная строка
        strip_spaces: Убрать пробелы с краев
        remove_extra_spaces: Убрать лишние пробелы внутри
        normalize_case: Нормализовать регистр
        
    Returns:
        Очищенная строка
    """
    if not isinstance(text, str):
        text = str(text)
    
    if strip_spaces:
        text = text.strip()
    
    if remove_extra_spaces:
        text = re.sub(r'\s+', ' ', text)
    
    if normalize_case:
        text = text.lower()
    
    return text

def capitalize_words(text: str, smart: bool = True) -> str:
    """
    Сделать первые буквы слов заглавными
    
    Args:
        text: Исходная строка
        smart: Умная капитализация (учитывает предлоги)
        
    Returns:
        Строка с заглавными буквами
    """
    if not text:
        return text
    
    if not smart:
        return text.title()
    
    # Список предлогов и союзов (не делаем заглавными)
    small_words = {
        'и', 'или', 'но', 'а', 'да', 'что', 'как', 'где', 'когда',
        'от', 'до', 'для', 'на', 'в', 'с', 'из', 'по', 'за', 'под',
        'над', 'при', 'без', 'через', 'между', 'возле', 'около'
    }
    
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        word_lower = word.lower()
        if i == 0 or word_lower not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word_lower)
    
    return ' '.join(result)

def suggest_similar_strings(target: str, 
                          candidates: List[str], 
                          max_suggestions: int = 3,
                          min_similarity: float = 0.6) -> List[str]:
    """
    Предложить похожие строки на основе расстояния редактирования
    
    Args:
        target: Целевая строка
        candidates: Список кандидатов
        max_suggestions: Максимум предложений
        min_similarity: Минимальная схожесть (0-1)
        
    Returns:
        Список похожих строк
    """
    if not target or not candidates:
        return []
    
    target_lower = target.lower()
    scored_candidates = []
    
    for candidate in candidates:
        candidate_lower = candidate.lower()
        similarity = difflib.SequenceMatcher(None, target_lower, candidate_lower).ratio()
        
        if similarity >= min_similarity:
            scored_candidates.append((candidate, similarity))
    
    # Сортируем по убыванию схожести
    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    
    return [candidate for candidate, _ in scored_candidates[:max_suggestions]]

def suggest_email_domains(email_part: str) -> List[str]:
    """
    Предложить популярные домены для email
    
    Args:
        email_part: Часть email (может быть неполной)
        
    Returns:
        Список предложений доменов
    """
    popular_domains = [
        'gmail.com', 'mail.ru', 'yandex.ru', 'outlook.com', 'yahoo.com',
        'hotmail.com', 'icloud.com', 'rambler.ru', 'list.ru', 'bk.ru'
    ]
    
    if '@' in email_part:
        user_part, domain_part = email_part.rsplit('@', 1)
        suggestions = suggest_similar_strings(domain_part, popular_domains, max_suggestions=3)
        return [f"{user_part}@{domain}" for domain in suggestions]
    
    return [f"{email_part}@{domain}" for domain in popular_domains[:3]]

def format_phone_number(phone: str, format_type: str = "international") -> str:
    """
    Форматировать номер телефона
    
    Args:
        phone: Исходный номер
        format_type: Тип форматирования ("international", "national", "compact")
        
    Returns:
        Отформатированный номер
    """
    # Убираем все кроме цифр
    digits = re.sub(r'\D', '', phone)
    
    if not digits:
        return phone
    
    # Российские номера
    if digits.startswith('7') and len(digits) == 11:
        if format_type == "international":
            return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        elif format_type == "national":
            return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        else:  # compact
            return f"+7{digits[1:]}"
    
    elif digits.startswith('8') and len(digits) == 11:
        if format_type == "international":
            return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        elif format_type == "national":
            return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        else:  # compact
            return f"+7{digits[1:]}"
    
    # Если не удалось определить формат, возвращаем как есть
    return phone

def mask_sensitive_data(text: str, mask_char: str = "*", 
                       visible_start: int = 2, visible_end: int = 2) -> str:
    """
    Замаскировать чувствительные данные
    
    Args:
        text: Исходный текст
        mask_char: Символ для маскирования
        visible_start: Сколько символов показать в начале
        visible_end: Сколько символов показать в конце
        
    Returns:
        Замаскированная строка
    """
    if len(text) <= visible_start + visible_end:
        return mask_char * len(text)
    
    start = text[:visible_start]
    end = text[-visible_end:] if visible_end > 0 else ""
    middle_length = len(text) - visible_start - visible_end
    middle = mask_char * middle_length
    
    return start + middle + end

def progress_bar(current: int, total: int, width: int = 50, 
                 show_percent: bool = True, show_numbers: bool = True) -> str:
    """
    Создать текстовый прогресс-бар
    
    Args:
        current: Текущее значение
        total: Общее количество
        width: Ширина бара
        show_percent: Показывать проценты
        show_numbers: Показывать числа
        
    Returns:
        Строка с прогресс-баром
    """
    if total <= 0:
        return "Invalid progress values"
    
    percent = min(100, max(0, (current / total) * 100))
    filled_width = int((current / total) * width)
    
    bar = "█" * filled_width + "░" * (width - filled_width)
    
    result_parts = [bar]
    
    if show_percent:
        result_parts.append(f" {percent:.1f}%")
    
    if show_numbers:
        result_parts.append(f" ({current}/{total})")
    
    return "".join(result_parts)

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Обрезать текст до заданной длины
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    
    if max_length <= len(suffix):
        return suffix[:max_length]
    
    return text[:max_length - len(suffix)] + suffix

def format_file_size(size_bytes: int) -> str:
    """
    Форматировать размер файла в человекочитаемый вид
    
    Args:
        size_bytes: Размер в байтах
        
    Returns:
        Отформатированная строка
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def parse_boolean(value: Any) -> bool:
    """
    Умный парсинг логических значений
    
    Args:
        value: Значение для парсинга
        
    Returns:
        Логическое значение
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, (int, float)):
        return value != 0
    
    if isinstance(value, str):
        value_lower = value.lower().strip()
        true_values = {'true', '1', 'yes', 'on', 'да', 'истина', 'включено'}
        false_values = {'false', '0', 'no', 'off', 'нет', 'ложь', 'выключено'}
        
        if value_lower in true_values:
            return True
        elif value_lower in false_values:
            return False
    
    # По умолчанию считаем непустые значения как True
    return bool(value)

def smart_round(value: float, precision: int = 2) -> Union[int, float]:
    """
    Умное округление (возвращает int если нет дробной части)
    
    Args:
        value: Число для округления
        precision: Количество знаков после запятой
        
    Returns:
        Округленное число
    """
    rounded = round(value, precision)
    if rounded == int(rounded):
        return int(rounded)
    return rounded

# === ВАЛИДАЦИОННЫЕ УТИЛИТЫ ===

def is_valid_email_format(email: str) -> bool:
    """Базовая проверка формата email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_phone_format(phone: str) -> bool:
    """Базовая проверка формата телефона"""
    # Убираем все кроме цифр и плюса
    clean_phone = re.sub(r'[^\d+]', '', phone)
    
    # Проверяем основные форматы
    patterns = [
        r'^\+7\d{10}$',      # +7XXXXXXXXXX
        r'^8\d{10}$',        # 8XXXXXXXXXX
        r'^\+\d{10,15}$',    # Международный формат
    ]
    
    return any(re.match(pattern, clean_phone) for pattern in patterns)

def is_numeric_string(text: str) -> bool:
    """Проверить, содержит ли строка только числа"""
    try:
        float(text)
        return True
    except ValueError:
        return False

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

def demo_utils():
    """Демонстрация утилит"""
    
    print(colorize("🛡️ PyDefender Utils Demo", Color.BRIGHT_CYAN, bold=True))
    print()
    
    # Цвета и эмодзи
    print(add_emoji("Успешная валидация", EmojiSet.SUCCESS))
    print(add_emoji(colorize("Ошибка валидации", Color.RED), EmojiSet.ERROR))
    print()
    
    # Извлечение чисел
    text = "Мне 25 лет, рост 180.5 см"
    numbers = extract_numbers_from_string(text)
    print(f"Текст: {text}")
    print(f"Числа: {numbers}")
    print()
    
    # Предложения
    suggestions = suggest_similar_strings("gmai.com", ["gmail.com", "mail.ru", "yahoo.com"])
    print(f"Предложения для 'gmai.com': {suggestions}")
    print()
    
    # Прогресс
    print("Прогресс валидации:")
    for i in range(0, 101, 20):
        print(f"  {progress_bar(i, 100)}")

if __name__ == "__main__":
    demo_utils()