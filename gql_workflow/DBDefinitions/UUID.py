import uuid
from typing import Optional

from sqlalchemy import (
    Column,
    String
)


def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDColumn(name=None,comment: Optional[str] = None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString, comment=comment)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString, comment=comment
        )


def UUIDFKey(*, ForeignKey=None, nullable=False,comment: Optional[str] = None):
    if ForeignKey is None:
        return Column(
            String, index=True, nullable=nullable, comment=comment
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable, comment=comment
        )