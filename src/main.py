from schema import make_schema,make_multiple_schemas
import asyncio
from args import parse_arguments
from utils import get_logger,logging
from pathlib import Path
from config import ext
LOGGER = get_logger()
if __name__ == "__main__":
    args = parse_arguments()

    if args.verbose:
        LOGGER.level = logging.DEBUG
    else:
        LOGGER.level = logging.INFO    
    LOGGER.debug("source: ", args.source)
    LOGGER.debug("target: ", args.target)
    LOGGER.debug("depth: ", args.depth)
    LOGGER.debug("select_attr: ", args.select)
    source = Path(args.source).resolve()
    if source.suffix == ext:
        asyncio.run(
            make_schema(
                source=args.source,
                target=args.target,
                depth=args.depth,
                select_attr=args.select,
            )
        )
    elif source.is_dir() or source.suffix == "":
        asyncio.run(
            make_multiple_schemas(
                source=args.source,
                target=args.target,
                depth=args.depth,
                select_attr=args.select,
            )
        )

