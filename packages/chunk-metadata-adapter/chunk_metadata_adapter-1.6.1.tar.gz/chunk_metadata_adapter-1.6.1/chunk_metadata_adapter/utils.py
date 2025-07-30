from typing import Union
import pydantic
import uuid
import enum
import re
from typing import List
import json

def get_empty_value_for_type(base_type):
    if isinstance(base_type, type) and issubclass(base_type, enum.Enum):
        # Вернуть первый элемент Enum
        return list(base_type)[0]
    if base_type in (int, float):
        return 0
    elif base_type is str:
        return ""
    elif base_type is bool:
        return False
    elif base_type is list:
        return []
    elif base_type is dict:
        return {}
    elif base_type is tuple:
        return ()
    else:
        return None

def is_empty_value(value):
    return value in (None, "", [], {}, (), "None", ChunkId.empty_uuid4())

def get_base_type(ann):
    origin = getattr(ann, '__origin__', None)
    args = getattr(ann, '__args__', ())
    if origin is Union and args:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return non_none[0]
    return ann 

def get_valid_default_for_field(field):
    ann = field.annotation
    base_type = get_base_type(ann)
    # UUID
    if field.name.endswith('uuid') or field.name == 'uuid' or (hasattr(field, 'pattern') and field.pattern and 'uuid' in field.pattern.pattern.lower()):
        return str(uuid.uuid4())
    # min_length для строк
    if base_type is str:
        min_length = getattr(field, 'min_length', None)
        if min_length and min_length > 0:
            return 'x' * min_length
        return ""
    # min_length для списков
    if base_type is list:
        min_length = getattr(field, 'min_length', None)
        if min_length and min_length > 0:
            return [None] * min_length
        return []
    # dict, tuple, bool, int, float
    return get_empty_value_for_type(base_type)

def get_valid_default_for_type(base_type, uuid_zero=False):
    if isinstance(base_type, type) and issubclass(base_type, enum.Enum):
        return list(base_type)[0]
    # UUID (pydantic, stdlib)
    if base_type is uuid.UUID or (uuid_zero and (base_type is str or base_type is uuid.UUID)):
        return ChunkId.empty_uuid4()
    # min_length для строк
    if base_type is str:
        return ""
    # list, dict, tuple, bool, int, float
    return get_empty_value_for_type(base_type)

class EnumBase(enum.Enum):
    @classmethod
    def default_value(cls):
        vals = list(cls)
        return vals[0] if vals else None

class ChunkId(str):
    @staticmethod
    def empty_uuid4():
        # Валидный UUIDv4: de93be12-3af5-4e6d-9ad2-c2a843c0bfb5
        return "de93be12-3af5-4e6d-9ad2-c2a843c0bfb5"

    DEFAULT_VALUE = empty_uuid4.__func__()
    UUID4_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.IGNORECASE)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if v is None:
            return None
        if isinstance(v, uuid.UUID):
            if v.version != 4:
                raise ValueError("Invalid UUIDv4 format: not version 4")
            return str(v)
        if isinstance(v, str):
            # Проверка: если строка состоит только из нулей и разделителей, считать валидным UUIDv4
            if v.replace('-', '') == '0' * 32 or v == cls.empty_uuid4():
                return cls.empty_uuid4()
            if not cls.UUID4_PATTERN.match(v):
                raise ValueError("Invalid UUIDv4 format: regex check failed")
            try:
                uuid_obj = uuid.UUID(v)
                if uuid_obj.version != 4:
                    raise ValueError("Invalid UUIDv4 format: not version 4")
                return str(uuid_obj)
            except Exception:
                raise ValueError("Invalid UUIDv4 format")
        raise TypeError("ChunkId must be a UUIDv4 string or None")

    @staticmethod
    def default_value():
        return ChunkId.empty_uuid4()

    def is_default(self):
        return str(self) == ChunkId.empty_uuid4()

