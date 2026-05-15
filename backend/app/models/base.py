from datetime import datetime
from enum import StrEnum
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy import DateTime, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(String(255), unique=True, nullable=False)]
int_uniq = Annotated[int, mapped_column(unique=True, nullable=False)]
created_at = Annotated[
    datetime, mapped_column(DateTime(timezone=True), server_default=func.now())
]
updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    ),
]


def IntrospectedEnum(enum_cls: type[StrEnum], **kwargs) -> sa.Enum:
    return sa.Enum(enum_cls, values_callable=lambda x: [e.value for e in x], **kwargs)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
