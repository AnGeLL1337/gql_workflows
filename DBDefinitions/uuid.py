from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID # Fixed changing UUID type to varchar!!!
#https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.UUID.params.as_uuid

uuid = uuid4

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(UUID, index=True, comment=comment, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(UUID, primary_key=True, comment="primary key", default=uuid)