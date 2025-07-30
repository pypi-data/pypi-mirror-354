import pytest
import uuid
from chunk_metadata_adapter.utils import (
    ChunkId, EnumBase, is_empty_value, get_empty_value_for_type, get_valid_default_for_type, get_base_type, get_valid_default_for_field, dict_prop_to_flat_dict, flat_dict_to_dict_prop, flat_dict_to_dict_prop_recursive, semantic_to_flat_value, coerce_value_with_modifiers, autofill_enum_field, str_to_list, list_to_str
)
import enum

# --- EnumBase тестовый класс ---
class TestEnum(EnumBase):
    A = "a"
    B = "b"
    C = "c"

class TestEnumNone(EnumBase):
    @classmethod
    def default_value(cls):
        return None

# --- Тесты для ChunkId ---
def test_chunkid_valid_uuid():
    u = str(uuid.uuid4())
    cid = ChunkId.validate(u, None)
    assert isinstance(cid, str)
    assert uuid.UUID(cid, version=4)

def test_chunkid_default_value():
    assert ChunkId.default_value() == ChunkId.DEFAULT_VALUE
    assert uuid.UUID(ChunkId.default_value(), version=4)

def test_chunkid_zero_uuid():
    zero = "00000000-0000-0000-0000-000000000000"
    cid = ChunkId.validate(zero, None)
    assert cid == ChunkId.DEFAULT_VALUE
    assert is_empty_value(cid)

def test_chunkid_default_uuid():
    cid = ChunkId.validate(ChunkId.DEFAULT_VALUE, None)
    assert cid == ChunkId.DEFAULT_VALUE
    assert is_empty_value(cid)

def test_chunkid_is_default():
    cid = ChunkId(ChunkId.DEFAULT_VALUE)
    assert cid.is_default()
    cid2 = ChunkId(str(uuid.uuid4()))
    assert not cid2.is_default()

def test_chunkid_invalid_uuid():
    with pytest.raises(ValueError):
        ChunkId.validate("not-a-uuid", None)
    with pytest.raises(ValueError):
        # Не v4: третий блок не начинается с '4'
        ChunkId.validate("12345678-1234-1234-1234-1234567890ab", None)

def test_chunkid_none():
    assert ChunkId.validate(None, None) is None

def test_chunkid_uuid_instance():
    u = uuid.uuid4()
    cid = ChunkId.validate(u, None)
    assert isinstance(cid, str)
    assert uuid.UUID(cid, version=4)

# --- Тесты для is_empty_value ---
def test_is_empty_value_various():
    assert is_empty_value(None)
    assert is_empty_value("")
    assert is_empty_value([])
    assert is_empty_value({})
    assert is_empty_value(())
    assert is_empty_value("None")
    assert is_empty_value(ChunkId.DEFAULT_VALUE)
    assert not is_empty_value("some-value")
    assert not is_empty_value(str(uuid.uuid4()))

# --- Тесты для EnumBase ---
def test_enum_base_default_value():
    assert TestEnum.default_value() == TestEnum.A
    assert TestEnumNone.default_value() is None

def test_enum_base_members():
    vals = list(TestEnum)
    assert TestEnum.A in vals
    assert TestEnum.B in vals
    assert TestEnum.C in vals

# --- Тесты для get_empty_value_for_type ---
def test_get_empty_value_for_type():
    assert get_empty_value_for_type(int) == 0
    assert get_empty_value_for_type(float) == 0
    assert get_empty_value_for_type(str) == ""
    assert get_empty_value_for_type(bool) is False
    assert get_empty_value_for_type(list) == []
    assert get_empty_value_for_type(dict) == {}
    assert get_empty_value_for_type(tuple) == ()
    assert get_empty_value_for_type(TestEnum) == TestEnum.A
    assert get_empty_value_for_type(type(None)) is None

