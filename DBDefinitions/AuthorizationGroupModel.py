import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import relationship

from .uuid import UUIDColumn, UUIDFKey
from .Base import BaseModel

class AuthorizationGroupModel(BaseModel):
    """Spravuje pristupove informace zalozene na skupinach"""

    __tablename__ = "awauthorizationgroups"

    id = UUIDColumn()

    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True, comment="Identifikátor autorizácie (foreign key) a indexovaný stĺpec")
    #authorization = relationship("AuthorizationModel", back_populates="groupaccesses")

    group_id = UUIDFKey(nullable=True, comment="Identifikátor skupiny (foreign key) s možnosťou null hodnoty")#Column(ForeignKey("groups.id"), index=True)

    accesslevel = Column(Integer, comment="Úroveň prístupu v podobe celého čísla")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(),
                     comment="Dátum a čas vytvorenia záznamu")

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Dátum a čas poslednej zmeny")

    changedby = UUIDFKey(nullable=True, comment="Identifikátor používateľa, ktorý vykonal poslednú zmenu")  # Column(ForeignKey("users.id"), index=True, nullable=True)

    createdby = UUIDFKey(nullable=True, comment="Identifikátor používateľa, ktorý vytvoril tento záznam")  # Column(ForeignKey("users.id"), index=True, nullable=True)
