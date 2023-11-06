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

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class AuthorizationGroupModel(BaseModel):
    """Spravuje pristupove informace zalozene na skupinach"""

    __tablename__ = "awauthorizationgroups"

    # Unikátny identifikátor skupiny
    id = UUIDColumn()

    # Identifikátor autorizácie (foreign key) a indexovaný stĺpec
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="groupaccesses")

    # Identifikátor skupiny (foreign key) s možnosťou null hodnoty
    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)

    # Úroveň prístupu v podobe celého čísla
    accesslevel = Column(Integer)

    # Dátum a čas vytvorenia záznamu, server default nastavený na aktuálny čas
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(),
                     comment="FK používateľa, ktorý vytvoril tento záznam")

    # Dátum a čas poslednej zmeny, server default nastavený na aktuálny čas
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    # Identifikátor používateľa, ktorý vykonal poslednú zmenu, možno null hodnota
    changedby = UUIDFKey(nullable=True)  # Column(ForeignKey("users.id"), index=True, nullable=True)

    # Identifikátor používateľa, ktorý vytvoril tento záznam, možno null hodnota
    createdby = UUIDFKey(nullable=True)  # Column(ForeignKey("users.id"), index=True, nullable=True)