# --- Тесты для get_valid_default_for_type ---
def test_get_valid_default_for_type():
    assert get_valid_default_for_type(int) == 0
    assert get_valid_default_for_type(float) == 0
    assert get_valid_default_for_type(str) == ""
    assert get_valid_default_for_type(bool) is False
    assert get_valid_default_for_type(list) == []
    assert get_valid_default_for_type(dict) == {}
    assert get_valid_default_for_type(tuple) == ()
    assert get_valid_default_for_type(TestEnum) == TestEnum.A
    assert get_valid_default_for_type(uuid.UUID, uuid_zero=True) == ChunkId.empty_uuid4()

# --- Тесты для автозаполнения Enum ---
def test_enum_autofill_optional():
    # Симуляция автозаполнения для Optional[Enum]
    val = TestEnum.default_value()
    assert val == TestEnum.A
    val_none = TestEnumNone.default_value()
    assert val_none is None

# --- Тесты для автозаполнения ChunkId ---
def test_chunkid_autofill_optional():
    # Симуляция автозаполнения для Optional[ChunkId]
    val = ChunkId.default_value()
    assert val == ChunkId.DEFAULT_VALUE
    assert is_empty_value(val)

# --- Тесты для преобразования и сравнения ---
def test_chunkid_equality():
    val = ChunkId.default_value()
    assert val == ChunkId.DEFAULT_VALUE
    assert str(val) == ChunkId.DEFAULT_VALUE
    assert not (val == str(uuid.uuid4()))

# --- Граничные случаи ---
def test_chunkid_all_zeros_variants():
    from chunk_metadata_adapter.utils import ChunkId
    # UUID с разным количеством нулей и разделителей
    for v in [
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-4000-8000-000000000000",
    ]:
        cid = ChunkId.validate(v, None)
        # Проверяем только валидность UUID
        assert isinstance(cid, str) and len(cid) == 36

# --- Проверка, что ChunkId всегда валидирует дефолтное значение ---
def test_chunkid_default_value_always_valid():
    cid = ChunkId.validate(ChunkId.default_value(), None)
    assert cid == ChunkId.DEFAULT_VALUE
    assert is_empty_value(cid)

def test_get_base_type():
    from typing import Optional, Union, List
    assert get_base_type(int) is int
    assert get_base_type(Optional[int]) is int
    assert get_base_type(Union[int, None]) is int
    assert get_base_type(Union[str, int]) is str  # берёт первый
    assert get_base_type(List[int]) == List[int]

class DummyField:
    def __init__(self, name, annotation, min_length=None, pattern=None):
        self.name = name
        self.annotation = annotation
        self.min_length = min_length
        self.pattern = pattern

def test_get_valid_default_for_field_uuid():
    field = DummyField('uuid', str)
    val = get_valid_default_for_field(field)
    assert isinstance(val, str)
    assert len(val) == 36
    import uuid as uuidlib
    uuidlib.UUID(val)

def test_get_valid_default_for_field_str_min_length():
    field = DummyField('name', str, min_length=5)
    val = get_valid_default_for_field(field)
    assert val == 'xxxxx'

def test_get_valid_default_for_field_str():
    field = DummyField('name', str)
    val = get_valid_default_for_field(field)
    assert val == ''

def test_get_valid_default_for_field_list_min_length():
    field = DummyField('tags', list, min_length=3)
    val = get_valid_default_for_field(field)
    assert val == [None, None, None]

def test_get_valid_default_for_field_list():
    field = DummyField('tags', list)
    val = get_valid_default_for_field(field)
    assert val == []

def test_get_valid_default_for_field_other_types():
    field = DummyField('count', int)
    assert get_valid_default_for_field(field) == 0
    field = DummyField('flag', bool)
    assert get_valid_default_for_field(field) is False
    field = DummyField('data', dict)
    assert get_valid_default_for_field(field) == {}
    field = DummyField('tup', tuple)
    assert get_valid_default_for_field(field) == () 

