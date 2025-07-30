import typing

from sqlalchemy import ClauseElement

from .execute import execute_query, EXECUTION_MAP

if typing.TYPE_CHECKING:
    from .transaction_context import SQLAlchemyTransactionContext


T = typing.TypeVar('T', bound=ClauseElement)


EXECUTE_PROPERTIES = frozenset(EXECUTION_MAP.keys())

IGNORE_PROPERTIES = [
    'compile',
    'alias',
    'subquery',
    'label',
    'scalar_subquery',
]


class ProxyQuery(typing.Generic[T]):

    def __init__(self, query: T, context: 'SQLAlchemyTransactionContext') -> None:
        self._query = query
        self._context = context

    def unwrap(self):
        return self._query

    def __getattr__(self, item):
        if item in EXECUTE_PROPERTIES:
            return execute_query(self._context, self._query, item)

        value = getattr(self._query, item)

        if item in IGNORE_PROPERTIES:
            return value

        if not callable(value):
            return value

        def wrapper(*args, **kwargs):
            result = value(*args, **kwargs)
            if isinstance(result, ClauseElement):
                return ProxyQuery(result, self._context)
            return self

        return wrapper
