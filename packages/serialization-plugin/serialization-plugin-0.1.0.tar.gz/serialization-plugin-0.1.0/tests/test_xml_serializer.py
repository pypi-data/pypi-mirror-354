import os
import pytest
from serialization_plugin import XmlSerializer
from serialization_plugin.exceptions import SerializationError, DeserializationError


@pytest.fixture
def xml_serializer():
    return XmlSerializer()


@pytest.fixture
def test_data():
    return {
        "name": "Test",
        "value": "42",
        "is_valid": "True",
        "nested": {
            "item": ["1", "2", "3"]
        }
    }


@pytest.fixture
def test_file(tmp_path):
    return os.path.join(tmp_path, "test.xml")


def test_xml_serialize_deserialize(xml_serializer, test_data, test_file):
    # Test serialization and deserialization
    xml_serializer.serialize(test_data, test_file)
    loaded_data = xml_serializer.deserialize(test_file)

    # XML converts all values to strings, so we need to adjust comparison
    assert loaded_data == test_data
    assert os.path.exists(test_file)


def test_xml_serialize_non_dict_data(xml_serializer, test_file):
    # Test serialization of non-dictionary data
    with pytest.raises(SerializationError):
        xml_serializer.serialize([1, 2, 3], test_file)


def test_xml_deserialize_nonexistent_file(xml_serializer):
    # Test deserialization from nonexistent file
    with pytest.raises(DeserializationError):
        xml_serializer.deserialize("nonexistent.xml")


def test_xml_serialize_invalid_path(xml_serializer, test_data):
    # Test serialization to invalid path
    with pytest.raises(SerializationError):
        xml_serializer.serialize(test_data, "/invalid/path/test.xml")


def test_xml_deserialize_invalid_content(xml_serializer, test_file):
    # Test deserialization of invalid XML
    with open(test_file, 'w') as f:
        f.write("invalid xml")

    with pytest.raises(DeserializationError):
        xml_serializer.deserialize(test_file)


def test_xml_serialize_empty_dict(xml_serializer, test_file):
    # Test serialization of empty dictionary
    xml_serializer.serialize({}, test_file)
    loaded_data = xml_serializer.deserialize(test_file)
    assert loaded_data == {}