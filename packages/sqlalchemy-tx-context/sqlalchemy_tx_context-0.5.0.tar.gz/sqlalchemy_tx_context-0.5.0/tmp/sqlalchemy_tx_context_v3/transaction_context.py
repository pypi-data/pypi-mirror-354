import typing
import contextvars
from contextlib import asynccontextmanager

import sqlalchemy
from sqlalchemy import dialects
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSessionTransaction
from sqlalchemy.ext.asyncio import AsyncSession


from .proxy import ProxyQuery
from .test import Select


class PostgreSQL:
    def __init__(self, insert):
        self.insert = insert


class SQLAlchemyTransactionContext:
    def __init__(
        self,
        engine: AsyncEngine,
        *,
        default_session_maker: typing.Callable[
            [], typing.AsyncContextManager[AsyncSession]
        ] = None
    ):
        self.engine = engine
        if default_session_maker is None:
            self.default_session_maker = async_sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            ).begin
        else:
            self.default_session_maker = default_session_maker
        self._transaction_var = contextvars.ContextVar('transactions')

        self.select = self._proxy_sqlalchemy_query_factory(sqlalchemy.select)
        self.insert = self._proxy_sqlalchemy_query_factory(sqlalchemy.insert)
        self.update = self._proxy_sqlalchemy_query_factory(sqlalchemy.update)
        self.delete = self._proxy_sqlalchemy_query_factory(sqlalchemy.delete)
        self.union = self._proxy_sqlalchemy_query_factory(sqlalchemy.union)
        self.union_all = self._proxy_sqlalchemy_query_factory(sqlalchemy.union_all)
        self.exists = self._proxy_sqlalchemy_query_factory(sqlalchemy.exists)
        self.postgresql = PostgreSQL(
            self._proxy_sqlalchemy_query_factory(dialects.postgresql.insert)
        )

    def select(self, *args):
        return Select(*args)

    @asynccontextmanager
    async def transaction(
        self,
        session_maker=None
    ) -> typing.AsyncContextManager[typing.Union[AsyncSession, AsyncSessionTransaction]]:
        tx: typing.Optional[AsyncSession] = self._transaction_var.get(None)
        if tx is None:
            if session_maker is None:
                session_maker = self.default_session_maker
            async with session_maker() as tx:
                token = self._transaction_var.set(tx)
                try:
                    yield tx
                finally:
                    self._transaction_var.reset(token)
        else:
            async with tx.begin_nested() as nested_tx:
                yield nested_tx

    @asynccontextmanager
    async def current_transaction_or_default(self):
        tx: typing.Optional[AsyncSession] = self._transaction_var.get(None)
        if tx is not None:
            yield tx
            return
        async with self.transaction() as tx:
            yield tx

    def get_current_transaction(self) -> typing.Optional[AsyncSession]:
        return self._transaction_var.get(None)

    @asynccontextmanager
    async def new_transaction(
        self,
        session_maker=None
    ):
        if session_maker is None:
            session_maker = self.default_session_maker
        async with session_maker() as tx:
            token = self._transaction_var.set(tx)
            try:
                yield tx
            finally:
                self._transaction_var.reset(token)

    def _proxy_sqlalchemy_query_factory(self, method: typing.Any) -> typing.Any:
        def wrapper(*args, **kwargs):
            return ProxyQuery(method(*args, **kwargs), self)
        return wrapper
