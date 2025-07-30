#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDefender Base Validator
=========================

Базовый класс для всех валидаторов PyDefender
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Callable, Type
from ..config import get_config
from ..exceptions import ValidationError, PyDefenderError
from ..utils import format_error_message, format_success_message

class BaseValidator(ABC):
    """
    Абстрактный базовый класс для всех валидаторов
    
    Определяет общий интерфейс и базовую функциональность
    """
    
    def __init__(self, 
                 error_message: Optional[str] = None,
                 success_message: Optional[str] = None,
                 field_name: Optional[str] = None,
                 required: bool = True,
                 allow_none: bool = False,
                 custom_validator: Optional[Callable[[Any], bool]] = None,
                 preprocessor: Optional[Callable[[Any], Any]] = None,
                 postprocessor: Optional[Callable[[Any], Any]] = None,
                 **kwargs):
        """
        Инициализация базового валидатора
        
        Args:
            error_message: Кастомное сообщение об ошибке
            success_message: Сообщение об успехе
            field_name: Имя поля (для форм)
            required: Обязательное ли поле
            allow_none: Разрешить None значения
            custom_validator: Дополнительная функция валидации
            preprocessor: Функция предобработки
            postprocessor: Функция постобработки
            **kwargs: Дополнительные параметры
        """
        self.error_message = error_message
        self.success_message = success_message
        self.field_name = field_name
        self.required = required
        self.allow_none = allow_none
        self.custom_validator = custom_validator
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor
        
        # Сохраняем все параметры для отладки
        self.config_params = kwargs
        
        # Статистика валидации
        self.validation_count = 0
        self.success_count = 0
        self.error_count = 0
        
        # Конфигурация
        self._config = get_config()
    
    @abstractmethod
    def _validate_value(self, value: Any) -> Any:
        """
        Основная логика валидации (должна быть реализована в наследниках)
        
        Args:
            value: Значение для валидации
            
        Returns:
            Валидированное и возможно преобразованное значение
            
        Raises:
            ValidationError: При ошибке валидации
        """
        pass
    
    def validate(self, value: Any) -> Any:
        """
        Полный цикл валидации с предобработкой и постобработкой
        
        Args:
            value: Значение для валидации
            
        Returns:
            Валидированное значение
            
        Raises:
            ValidationError: При ошибке валидации
        """
        self.validation_count += 1
        
        try:
            # 1. Проверка на None
            if value is None:
                if self.allow_none:
                    return None
                elif not self.required:
                    return None
                else:
                    raise self._create_error("Значение не может быть пустым")
            
            # 2. Проверка на пустое значение
            if not self.required and self._is_empty_value(value):
                return self._get_default_value()
            
            # 3. Предобработка
            if self.preprocessor:
                try:
                    value = self.preprocessor(value)
                except Exception as e:
                    raise self._create_error(f"Ошибка предобработки: {e}")
            
            # 4. Основная валидация
            validated_value = self._validate_value(value)
            
            # 5. Дополнительная валидация
            if self.custom_validator:
                try:
                    if not self.custom_validator(validated_value):
                        raise self._create_error("Значение не прошло дополнительную проверку")
                except Exception as e:
                    if isinstance(e, ValidationError):
                        raise
                    raise self._create_error(f"Ошибка дополнительной валидации: {e}")
            
            # 6. Постобработка
            if self.postprocessor:
                try:
                    validated_value = self.postprocessor(validated_value)
                except Exception as e:
                    raise self._create_error(f"Ошибка постобработки: {e}")
            
            # 7. Успех
            self.success_count += 1
            self._log_success(validated_value)
            
            return validated_value
            
        except ValidationError as e:
            self.error_count += 1
            # Добавляем имя поля если есть
            if self.field_name and not e.field_name:
                e.field_name = self.field_name
            self._log_error(e)
            raise
        except Exception as e:
            self.error_count += 1
            # Оборачиваем неожиданные ошибки
            wrapped_error = self._create_error(f"Неожиданная ошибка: {e}")
            self._log_error(wrapped_error)
            raise wrapped_error
    
    def _is_empty_value(self, value: Any) -> bool:
        """
        Проверить, является ли значение пустым
        
        Args:
            value: Значение для проверки
            
        Returns:
            True если значение считается пустым
        """
        if value is None:
            return True
        
        if isinstance(value, str):
            return value.strip() == ""
        
        if isinstance(value, (list, dict, tuple, set)):
            return len(value) == 0
        
        return False
    
    def _get_default_value(self) -> Any:
        """
        Получить значение по умолчанию для необязательных полей
        
        Returns:
            Значение по умолчанию
        """
        return None
    
    def _create_error(self, 
                     message: str, 
                     suggestions: Optional[List[str]] = None,
                     original_value: Any = None) -> ValidationError:
        """
        Создать ошибку валидации
        
        Args:
            message: Сообщение об ошибке
            suggestions: Предложения по исправлению
            original_value: Исходное значение
            
        Returns:
            ValidationError
        """
        # Используем кастомное сообщение если есть
        if self.error_message:
            message = self.error_message
        
        error = ValidationError(
            message=message,
            suggestions=suggestions or [],
            original_value=original_value,
            field_name=self.field_name
        )
        
        return error
    
    def _log_success(self, value: Any):
        """
        Логировать успешную валидацию
        
        Args:
            value: Валидированное значение
        """
        if self._config.log_attempts:
            print(f"✅ Валидация успешна: {self.__class__.__name__}")
        
        if self.success_message:
            success_msg = self.success_message.format(value=value)
            print(format_success_message(success_msg, value))
    
    def _log_error(self, error: ValidationError):
        """
        Логировать ошибку валидации
        
        Args:
            error: Ошибка валидации
        """
        if self._config.log_attempts:
            print(f"❌ Ошибка валидации: {self.__class__.__name__} - {error}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получить статистику работы валидатора
        
        Returns:
            Словарь со статистикой
        """
        success_rate = (self.success_count / self.validation_count * 100) if self.validation_count > 0 else 0
        
        return {
            'validator_type': self.__class__.__name__,
            'total_validations': self.validation_count,
            'successful_validations': self.success_count,
            'failed_validations': self.error_count,
            'success_rate': round(success_rate, 2),
            'configuration': self.config_params.copy()
        }
    
    def reset_statistics(self):
        """Сбросить статистику валидации"""
        self.validation_count = 0
        self.success_count = 0
        self.error_count = 0
    
    def clone(self, **new_params) -> 'BaseValidator':
        """
        Создать копию валидатора с новыми параметрами
        
        Args:
            **new_params: Новые параметры
            
        Returns:
            Новый экземпляр валидатора
        """
        # Объединяем старые и новые параметры
        all_params = self.config_params.copy()
        all_params.update(new_params)
        
        # Создаем новый экземпляр
        return self.__class__(**all_params)
    
    def __str__(self) -> str:
        """Строковое представление валидатора"""
        return f"{self.__class__.__name__}({self.config_params})"
    
    def __repr__(self) -> str:
        """Подробное представление валидатора"""
        return f"{self.__class__.__name__}({self.config_params})"

class CombinedValidator(BaseValidator):
    """
    Комбинированный валидатор для применения нескольких валидаторов
    """
    
    def __init__(self, *validators: BaseValidator, stop_on_first_error: bool = True):
        """
        Args:
            *validators: Валидаторы для применения
            stop_on_first_error: Остановиться при первой ошибке
        """
        super().__init__()
        self.validators = validators
        self.stop_on_first_error = stop_on_first_error
    
    def _validate_value(self, value: Any) -> Any:
        """Применить все валидаторы по очереди"""
        current_value = value
        errors = []
        
        for validator in self.validators:
            try:
                current_value = validator.validate(current_value)
            except ValidationError as e:
                errors.append(e)
                if self.stop_on_first_error:
                    raise e
        
        if errors and not self.stop_on_first_error:
            # Создаем общую ошибку
            messages = [error.message for error in errors]
            combined_message = "; ".join(messages)
            raise self._create_error(combined_message)
        
        return current_value

class ConditionalValidator(BaseValidator):
    """
    Условный валидатор - применяется только при выполнении условия
    """
    
    def __init__(self, 
                 condition: Callable[[Any], bool],
                 validator: BaseValidator,
                 else_validator: Optional[BaseValidator] = None):
        """
        Args:
            condition: Функция условия
            validator: Валидатор для случая True
            else_validator: Валидатор для случая False
        """
        super().__init__()
        self.condition = condition
        self.validator = validator
        self.else_validator = else_validator
    
    def _validate_value(self, value: Any) -> Any:
        """Применить валидатор в зависимости от условия"""
        try:
            if self.condition(value):
                return self.validator.validate(value)
            elif self.else_validator:
                return self.else_validator.validate(value)
            else:
                return value
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise self._create_error(f"Ошибка условной валидации: {e}")

class ChainValidator(BaseValidator):
    """
    Цепочка валидаторов - применяется последовательно
    """
    
    def __init__(self, *validators: BaseValidator):
        """
        Args:
            *validators: Валидаторы для последовательного применения
        """
        super().__init__()
        self.validators = validators
    
    def _validate_value(self, value: Any) -> Any:
        """Применить валидаторы последовательно"""
        current_value = value
        
        for validator in self.validators:
            current_value = validator.validate(current_value)
        
        return current_value

# === УТИЛИТЫ ДЛЯ СОЗДАНИЯ ВАЛИДАТОРОВ ===

def combine_validators(*validators: BaseValidator, 
                      stop_on_first_error: bool = True) -> CombinedValidator:
    """
    Объединить несколько валидаторов
    
    Args:
        *validators: Валидаторы для объединения
        stop_on_first_error: Остановиться при первой ошибке
        
    Returns:
        CombinedValidator
    """
    return CombinedValidator(*validators, stop_on_first_error=stop_on_first_error)

def chain_validators(*validators: BaseValidator) -> ChainValidator:
    """
    Создать цепочку валидаторов
    
    Args:
        *validators: Валидаторы для цепочки
        
    Returns:
        ChainValidator
    """
    return ChainValidator(*validators)

def conditional_validator(condition: Callable[[Any], bool],
                         true_validator: BaseValidator,
                         false_validator: Optional[BaseValidator] = None) -> ConditionalValidator:
    """
    Создать условный валидатор
    
    Args:
        condition: Условие
        true_validator: Валидатор для True
        false_validator: Валидатор для False
        
    Returns:
        ConditionalValidator
    """
    return ConditionalValidator(condition, true_validator, false_validator)

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

class ExampleValidator(BaseValidator):
    """Пример простого валидатора"""
    
    def __init__(self, min_length: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
    
    def _validate_value(self, value: Any) -> str:
        """Проверить что значение - строка минимальной длины"""
        if not isinstance(value, str):
            value = str(value)
        
        if len(value) < self.min_length:
            raise self._create_error(
                f"Строка слишком короткая (минимум {self.min_length} символов)",
                suggestions=[f"Добавьте еще {self.min_length - len(value)} символов"]
            )
        
        return value

def demo_validators():
    """Демонстрация работы валидаторов"""
    
    print("🛡️ PyDefender Base Validator Demo")
    print("=" * 40)
    
    # Простой валидатор
    validator = ExampleValidator(min_length=3)
    
    try:
        result = validator.validate("Hello")
        print(f"✅ Результат: {result}")
    except ValidationError as e:
        print(format_error_message(e))
    
    # Статистика
    print(f"\n📊 Статистика: {validator.get_statistics()}")
    
    # Комбинированный валидатор
    validator1 = ExampleValidator(min_length=2)
    validator2 = ExampleValidator(min_length=5)
    
    combined = combine_validators(validator1, validator2)
    
    try:
        result = combined.validate("Hi")
        print(f"✅ Комбинированный результат: {result}")
    except ValidationError as e:
        print(format_error_message(e))

if __name__ == "__main__":
    demo_validators()