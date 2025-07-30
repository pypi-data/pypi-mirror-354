#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Decorators System
============================

Красивые декораторы для валидации функций
"""

import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union, Type
from .config import get_config
from .exceptions import ValidationError, RetryLimitError
from .validators.base import BaseValidator
from .utils import format_error_message, format_success_message, colorize, add_emoji, EmojiSet, Color

class ValidationDecorator:
    """
    Базовый класс для декораторов валидации
    
    Обеспечивает красивое отображение ошибок и автоматические повторы
    """
    
    def __init__(self, validator: BaseValidator):
        """
        Args:
            validator: Валидатор для применения
        """
        self.validator = validator
        self.config = get_config()
    
    def __call__(self, func: Callable) -> Callable:
        """
        Применить валидацию к функции
        
        Args:
            func: Функция для декорирования
            
        Returns:
            Декорированная функция
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Определяем какой аргумент валидировать
            target_value = self._get_target_value(func, args, kwargs)
            
            if target_value is None:
                # Нет аргументов для валидации
                return func(*args, **kwargs)
            
            # Валидируем с возможными повторами
            validated_value = self._validate_with_retry(target_value)
            
            # Заменяем аргумент на валидированное значение
            new_args, new_kwargs = self._replace_target_value(
                func, args, kwargs, validated_value
            )
            
            # Вызываем функцию с валидированными аргументами
            return func(*new_args, **new_kwargs)
        
        # Добавляем метаданные
        wrapper._pydefender_validator = self.validator
        wrapper._pydefender_original = func
        
        return wrapper
    
    def _get_target_value(self, func: Callable, args: tuple, kwargs: dict) -> Any:
        """
        Определить какое значение нужно валидировать
        
        Args:
            func: Функция
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            
        Returns:
            Значение для валидации или None
        """
        # Получаем сигнатуру функции
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        # Если есть имя поля в валидаторе, ищем его
        if self.validator.field_name:
            if self.validator.field_name in kwargs:
                return kwargs[self.validator.field_name]
            
            # Ищем по позиции
            try:
                param_index = params.index(self.validator.field_name)
                if param_index < len(args):
                    return args[param_index]
            except ValueError:
                pass
        
        # По умолчанию валидируем первый аргумент
        if args:
            return args[0]
        
        # Или первый именованный аргумент
        if kwargs and params:
            first_param = params[0]
            if first_param in kwargs:
                return kwargs[first_param]
        
        return None
    
    def _replace_target_value(self, func: Callable, args: tuple, kwargs: dict, 
                            new_value: Any) -> tuple[tuple, dict]:
        """
        Заменить целевое значение на валидированное
        
        Args:
            func: Функция
            args: Исходные позиционные аргументы
            kwargs: Исходные именованные аргументы
            new_value: Новое значение
            
        Returns:
            Кортеж (новые_args, новые_kwargs)
        """
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        new_args = list(args)
        new_kwargs = kwargs.copy()
        
        # Если есть имя поля, заменяем его
        if self.validator.field_name:
            if self.validator.field_name in kwargs:
                new_kwargs[self.validator.field_name] = new_value
                return tuple(new_args), new_kwargs
            
            # Заменяем по позиции
            try:
                param_index = params.index(self.validator.field_name)
                if param_index < len(new_args):
                    new_args[param_index] = new_value
                    return tuple(new_args), new_kwargs
            except ValueError:
                pass
        
        # По умолчанию заменяем первый аргумент
        if new_args:
            new_args[0] = new_value
        elif kwargs and params:
            first_param = params[0]
            if first_param in new_kwargs:
                new_kwargs[first_param] = new_value
        
        return tuple(new_args), new_kwargs
    
    def _validate_with_retry(self, value: Any) -> Any:
        """
        Валидация с возможными повторами
        
        Args:
            value: Значение для валидации
            
        Returns:
            Валидированное значение
            
        Raises:
            ValidationError: При ошибке валидации
            RetryLimitError: При превышении лимита попыток
        """
        attempt = 0
        last_error = None
        
        while attempt < self.config.max_attempts:
            try:
                # Пробуем валидацию
                return self.validator.validate(value)
                
            except ValidationError as e:
                last_error = e
                attempt += 1
                
                # Показываем красивое сообщение об ошибке
                self._display_error(e, attempt)
                
                # Если это последняя попытка или отключены повторы
                if attempt >= self.config.max_attempts or not self.config.auto_retry:
                    break
                
                # Запрашиваем новое значение
                value = self._prompt_for_new_value(e, attempt)
                if value is None:
                    break
        
        # Превышен лимит попыток
        if last_error:
            if attempt >= self.config.max_attempts:
                raise RetryLimitError(
                    f"Превышен лимит попыток ({self.config.max_attempts})",
                    attempt,
                    self.config.max_attempts
                )
            raise last_error
        
        return value
    
    def _display_error(self, error: ValidationError, attempt: int):
        """
        Показать красивое сообщение об ошибке
        
        Args:
            error: Ошибка валидации
            attempt: Номер попытки
        """
        print()  # Отступ
        
        # Заголовок
        if attempt == 1:
            header = colorize("Ошибка валидации", Color.BRIGHT_RED, bold=True)
        else:
            header = colorize(f"Ошибка валидации (попытка {attempt})", Color.BRIGHT_RED, bold=True)
        
        print(add_emoji(header, EmojiSet.ERROR))
        
        # Основное сообщение
        print(f"  {colorize(error.message, Color.RED)}")
        
        # Дополнительная информация
        if error.original_value is not None:
            value_text = colorize(f"Получено: {repr(error.original_value)}", Color.DIM)
            print(f"  {value_text}")
        
        # Предложения
        if error.suggestions:
            suggestions_header = colorize("Предложения:", Color.BRIGHT_YELLOW, bold=True)
            print(f"\n{add_emoji(suggestions_header, EmojiSet.INFO)}")
            
            for suggestion in error.suggestions:
                suggestion_text = colorize(f"• {suggestion}", Color.YELLOW)
                print(f"  {suggestion_text}")
        
        # Информация о повторах
        if self.config.auto_retry and attempt < self.config.max_attempts:
            remaining = self.config.max_attempts - attempt
            retry_text = colorize(f"Осталось попыток: {remaining}", Color.CYAN)
            print(f"\n  {retry_text}")
    
    def _prompt_for_new_value(self, error: ValidationError, attempt: int) -> Any:
        """
        Запросить новое значение у пользователя
        
        Args:
            error: Ошибка валидации
            attempt: Номер попытки
            
        Returns:
            Новое значение или None для отмены
        """
        try:
            print()
            prompt_text = colorize("Введите новое значение: ", Color.BRIGHT_CYAN, bold=True)
            prompt = add_emoji(prompt_text, EmojiSet.EDIT)
            
            new_value = input(prompt)
            
            # Проверяем на отмену
            if new_value.lower().strip() in ['q', 'quit', 'exit', 'отмена', 'cancel']:
                return None
            
            return new_value
            
        except (KeyboardInterrupt, EOFError):
            print(colorize("\nОтменено пользователем", Color.YELLOW))
            return None

