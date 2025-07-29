import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from .serializer import Serializer
from .exceptions import SerializationError, DeserializationError
import os


class XmlSerializer(Serializer):
    def serialize(self, data: dict, file_path: str) -> None:
        """Serialize data to XML and save to file"""
        self._validate_file_path(file_path)
        try:
            if not isinstance(data, dict):
                raise SerializationError("XML serializer supports only dictionary data")

            xml_data = dicttoxml(data, attr_type=False)
            dom = parseString(xml_data)
            pretty_xml = dom.toprettyxml()

            with open(file_path, 'w') as file:
                file.write(pretty_xml)
        except Exception as e:
            raise SerializationError(f"XML serialization error: {str(e)}")

    def deserialize(self, file_path: str) -> dict:
        """Load XML data from file and deserialize"""
        if not os.path.exists(file_path):
            raise DeserializationError(f"File not found: {file_path}")

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return self._xml_to_dict(root)
        except Exception as e:
            raise DeserializationError(f"XML deserialization error: {str(e)}")

    def _xml_to_dict(self, element: ET.Element) -> dict:
        """Convert XML element to dictionary"""
        result = {}
        for child in element:
            if len(child) > 0:
                result[child.tag] = self._xml_to_dict(child)
            else:
                result[child.tag] = child.text
        return result
