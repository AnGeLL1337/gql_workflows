from typing import Optional
from uuid import uuid4, UUID
from sqlalchemy import Column, Uuid
uuid = uuid4

'''
def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDColumn(name=None, comment: Optional[str] = None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString, comment=comment)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString, comment=comment
        )


def UUIDFKey(*, ForeignKey=None, nullable=False, comment: Optional[str] = None):
    if ForeignKey is None:
        return Column(
            String, index=True, nullable=nullable, comment=comment
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable, comment=comment
        )
'''


def UUIDFKey(comment: Optional[str] = None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)


def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)