def create_validator_decorator(validator_class: Type[BaseValidator]):
    """
    Фабрика для создания декораторов валидации
    
    Args:
        validator_class: Класс валидатора
        
    Returns:
        Функция-декоратор
    """
    def decorator(**validator_kwargs):
        """
        Декоратор с параметрами валидатора
        
        Args:
            **validator_kwargs: Параметры для валидатора
            
        Returns:
            Декоратор функции
        """
        def function_decorator(func: Callable) -> Callable:
            """
            Декоратор функции
            
            Args:
                func: Функция для декорирования
                
            Returns:
                Декорированная функция
            """
            # Создаем валидатор
            validator = validator_class(**validator_kwargs)
            
            # Создаем и применяем декоратор валидации
            validation_decorator = ValidationDecorator(validator)
            return validation_decorator(func)
        
        return function_decorator
    
    return decorator

class FormValidator:
    """
    Валидатор для форм с несколькими полями
    """
    
    def __init__(self, field_validators: Dict[str, BaseValidator]):
        """
        Args:
            field_validators: Словарь {имя_поля: валидатор}
        """
        self.field_validators = field_validators
        self.config = get_config()
    
    def __call__(self, func: Callable) -> Callable:
        """
        Применить валидацию формы к функции
        
        Args:
            func: Функция для декорирования
            
        Returns:
            Декорированная функция
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем данные формы
            form_data = self._extract_form_data(func, args, kwargs)
            
            if not form_data:
                return func(*args, **kwargs)
            
            # Валидируем все поля
            validated_data = self._validate_form(form_data)
            
            # Заменяем данные на валидированные
            new_args, new_kwargs = self._replace_form_data(
                func, args, kwargs, validated_data
            )
            
            return func(*new_args, **new_kwargs)
        
        return wrapper
    
    def _extract_form_data(self, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """Извлечь данные формы из аргументов"""
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        form_data = {}
        
        # Ищем поля в именованных аргументах
        for field_name in self.field_validators.keys():
            if field_name in kwargs:
                form_data[field_name] = kwargs[field_name]
        
        # Ищем по позициям
        for i, arg in enumerate(args):
            if i < len(params):
                param_name = params[i]
                if param_name in self.field_validators:
                    form_data[param_name] = arg
        
        return form_data
    
    def _validate_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидировать все поля формы"""
        validated_data = {}
        errors = []
        
        for field_name, value in form_data.items():
            if field_name in self.field_validators:
                validator = self.field_validators[field_name]
                
                try:
                    validated_data[field_name] = validator.validate(value)
                except ValidationError as e:
                    e.field_name = field_name
                    errors.append(e)
            else:
                validated_data[field_name] = value
        
        # Если есть ошибки, показываем их все
        if errors:
            self._display_form_errors(errors)
            
            # Поднимаем первую ошибку
            raise errors[0]
        
        return validated_data
    
    def _display_form_errors(self, errors: List[ValidationError]):
        """Показать ошибки формы"""
        print()
        header = colorize("Ошибки в форме", Color.BRIGHT_RED, bold=True)
        print(add_emoji(header, EmojiSet.ERROR))
        
        for i, error in enumerate(errors, 1):
            field_text = colorize(f"Поле '{error.field_name}':", Color.BRIGHT_RED)
            print(f"\n  {i}. {field_text}")
            print(f"     {colorize(error.message, Color.RED)}")
            
            if error.suggestions:
                for suggestion in error.suggestions[:2]:  # Показываем только первые 2
                    print(f"     {colorize(f'💡 {suggestion}', Color.YELLOW)}")
    
    def _replace_form_data(self, func: Callable, args: tuple, kwargs: dict, 
                          validated_data: Dict[str, Any]) -> tuple[tuple, dict]:
        """Заменить данные формы на валидированные"""
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        new_args = list(args)
        new_kwargs = kwargs.copy()
        
        # Заменяем именованные аргументы
        for field_name, value in validated_data.items():
            if field_name in kwargs:
                new_kwargs[field_name] = value
        
        # Заменяем позиционные аргументы
        for i, param_name in enumerate(params):
            if param_name in validated_data and i < len(new_args):
                new_args[i] = validated_data[param_name]
        
        return tuple(new_args), new_kwargs

