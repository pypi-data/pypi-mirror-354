""" UUID-compatible Typed IDs with prefixes.

    \b
        user_nnv5rr3rfk3hgry6xrygr
        └──┘ └───────────────────┘
        type    uuid (base58)

    First generate the Types using generate(...), then use them
    like so:

    >>> from uuid_extensions import uuid7
    >>> from typeid import generate
    >>> typeids = generate("sk", "pk", "user", "apikey")
    >>> assert str(typeids.SkId(uuid7().hex)).startswith("sk_")
    >>> assert str(typeids.PkId(uuid7().hex)).startswith("pk_")
    >>> assert str(typeids.UserId(uuid7().hex)).startswith("user_")
    >>> assert str(typeids.ApikeyId(uuid7().hex)).startswith("apikey_")
    >>> assert (typeids.UserId("user_nnv5rr3rfk3hgry6xrygr").hex
    ...    == "0664c4135ed83faabd4bc0dc33839c9f")
    >>> extra_types = generate("admin", suffix="IdUseWithCare")
    >>> assert str(extra_types.AdminIdUseWithCare(uuid7().hex)).startswith("admin_")
"""

from typing import Optional, Callable
from base58 import b58encode, b58decode
from uuid import UUID

try:
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID
    from sqlalchemy.types import CHAR, TypeDecorator

    class SQLAMixin(TypeDecorator):
        """Mixin class to add SQLAlchemy support to BaseId."""

        impl = CHAR(32)
        cache_ok = True

        def load_dialect_impl(self, dialect):
            if dialect.name == "postgresql":
                return dialect.type_descriptor(PG_UUID())
            return dialect.type_descriptor(self.impl)

        def process_bind_param(self, value, dialect):
            if value is None:
                return value

            if not isinstance(value, UUID):
                value = self.__class__(value)

            if dialect.name == "postgresql":
                return str(UUID(value.hex))
            return value.hex

        def process_result_value(self, value, dialect):
            if value is None:
                return value
            return self.__class__(value)

        @property
        def python_type(self):
            return self.__class__

        def __repr__(self):
            """We need this so alembic can use the correct type for upgrades"""
            return f"{self.__class__.__name__}()"

    BASE = (UUID, SQLAMixin)
except ImportError:
    BASE = (UUID,)


class BaseId(*BASE):
    """BaseID implementation that does the lifting of a UUID into a typed UUID
    and formats it more nicely.

    :param _prefix: The internal _prefix is filled in the generate() method
    """

    #: This class variable will be filled in by type() later own
    _prefix: str = ""
    _generator: Optional[Callable] = None
    _encode = staticmethod(b58encode)
    _decode = staticmethod(b58decode)

    def __init__(self, id: Optional[UUID | str | bytes] = None) -> None:
        if id is None:
            if callable(self._generator):
                id = self._generator()
            else:
                # Fall back to UUID's default (uuid4).
                super().__init__()
                return

        if isinstance(id, UUID):
            super().__init__(hex=id.hex)
        elif isinstance(id, bytes) and len(id) == 16:
            super().__init__(bytes=id)
        elif isinstance(id, str):
            if id.startswith(f"{self._prefix}_"):
                prefix_free_id = id[len(self._prefix) + 1 :]
                uid_bytes: bytes = self._decode(prefix_free_id.encode("ascii"))
                super().__init__(bytes=uid_bytes)
            elif "_" in id:
                found_prefix = id[: id.index("_")]
                raise ValueError(
                    f"Wrong prefix, got {found_prefix}, expected {self._prefix}"
                )
            else:
                # Assume it's a standard hex string representation of a UUID.
                super().__init__(hex=id)
        else:
            raise TypeError(
                f"Unsupported type for id: {type(id)}. "
                "Requires UUID, str, bytes, or None."
            )

    def __str__(self) -> str:
        """Prefix and base58 encode the id

        :return: encoded and prefixed id as string
        """
        prefix = str(self._prefix)
        id = self._encode(self.bytes).decode("ascii")
        return f"{prefix}_{id}"


class AttrDict(dict):
    """This class enables us to access the return values of generate() as
    attributes."""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def generate(
    *args: str,
    suffix: str = "Id",
    generator: Callable = None,
) -> AttrDict:
    """Generate types based on a list of arguments. Each argument will result in
    a new type named after the argument (camel-cased) with the defined suffix at the end.

    :param *args: list of strings for which to generate typed Id classes
    :param suffix: (Id) suffix used in the classes
    :param generator: (None) Allows to provide a generator for new instances
    :return: AttributeClass that allows to access new classes through attributes

    Usage
    =====

    >>> from uuid_extensions import uuid7
    >>> from typeid import generate
    >>> typed_ids = generate(
    ...     "user",
    ...     "apikey",
    ...     generator=lambda: uuid7().hex
    ... )
    >>> user_id = str(typed_ids.UserId())
    >>> # user_id = user_nnv5rr3rfk3hgry6xrygr
    >>> u_id_typed = typed_ids.userId("user_nnv5rr3rfk3hgry6xrygr")
    """
    ret = {}
    for _type in args:
        name = f"{_type.capitalize()}{suffix}"
        typeid_class = type(
            name, (BaseId,), dict(_prefix=_type, _generator=staticmethod(generator))
        )
        globals()[name] = typeid_class
        ret[name] = typeid_class
    return AttrDict(ret)


if __name__ == "__main__":
    import doctest
    from uuid_extensions import uuid7

    generate("sk", "pk", "user", "apikey")
    generate("admin", suffix="IdUseWithCare", generator=lambda: uuid7().hex)

    doctest.testmod()