def test_dict_prop_to_flat_dict_and_back_edge():
    nested = {"a": {"b": "1", "c": ["x", "y"]}, "z": "2"}
    flat = dict_prop_to_flat_dict(nested)
    assert flat["a.b"] == "1"
    assert flat["a.c"] == "x,y"
    assert flat["z"] == "2"
    restored = flat_dict_to_dict_prop_recursive(flat)
    assert restored["a"]["b"] == "1"
    assert restored["a"]["c"] == "x,y"
    assert restored["z"] == "2"
    # flat_dict_to_dict_prop (нерекурсивная)
    flat_simple = {"a.b": "1", "a.c": "2"}
    restored_simple = flat_dict_to_dict_prop(flat_simple)
    assert restored_simple == {"a": {"b": "1", "c": "2"}}
    # Ошибка на не-словаре
    with pytest.raises(ValueError):
        dict_prop_to_flat_dict([1,2,3])
    with pytest.raises(ValueError):
        flat_dict_to_dict_prop([1,2,3])

def test_semantic_to_flat_value_and_coerce():
    class DummyField:
        def __init__(self, annotation, min_length=None, max_length=None, ge=None, le=None, decimal_places=None):
            self.annotation = annotation
            self.min_length = min_length
            self.max_length = max_length
            self.ge = ge
            self.le = le
            self.decimal_places = decimal_places
    # str
    f = DummyField(str, min_length=3, max_length=5)
    assert semantic_to_flat_value("a", f, "f") == "axx"
    assert semantic_to_flat_value("abcdef", f, "f") == "abcde"
    # int
    f = DummyField(int, ge=10, le=20)
    assert semantic_to_flat_value(5, f, "f") == 10
    assert semantic_to_flat_value(25, f, "f") == 20
    # float
    f = DummyField(float, ge=0.5, le=2.5, decimal_places=1)
    assert semantic_to_flat_value(0.1, f, "f") == 0.5
    assert semantic_to_flat_value(3.0, f, "f") == 2.5
    assert semantic_to_flat_value(1.234, f, "f") == 1.2
    # bool
    f = DummyField(bool)
    assert semantic_to_flat_value(None, f, "f") is False
    assert semantic_to_flat_value(True, f, "f") is True
    # list
    f = DummyField(list, min_length=2, max_length=3)
    assert semantic_to_flat_value(["a"], f, "f") == "a,None"
    assert semantic_to_flat_value(["a","b","c","d"], f, "f") == "a,b,c"
    # dict
    f = DummyField(dict)
    assert semantic_to_flat_value({"x":1,"y":2}, f, "meta") == "meta.x=1,meta.y=2"
    # coerce_value_with_modifiers
    f = DummyField(str, min_length=3, max_length=5)
    assert coerce_value_with_modifiers("a", f) == "axx"
    f = DummyField(int, ge=10, le=20)
    assert coerce_value_with_modifiers(5, f) == 10
    f = DummyField(float, ge=0.5, le=2.5, decimal_places=1)
    assert coerce_value_with_modifiers(0.1, f) == 0.5
    f = DummyField(bool)
    assert coerce_value_with_modifiers("yes", f) is True
    f = DummyField(list, min_length=2)
    assert coerce_value_with_modifiers(["a"], f) == ["a", None]
    # ChunkId
    from chunk_metadata_adapter.utils import ChunkId
    f = DummyField(ChunkId)
    assert coerce_value_with_modifiers(None, f) is None

def test_autofill_enum_field():
    class DummyEnum(EnumBase):
        A = "a"
        B = "b"
        @classmethod
        def default_value(cls):
            return cls.A
    assert autofill_enum_field(None, DummyEnum) is None
    assert autofill_enum_field("a", DummyEnum) == "a"
    assert autofill_enum_field("bad", DummyEnum) == "a"
    assert autofill_enum_field(DummyEnum.B, DummyEnum) == "b"

def test_str_to_list_and_list_to_str():
    assert str_to_list("a,b,c") == ["a","b","c"]
    assert str_to_list("") == []
    assert str_to_list(None) == []
    with pytest.raises(ValueError):
        str_to_list(["a","b"])
    assert list_to_str(["a","b"]) == "a,b"
    assert list_to_str([]) == ""
    with pytest.raises(ValueError):
        str_to_list(123)
    with pytest.raises(ValueError):
        list_to_str("abc") 