def form_validator(**field_validators) -> FormValidator:
    """
    Создать валидатор формы
    
    Args:
        **field_validators: Именованные валидаторы полей
        
    Returns:
        FormValidator
    
    Examples:
        @form_validator(
            name=StringValidator(min_length=2),
            age=NumberValidator(min_value=0, max_value=150),
            email=EmailValidator()
        )
        def register_user(name, age, email):
            return f"User {name}, {age} years old, {email}"
    """
    return FormValidator(field_validators)

class ConditionalDecorator:
    """
    Условный декоратор - применяется только при выполнении условия
    """
    
    def __init__(self, condition: Callable, decorator: Callable):
        """
        Args:
            condition: Функция условия
            decorator: Декоратор для применения
        """
        self.condition = condition
        self.decorator = decorator
    
    def __call__(self, func: Callable) -> Callable:
        """Применить декоратор условно"""
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверяем условие
            if self.condition(*args, **kwargs):
                # Применяем декоратор динамически
                decorated_func = self.decorator(func)
                return decorated_func(*args, **kwargs)
            else:
                # Вызываем функцию без декорации
                return func(*args, **kwargs)
        
        return wrapper

def conditional(condition: Callable) -> Callable:
    """
    Создать условный декоратор
    
    Args:
        condition: Функция условия
        
    Returns:
        Декоратор
    
    Examples:
        @conditional(lambda x: isinstance(x, str))
        @string_validator(min_length=5)
        def process_data(data):
            return data
    """
    def decorator_factory(decorator):
        return ConditionalDecorator(condition, decorator)
    
    return decorator_factory

