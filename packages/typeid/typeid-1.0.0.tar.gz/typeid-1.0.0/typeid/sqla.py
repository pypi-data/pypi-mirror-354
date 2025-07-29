# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

try:
    from sqlalchemy.dialects.postgresql import UUID
    from sqlalchemy.types import CHAR, TypeDecorator
except ImportError:
    import sys

    print(
        "'sqlalchemy' module is required when using enable_sqla=True", file=sys.stderr
    )
    sys.exit(1)


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """

    impl = CHAR
    cache_ok = True
    typeid_class = uuid.UUID

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            # Force regular UUID representation on postgres
            if not isinstance(value, self.typeid_class):
                return self.typeid_class(value).hex
            else:
                return str(uuid.UUID(value.hex))
        else:
            if not isinstance(value, self.typeid_class):
                return self.typeid_class(value).hex
            else:
                return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return self.typeid_class(value)

    def __repr__(self):
        """We need this so alembic can use the correct type for upgrades"""
        return self.impl.__repr__()
