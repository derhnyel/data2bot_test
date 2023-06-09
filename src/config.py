from dataclasses import dataclass
from json_stream import base as json_stream_base
from typing import Dict, Type


# Path: config.py

ext = ".json"  # Set the extension based on the output format (json/yaml)


@dataclass
class SchemaDataType:
    json: str = "ARRAY"
    array: str = "ENUM"
    string: str = "STRING"
    integer: str = "INTEGER"
    boolean: str = "BOOLEAN"
    null: str = "NULL"

    def __post_init__(self):
        self.data_type_map: Dict[Type, str] = {
            str: self.string,
            dict: self.json,
            list: self.array,
            int: self.integer,
            float: self.integer,
            bool: self.boolean,
            type(None): self.null,
            json_stream_base.TransientStreamingJSONObject: self.json,
            json_stream_base.TransientStreamingJSONList: self.array,
        }

    def get_type_repr(self, type: Type) -> str:
        """
        Get the string representation of the given type
        Args:
            type (Type): The type to get the string representation of
        Returns:
            str: The string representation of the given type
        """
        return self.data_type_map[type]
