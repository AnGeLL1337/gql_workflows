import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey
)

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel


class WorkflowTransitionModel(BaseModel):
    """zmena stav - prechod (hrana)"""

    __tablename__ = "awworkflowtransitions"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    valid = Column(Boolean)
    
    workflow_id = Column(ForeignKey("awworkflows.id"), index=True)
    sourcestate_id = Column(ForeignKey("awworkflowstates.id"), index=True)
    destinationstate_id = Column(ForeignKey("awworkflowstates.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)
    # Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)
    # Column(ForeignKey("users.id"), index=True, nullable=True)
