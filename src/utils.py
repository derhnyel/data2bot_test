import logging

__LOGGER = logging.getLogger()
__LOGGER.level = logging.DEBUG
def get_logger(level:int=None) -> logging.Logger:
    """
    Get the logger for the module
    Returns:
        logging.Logger: The logger for the module
    """
    if level:
        __LOGGER.level = level
    return __LOGGER




# from collections import deque
# import inspect


# class Streamable:
#     def __init__(self, iterable):
#         super().__init__()
#         if not inspect.isasyncgen(iterable):
#             self._it = iter(iterable)
#         else:
#             self._it = iterable
#         self._cache = deque()

#     async def __aiter__(self):
#         return self

#     async def __anext__(self):
#         if self._cache:
#             return self._cache.popleft()
#         return await anext(self._it)
    
#     async def _peek(self):
#         try:
#             peek = await anext(self._it)
#         except StopIteration:
#             pass
#         else:
#             self._cache.append(peek)

#     def __bool__(self):

#         loop = asyncio.get_running_loop()
#         task = loop.create_task(self._peek())
#         return bool(self._cache)

#     def __repr__(self):  # pragma: no cover
#         return f'<{type(self).__name__} for {self._it}>'

# class StreamableDict(Streamable, dict):
#     """
#         Class specifically designed to pass isinstance(o, dict)
#         and conform to the implementation of json.dump(o)
#         for lists, except items are provided by passed in
#         generator. Generator must produce pairs of key/value
#     """
#     def items(self):
#         return self


