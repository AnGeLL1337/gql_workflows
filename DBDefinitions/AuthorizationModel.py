from .uuid import UUIDColumn
from .base import BaseModel


class AuthorizationModel(BaseModel):
    """Spravuje pristupove informace"""

    __tablename__ = "awauthorizations"

    #
    id = UUIDColumn()