def coerce_value_with_modifiers(value, field):
    """
    Приводит значение к типу с учётом модификаторов поля (min_length, max_length, ge, le, decimal_places).
    Используется для строгого преобразования flat <-> semantic.
    """
    base_type = get_base_type(field.annotation)
    # Строки
    if base_type is str:
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        min_length = getattr(field, 'min_length', None)
        max_length = getattr(field, 'max_length', None)
        if min_length is not None and len(value) < min_length:
            value = value.ljust(min_length, 'x')
        if max_length is not None and len(value) > max_length:
            value = value[:max_length]
        return value
    # Числа
    if base_type in (int, float):
        if value is None or value == '':
            return None
        try:
            value = base_type(value)
        except Exception:
            return None
        ge = getattr(field, 'ge', None)
        le = getattr(field, 'le', None)
        if ge is not None and value < ge:
            value = ge
        if le is not None and value > le:
            value = le
        # decimal_places (если появится)
        decimal_places = getattr(field, 'decimal_places', None)
        if decimal_places is not None and base_type is float:
            value = round(value, decimal_places)
        return value
    # Bool
    if base_type is bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "y")
        return bool(value)
    # Списки
    if base_type is list:
        if value is None:
            return []
        if isinstance(value, str):
            value = [v for v in value.split(",") if v]
        if not isinstance(value, list):
            value = list(value)
        min_length = getattr(field, 'min_length', None)
        max_length = getattr(field, 'max_length', None)
        if min_length is not None and len(value) < min_length:
            value += [None] * (min_length - len(value))
        if max_length is not None and len(value) > max_length:
            value = value[:max_length]
        return value
    # UUID/ChunkId
    if base_type.__name__ == 'ChunkId':
        if value is None or value == '' or value == ChunkId.empty_uuid4():
            return None
        return str(value)
    # Остальные типы (dict, tuple, enum, etc)
    return value 

def semantic_to_flat_value(value, field, field_name):
    """
    Преобразует значение из semantic-слоя в flat-слой:
    - строки — строки (min_length/max_length)
    - числа — числа (decimal_places, ge/le)
    - bool — bool
    - массив — строка с запятыми (экранировать кавычки, min_length/max_length)
    - словарь — ИмяПоля.Ключ
    - объект — копируется как есть
    """
    base_type = get_base_type(field.annotation)
    # Строки
    if base_type is str:
        if value is None:
            value = ""
        min_length = getattr(field, 'min_length', None)
        max_length = getattr(field, 'max_length', None)
        if min_length is not None and len(value) < min_length:
            value = value.ljust(min_length, 'x')
        if max_length is not None and len(value) > max_length:
            value = value[:max_length]
        return value
    # Числа
    if base_type is int:
        if value is None:
            return 0
        ge = getattr(field, 'ge', None)
        le = getattr(field, 'le', None)
        if ge is not None and value < ge:
            value = ge
        if le is not None and value > le:
            value = le
        return value
    if base_type is float:
        if value is None:
            return 0.0
        ge = getattr(field, 'ge', None)
        le = getattr(field, 'le', None)
        decimal_places = getattr(field, 'decimal_places', None)
        if ge is not None and value < ge:
            value = ge
        if le is not None and value > le:
            value = le
        if decimal_places is not None:
            value = round(value, decimal_places)
        return value
    # Bool
    if base_type is bool:
        if value is None:
            return False
        return value
    # Массив (list)
    if base_type is list:
        if value is None:
            value = []
        min_length = getattr(field, 'min_length', None)
        max_length = getattr(field, 'max_length', None)
        if min_length is not None and len(value) < min_length:
            value = value + [None] * (min_length - len(value))
        if max_length is not None and len(value) > max_length:
            value = value[:max_length]
        # Экранируем кавычки внутри элементов
        def escape_elem(elem):
            if not isinstance(elem, str):
                elem = str(elem)
            return elem.replace('"', '\"').replace("'", "\'")
        return ",".join(escape_elem(e) for e in value)
    # Словарь (dict)
    if base_type is dict:
        if value is None:
            return ""
        return ",".join(f"{field_name}.{k}={v}" for k, v in value.items())
    # Остальные типы
    return value 

