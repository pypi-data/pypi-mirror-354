import typing

if typing.TYPE_CHECKING:
    from .transaction_context import SQLAlchemyTransactionContext


EXECUTION_MAP = {
    'execute': lambda result: result,

    'fetchone': lambda result: result.fetchone(),
    'first': lambda result: result.first(),
    'fetchall': lambda result: result.fetchall(),
    'one': lambda result: result.one(),
    'one_or_none': lambda result: result.one_or_none(),
    'all': lambda result: result.all(),

    'scalars': lambda result: result.scalars(),
    'scalars_all': lambda result: result.scalars().all(),
    'scalars_first': lambda result: result.scalars().first(),
    'scalars_one': lambda result: result.scalars().one(),
    'scalars_one_or_none': lambda result: result.scalars().one_or_none(),
    'scalars_fetchall': lambda result: result.scalars().fetchall(),
    'scalars_fetchmany': lambda result: result.scalars().fetchmany(),

    'mappings': lambda result: result.mappings(),
    'mappings_all': lambda result: result.mappings().all(),
    'mappings_first': lambda result: result.mappings().first(),
    'mappings_one': lambda result: result.mappings().one(),
    'mappings_one_or_none': lambda result: result.mappings().one_or_none(),
    'mappings_fetchall': lambda result: result.mappings().fetchall(),
    'mappings_fetchone': lambda result: result.mappings().fetchone(),

    'tuples': lambda result: result.tuples(),
    'tuples_all': lambda result: result.tuples().all(),
    'tuples_first': lambda result: result.tuples().first(),
    'tuples_one': lambda result: result.tuples().one(),
    'tuples_one_or_none': lambda result: result.tuples().one_or_none(),
    'tuples_fetchall': lambda result: result.tuples().fetchall(),
    'tuples_fetchone': lambda result: result.tuples().fetchone(),

    'rowcount': lambda result: result.rowcount,

    'scalar': lambda result: result.scalar(),

    # Deprecated
    'mapped_first': lambda result: result.mappings().first(),
    'mapped_one': lambda result: result.mappings().fetchone(),
    'mapped_all': lambda result: result.mappings().fetchall(),
}


def execute_query(
    context: "SQLAlchemyTransactionContext",
    query,
    method: str
) -> typing.Callable[[typing.Any], typing.Any]:
    if method not in EXECUTION_MAP:
        raise AttributeError(f'Unsupported execution method: {method}')

    extractor = EXECUTION_MAP[method]

    async def executor(*args, **kwargs):
        async with context.current_transaction_or_default() as tx:
            result = await tx.execute(query, *args, **kwargs)
            return extractor(result)

    return executor
