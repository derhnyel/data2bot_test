import os
from pathlib import Path
import asyncio
from handler import JsonSchemaHandler
from utils import get_logger
from config import ext

LOGGER = get_logger()


async def make_schema(
    source: str,
    target: str,
    select_attr: str = None,
    depth: int = -1,
    parent_key: str = "root",
    skip: bool = True,
) -> None:
    """
    Make a schema from the given json file and write it to the given target
    Args:
        source (Any): The source to load the json file from
        target (Any): The target to write the schema to
        select_attr (str, optional): The attribute to select from the json file. Defaults to None.
        depth (int, optional): The depth to which all nodes will be tranversed (Number of times recursive loop is called). Defaults to -1.
        parent_key (str, optional): The key of the parent object. Defaults to "root".
        skip (bool, optional): Whether to skip the map function on the parent object. Defaults to True.
    Returns:
        None
    Raises:
        FileNotFoundError: If the source is not a valid file
    """
    source, target = (Path(source).resolve(), Path(target).resolve())
    if not source.suffix == ext:
        raise FileNotFoundError(f"{source} is not a valid file")
    if not str(target).endswith(ext) and target.suffix == "":
        sourcename = os.path.basename(source).strip(ext)
        target = os.path.join(target, f"{sourcename}_schema{ext}")
    schema_handler = JsonSchemaHandler()
    await schema_handler.read(source)
    if select_attr:
        schema_handler.data = schema_handler.data[select_attr]
    await schema_handler.parse(
        parent_key=parent_key,
        parent_value=schema_handler.data,
        map_function=schema_handler.to_schema,
        root=parent_key,
        skip=skip,
        depth=depth,
    )
    await schema_handler.write(target)


async def make_multiple_schemas(
    source: str,
    target: str,
    select_attr: str = None,
    depth: int = -1,
    parent_key: str = "root",
    skip: bool = True,
) -> None:
    """
    Make a schemas for json files and in a directory and write it to the given target
    Args:
        source (Any): The source to load the json file from
        target (Any): The target to write the schema to
        select_attr (str, optional): The attribute to select from the json file. Defaults to None.
        depth (int, optional): The depth to which all nodes will be tranversed (Number of times recursive loop is called). Defaults to -1.
        parent_key (str, optional): The key of the parent object. Defaults to "root".
        skip (bool, optional): Whether to skip the map function on the parent object. Defaults to True.
    Returns:
        None
    Raises:
        NotADirectoryError: If the source or target is not a valid directory
    """
    source, target = (Path(source).resolve(), Path(target).resolve())
    if source.suffix == "":
        source.mkdir(parents=True, exist_ok=True)
    else:
        raise NotADirectoryError("source must be a directory")
    if target.suffix == "":
        target.mkdir(parents=True, exist_ok=True)
    else:
        raise NotADirectoryError("target must be a directory")

    # Get all json files in the directory
    pathlist = Path(source).glob(f"*{ext}")

    # A list to be populated with async tasks.
    tasks = []

    # Iterate through all json files in the directory.
    for path in pathlist:
        tasks.append(
            asyncio.ensure_future(
                make_schema(
                    source=path,
                    depth=depth,
                    select_attr=select_attr,
                    parent_key=parent_key,
                    target=target,
                    skip=skip,
                )
            )
        )
