import typing


if typing.TYPE_CHECKING:
    # noinspection PyProtectedMember
    from sqlalchemy.sql.selectable import _ForUpdateOfArgument
    # noinspection PyProtectedMember
    from sqlalchemy.sql._typing import _ColumnsClauseArgument, _DMLTableArgument, _SelectStatementForCompoundArgument
    # noinspection PyProtectedMember
    from sqlalchemy.sql._typing import (
        _TypedColumnClauseArgument,
        _ColumnsClauseArgument,
        _TP, _T0, _T1, _T2,
        _T3, _T4, _T5, _T6,
        _T7, _T8, _T9
    )


class GenerativeSelect(typing.Protocol):
    def with_for_update(
        self,
        *,
        nowait: bool = False,
        read: bool = False,
        of: typing.Optional[_ForUpdateOfArgument] = None,
        skip_locked: bool = False,
        key_share: bool = False,
    ) -> typing.Self: ...


class CompoundSelect(typing.Protocol):
    pass


class Select(typing.Protocol):
    pass


class Delete(typing.Protocol):
    pass


class Exists(typing.Protocol):
    pass


class Insert(typing.Protocol):
    pass


class Update(typing.Protocol):
    pass
