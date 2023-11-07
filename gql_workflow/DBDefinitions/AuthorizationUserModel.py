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
    
    # Unikátní identifikátor skupiny
    id = UUIDColumn()
    
    
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="useraccesses")
    
    # Identifikátor uživatele (foreign key) s možností null hodnoty
    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    
    # Úroveň přístupu v podobě celého čísla
    accesslevel = Column(Integer)

    # Datum a čas vytvoření záznamu, server default nastavený na aktuální čas
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    
    # Datum a čas poslední změny, server default nastavený na aktuální čas
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    
    # Identifikátor uživatele, který vykonal poslední změnu, možná null hodnota
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    # Identifikátor uživatele, který vytvořil tento záznam, možná null hodnota
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

