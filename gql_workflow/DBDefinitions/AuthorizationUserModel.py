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

class AuthorizationUserModel(BaseModel):
    """Spravuje pristupove informace zalozene na uzivatelich"""

    __tablename__ = "awauthorizationusers"
    
    id = UUIDColumn(comment="Unikátní identifikátor skupiny")
    
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="useraccesses")
    
    user_id = UUIDFKey(nullable=True, comment="Identifikátor uživatele (foreign key) s možností null hodnoty")#Column(ForeignKey("users.id"), index=True)
    
    accesslevel = Column(Integer, comment="Úroveň přístupu v podobě celého čísla")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Datum a čas vytvoření záznamu, server default nastavený na aktuální čas")
    
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Datum a čas poslední změny, server default nastavený na aktuální čas")
    
    changedby = UUIDFKey(nullable=True, comment="Identifikátor uživatele, který vykonal poslední změnu, možná null hodnota")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    createdby = UUIDFKey(nullable=True, comment="Identifikátor uživatele, který vytvořil tento záznam, možná null hodnota")#Column(ForeignKey("users.id"), index=True, nullable=True)

