import os
import pytest
from serialization_plugin import JsonSerializer
from serialization_plugin.exceptions import SerializationError, DeserializationError


@pytest.fixture
def json_serializer():
    return JsonSerializer()


@pytest.fixture
def test_data():
    return {
        "name": "Test",
        "value": 42,
        "is_valid": True,
        "nested": {
            "items": [1, 2, 3]
        }
    }


@pytest.fixture
def test_file(tmp_path):
    return os.path.join(tmp_path, "test.json")


def test_json_serialize_deserialize(json_serializer, test_data, test_file):
    # Test serialization and deserialization
    json_serializer.serialize(test_data, test_file)
    loaded_data = json_serializer.deserialize(test_file)

    assert loaded_data == test_data
    assert os.path.exists(test_file)


def test_json_serialize_invalid_data(json_serializer, test_file):
    # Test serialization of unserializable data
    class Unserializable:
        pass

    with pytest.raises(SerializationError):
        json_serializer.serialize(Unserializable(), test_file)


def test_json_deserialize_nonexistent_file(json_serializer):
    # Test deserialization from nonexistent file
    with pytest.raises(DeserializationError):
        json_serializer.deserialize("nonexistent.json")


def test_json_serialize_invalid_path(json_serializer, test_data):
    # Test serialization to invalid path
    with pytest.raises(SerializationError):
        json_serializer.serialize(test_data, "/invalid/path/test.json")


def test_json_deserialize_invalid_content(json_serializer, test_file):
    # Test deserialization of invalid JSON
    with open(test_file, 'w') as f:
        f.write("invalid json")

    with pytest.raises(DeserializationError):
        json_serializer.deserialize(test_file)