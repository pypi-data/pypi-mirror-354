from abc import ABC, abstractmethod
from typing import Any
import os


class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: Any, file_path: str) -> None:
        """Serialize data and save to file"""
        pass

    @abstractmethod
    def deserialize(self, file_path: str) -> Any:
        """Load data from file and deserialize"""
        pass

    def _validate_file_path(self, file_path: str) -> None:
        """Validate that file path is valid and directory exists"""
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            raise FileNotFoundError(f"Directory does not exist: {dir_path}")