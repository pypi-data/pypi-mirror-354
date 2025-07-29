import json
import os
from typing import Any
from .serializer import Serializer
from .exceptions import SerializationError, DeserializationError


class JsonSerializer(Serializer):
    def serialize(self, data: Any, file_path: str) -> None:
        """Serialize data to JSON and save to file"""
        self._validate_file_path(file_path)
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except (TypeError, OverflowError, ValueError) as e:
            raise SerializationError(f"JSON serialization error: {str(e)}")
        except IOError as e:
            raise SerializationError(f"File operation error: {str(e)}")

    def deserialize(self, file_path: str) -> Any:
        """Load JSON data from file and deserialize"""
        if not os.path.exists(file_path):
            raise DeserializationError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise DeserializationError(f"JSON decode error: {str(e)}")
        except IOError as e:
            raise DeserializationError(f"File operation error: {str(e)}")