def autofill_enum_field(value, enum_cls, allow_none=True):
    """
    Автозаполнение и валидация для Enum-полей.
    - Если value None или пустая строка и allow_none — вернуть None.
    - Если value валидный член Enum — вернуть value (или value.value).
    - Если невалидный — вернуть default_value().value Enum.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return None if allow_none else enum_cls.default_value().value
    if isinstance(value, enum_cls):
        return value.value
    if isinstance(value, str):
        for member in enum_cls:
            if value == member.value:
                return value
    # Не валидное значение — вернуть дефолт
    return enum_cls.default_value().value 

def str_to_list(value, separator=',', allow_none=True)->List[str]:
    """
    Transform string to list of strings.
    - If value is None or empty string — return empty list.
    - If value is list — return it.
    - If value is string — return list of strings, split by separator.
    - If value is not string — return list with value.
    """
    if not value is None and not isinstance(value, str) or (not allow_none and value is None):
        raise ValueError(f"value must be a string, got: {type(value)}")
    
    if value is None or value.strip() == '':
        return []
    
    if isinstance(value, list):
        return [v for v in value if not allow_none or (v is not None and v != '')]
    
    return [v for v in value.split(separator) if not allow_none or (v is not None and v != '')]

def list_to_str(value, separator=',', allow_none=True)->str:
    """
    Transform list of strings to string.
    - If value is None or empty list — return empty string.
    - If value is list — return string, joined by separator.
    - If value is not list — return string with value.
    """
    if not value is None and not isinstance(value, list) or (not allow_none and value is None):
        raise ValueError(f"value must be a list, got: {type(value)}")
    
    if value is None:
        return ""
    
    for v in value:
        if not isinstance(v, str):
            raise ValueError(f"value must be a list of strings, got: {type(v)}")
        
    return separator.join(value)

def to_flat_dict(data: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Recursively flattens a nested dictionary. Only lists/tuples and dicts are serialized via json; simple types (str, int, float, bool, None, Enum) are left as is (Enum -> .value).
    Example: {"a": {"b": {"c": ["c0", "c1"]}}} -> {"a.b.c": '["c0", "c1"]'}
    """
    items = {}
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        # Convert enums to their value
        if isinstance(v, enum.Enum):
            v = v.value
        # Convert objects to dict (if not a built-in type)
        elif hasattr(v, '__dict__') and not isinstance(v, (str, bytes, bytearray, dict, list, tuple)):
            obj_dict = vars(v)
            for obj_k, obj_v in obj_dict.items():
                obj_key = f"{new_key}{sep}{obj_k}"
                if isinstance(obj_v, (list, tuple)):
                    items[obj_key] = json.dumps(obj_v)
                elif isinstance(obj_v, dict):
                    items.update(to_flat_dict(obj_v, obj_key, sep=sep))
                elif isinstance(obj_v, enum.Enum):
                    items[obj_key] = obj_v.value
                else:
                    items[obj_key] = obj_v
            continue
        # Dict: recurse
        if isinstance(v, dict):
            items.update(to_flat_dict(v, new_key, sep=sep))
        # List/tuple: serialize via json
        elif isinstance(v, (list, tuple)):
            items[new_key] = json.dumps(v)
        # Simple types: leave as is
        else:
            items[new_key] = v
    return items

def from_flat_dict(flat: dict, sep: str = '.') -> dict:
    """
    Recursively unflattens a flat dict with dot-separated keys into a nested dict.
    Only values that look like JSON arrays/objects or JSON-strings (in quotes), or are valid JSON (e.g. numbers), are parsed via json.loads; others are left as is.
    Example: {"a.b.c": '["c0", "c1"]'} -> {"a": {"b": {"c": ["c0", "c1"]}}}
    """
    result = {}
    for flat_key, value in flat.items():
        keys = flat_key.split(sep)
        d = result
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        # Try to parse if value is str and looks like JSON array/object or JSON string, or is valid JSON (number, bool, null)
        if isinstance(value, str) and value:
            try:
                if value[0] in '[{' or (value[0] == '"' and value[-1] == '"'):
                    d[keys[-1]] = json.loads(value)
                else:
                    # Попробовать распарсить как число, bool, null
                    d[keys[-1]] = json.loads(value)
            except Exception:
                d[keys[-1]] = value
        else:
            d[keys[-1]] = value
    return result