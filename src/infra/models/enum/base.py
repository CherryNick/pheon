from typing import Any, Optional, Type

from sqlalchemy import Integer, TypeDecorator
from sqlalchemy.engine.interfaces import Dialect


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = Integer

    def __init__(self, enumtype: Type[Any], *args: Any, **kwargs: Any) -> None:
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype: Type[Any] = enumtype

    def process_bind_param(self, value: Any, _: Dialect) -> Optional[int]:
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value: Optional[int], _: Dialect) -> Any:
        return self._enumtype(value)