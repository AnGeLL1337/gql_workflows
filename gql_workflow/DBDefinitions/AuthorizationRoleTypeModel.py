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

class AuthorizationRoleTypeModel(BaseModel):
    """Spravuje pristupove informace zalozene na rolich ve skupinach"""

    __tablename__ = "awauthorizationroletypes"
    # Unikátní identifikátor skupiny
    id = UUIDColumn()
    
    # Identifikátor autorizace (foreign key) a indexovaný sloupec
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="roletypeacesses")
    
    # Identifikátor skupiny (foreign key) s možností null hodnoty
    group_id = UUIDFKey(nullable=True)#ForeignKey("groups.id"), index=True)
    
    # Identifikátor typu role (foreign key) s možností null hodnoty
    roletype_id = UUIDFKey(nullable=True)#Column(ForeignKey("roletypes.id"), index=True)
    
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