class RetryableDecorator:
    """
    Декоратор для функций с возможностью повтора при ошибках
    """
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        """
        Args:
            max_retries: Максимум повторов
            delay: Задержка между повторами
        """
        self.max_retries = max_retries
        self.delay = delay
    
    def __call__(self, func: Callable) -> Callable:
        """Применить повторы к функции"""
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            last_exception = None
            
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except ValidationError as e:
                    last_exception = e
                    
                    if attempt < self.max_retries:
                        retry_text = colorize(
                            f"Попытка {attempt + 1} не удалась, повтор через {self.delay}с...",
                            Color.YELLOW
                        )
                        print(add_emoji(retry_text, EmojiSet.LOADING))
                        time.sleep(self.delay)
                    else:
                        break
            
            # Все попытки исчерпаны
            if last_exception:
                raise RetryLimitError(
                    f"Все {self.max_retries + 1} попыток неудачны",
                    self.max_retries + 1,
                    self.max_retries
                ) from last_exception
        
        return wrapper

def retryable(max_retries: int = 3, delay: float = 1.0) -> RetryableDecorator:
    """
    Декоратор для повторов функции
    
    Args:
        max_retries: Максимум повторов
        delay: Задержка между повторами
        
    Returns:
        RetryableDecorator
    """
    return RetryableDecorator(max_retries, delay)

# === СПЕЦИАЛЬНЫЕ ДЕКОРАТОРЫ ===

def debug_validator(func: Callable) -> Callable:
    """
    Декоратор для отладки валидации
    
    Показывает подробную информацию о процессе валидации
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(colorize("🐛 Debug: Вызов функции с валидацией", Color.CYAN))
        print(f"  Функция: {func.__name__}")
        print(f"  Аргументы: {args}")
        print(f"  Ключевые аргументы: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            print(colorize("🐛 Debug: Валидация успешна", Color.GREEN))
            print(f"  Результат: {result}")
            return result
            
        except Exception as e:
            print(colorize("🐛 Debug: Ошибка валидации", Color.RED))
            print(f"  Ошибка: {e}")
            raise
    
    return wrapper

def performance_monitor(func: Callable) -> Callable:
    """
    Декоратор для мониторинга производительности валидации
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            if duration > 0.1:  # Показываем только медленные операции
                perf_text = colorize(
                    f"⚡ Валидация заняла {duration:.3f}s",
                    Color.YELLOW
                )
                print(perf_text)
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            error_text = colorize(
                f"⚡ Валидация с ошибкой заняла {duration:.3f}s",
                Color.RED
            )
            print(error_text)
            raise
    
    return wrapper

def silent_validator(func: Callable) -> Callable:
    """
    Декоратор для тихой валидации (без вывода сообщений)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Временно отключаем вывод
        original_config = get_config()
        original_colors = original_config.show_colors
        original_emojis = original_config.show_emojis
        
        try:
            original_config.show_colors = False
            original_config.show_emojis = False
            
            return func(*args, **kwargs)
            
        finally:
            # Восстанавливаем настройки
            original_config.show_colors = original_colors
            original_config.show_emojis = original_emojis
    
    return wrapper

# === УТИЛИТЫ ===

def get_validator_info(func: Callable) -> Optional[Dict[str, Any]]:
    """
    Получить информацию о валидаторе функции
    
    Args:
        func: Функция с валидатором
        
    Returns:
        Информация о валидаторе или None
    """
    if hasattr(func, '_pydefender_validator'):
        validator = func._pydefender_validator
        return {
            'validator_type': validator.__class__.__name__,
            'statistics': validator.get_statistics(),
            'original_function': getattr(func, '_pydefender_original', None)
        }
    
    return None

def remove_validation(func: Callable) -> Callable:
    """
    Удалить валидацию с функции
    
    Args:
        func: Функция с валидатором
        
    Returns:
        Исходная функция без валидации
    """
    return getattr(func, '_pydefender_original', func)

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

def demo_decorators():
    """Демонстрация декораторов"""
    
    print(colorize("🛡️ PyDefender Decorators Demo", Color.BRIGHT_CYAN, bold=True))
    print("=" * 40)
    
    # Простой валидатор (будет создан позже)
    # @number_validator(min_value=0, max_value=100)
    # def set_score(score):
    #     return f"Счет: {score}"
    
    # Форма
    # @form_validator(
    #     name=string_validator(min_length=2),
    #     age=number_validator(min_value=0, max_value=150)
    # )
    # def create_user(name, age):
    #     return f"Пользователь: {name}, {age} лет"
    
    print("Примеры будут работать после создания валидаторов чисел и строк")

if __name__ == "__main__":
    demo_decorators()