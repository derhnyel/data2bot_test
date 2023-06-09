from typing import Any, Dict, Callable, List, Type, Iterable, NamedTuple # AsyncGenerator
import json_stream
from json_stream import base as json_stream_base
import inspect
import inflect
import json
from config import ext, SchemaDataType
from utils import get_logger

LOGGER = get_logger()


class JsonSchemaHandler:
    """
    JsonSchemaHandler class to handle the json schema
    `read` the json file
    `parse` the json file
    `write` the schema to stdout/stderr/file
    `to_schema` to convert the json object to schema
    """

    SCHEMA_ATTRIBUTE = NamedTuple(
        "SchemaAttribute",
        [("tag", str), ("type", str), ("description", str), ("required", bool)],
    )  # NamedTuple to represent a schema attribute
    SCHEMA_DATA_TYPE = SchemaDataType()
    NUM2WORD = inflect.engine().number_to_words  #  engine to convert numbers to words

    def __init__(self) -> None:
        self.SCHEMA_MAP: Dict[str, Dict[str, str]] = {}  # Map of the schema
        self.POS: int = 0  # Position of the key in the json object

    async def write(self, target: Any,data:Dict=None) -> None:
        """
        Write the given target to stdout/stderr/file
        Args:
            target (Any): The target to write
        Returns:
            None
        """
        data = data or self.SCHEMA_MAP  # get a streamable generator from the schema map
        if str(target).endswith(ext):
            with open(
                target, mode="w"
            ) as f:  # async with aiofiles.open(source, mode='w') as f:
                LOGGER.info(f"Writing to {target} ...")
                json.dump(data, f, indent=2)  #  write dict generator to target
        elif hasattr(target, "write"):
            json.dump(data, target)

    async def parse(
        self,
        parent_key: str,
        parent_value: Any,
        map_function: Callable,
        root: str,
        skip: bool = False,
        depth: int = -1,
    ) -> None : # AsyncGenerator: 
        """
        Parse the given json object and call the given map function on each key value pair.
        Using a Depth First Approach (Recursive Loop) it traverses the json object and calls the map function on each key value pair.

        Args:
            parent_key (str): The key of the parent object
            parent_value (Any): The value of the parent object
            map_function (Callable): The function to call on each key value pair
            root (str): The root of the json object
            skip (bool, optional): Whether to skip the map function on the parent object. Defaults to False.
            depth (int, optional): The depth to which all nodes will be tranversed (Number of times recursive loop is called). Defaults to -1.
        Raises:
            TypeError: If the map_function is not callable
        Returns:
            None
        """
        if not callable(map_function):
            raise TypeError("map_function must be callable")
        parent_type: Type = type(parent_value)  # Get the type of the parent value
        parent_repr: str = SchemaDataType().get_type_repr(
            type(parent_value)
        )  # Get the string representation of the parent type
        if depth == 0:
            return  # base case to break out of the recursive loop
        elif not skip:
            function_output: Any = map_function(
                **{
                    "repr_": parent_repr,
                    "value": parent_value,
                    "type": parent_type,
                    "key": parent_key,
                    "root": root,
                }
            )
            if inspect.iscoroutinefunction(
                map_function
            ):  # Check if the map_function is a coroutine function
                function_output = await function_output
            
            # yield function_output

        value: Iterable = (
            parent_value.items()
            if (
                isinstance(parent_value, Dict)
                or isinstance(
                    parent_value, json_stream_base.TransientStreamingJSONObject
                )
            )
            else enumerate(parent_value)
            if (
                isinstance(parent_value, List)
                or isinstance(parent_value, json_stream_base.TransientStreamingJSONList)
            )
            else []
        )

        for child_key, child_value in value:
            # Tranverse the children of a parent (if any) and call the parse function recursively on each child
            LOGGER.debug(
                f"CHILD {child_key},{child_value} OF PARENT {parent_key},{parent_value}"
            )
            if str(depth).isalnum() and int(depth) > 0:  # Check if depth is a number
                await self.parse(
                    str(child_key),
                    child_value,
                    map_function,
                    root=parent_key,
                    depth=depth - 1,
                    skip=False,
                )
            else:
                await self.parse(
                    str(child_key),
                    child_value,
                    map_function,
                    root=parent_key,
                    skip=False,
                )

    async def to_schema(self, **kwargs) -> None:
        """
        Convert the given attribute to a schema object and update the schema map
        Args:
            kwargs (Dict[str,Any]): The attribute to convert to a schema object
        Returns:
            None
        """
        self.schema = self.SCHEMA_ATTRIBUTE(
            tag=kwargs.get("key"),
            type=kwargs.get("repr_"),
            description="",
            required=False,
        )
        self.POS += 1  # Handle duplicate keys by using a position number
        pos_word: str = self.NUM2WORD(self.POS)
        self.SCHEMA_MAP[f"key_{pos_word}"] = self.schema._asdict()
        return (f"key_{pos_word}",self.schema._asdict())

    async def read(
        self,
        source: Any,
    ) -> json_stream_base.TransientStreamingJSONObject:
        """
        Load a json file from the given path and return the data
        Args:
            source (str): the source object to load the json file from
        Returns:
            json_stream_base.TransientStreamingJSONObject | json_stream_base.TransientStreamingJSONList: The stream json object
        """
        if str(source).endswith(ext):
            with open(source) as f:  # async with aiofiles.open(source, mode='r') as f:
                LOGGER.info(f"Reading from {source} ...")
                self.data = json_stream.load(f)  # Source is a TextIOWrapper object
        else:
            self.data = json_stream.load(
                source
            )  # Load the json file as a json_stream object to support streaming and optimize memory usage for hanlding large files
