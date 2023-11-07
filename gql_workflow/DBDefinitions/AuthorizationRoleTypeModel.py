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
    id = UUIDColumn(comment="Unikátní identifikátor skupiny")
    
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True, comment="Identifikátor autorizace (foreign key) a indexovaný sloupec")
    #authorization = relationship("AuthorizationModel", back_populates="roletypeacesses")
    
    group_id = UUIDFKey(nullable=True, comment="Identifikátor skupiny (foreign key) s možností null hodnoty")#ForeignKey("groups.id"), index=True)
    
    roletype_id = UUIDFKey(nullable=True, comment="Identifikátor typu role (foreign key) s možností null hodnoty")#Column(ForeignKey("roletypes.id"), index=True)
    
    accesslevel = Column(Integer, comment="Úroveň přístupu v podobě celého čísla")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Datum a čas vytvoření záznamu, server default nastavený na aktuální čas")
    
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Datum a čas poslední změny, server default nastavený na aktuální čas")
    
    changedby = UUIDFKey(nullable=True, comment="Identifikátor uživatele, který vykonal poslední změnu, možná null hodnota")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    createdby = UUIDFKey(nullable=True, comment="Identifikátor uživatele, který vytvořil tento záznam, možná null hodnota")#Column(ForeignKey("users.id"), index=True, nullable=True)

