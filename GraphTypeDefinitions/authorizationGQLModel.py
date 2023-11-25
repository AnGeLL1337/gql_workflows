import uuid

import strawberry
from typing import List, Optional, Union, Annotated

import typing

from .BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo

# Annotácie na definíciu typov
GroupTypeGQLModel = Annotated["GroupTypeGQLModel", strawberry.lazy(".externals")]
AuthorizationUserGQLModel = Annotated["AuthorizationUserGQLModel", strawberry.lazy(".authorizationUserGQLModel")]
AuthorizationGroupGQLModel = Annotated["AuthorizationGroupGQLModel", strawberry.lazy(".authorizationGroupGQLModel")]
AuthorizationRoleTypeGQLModel = Annotated["AuthorizationRoleTypeGQLModel", strawberry.lazy(".authorizationRoleTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)

# Definícia GQL modelu AuthorizationGQLModel
class AuthorizationGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).authorizations

    '''
    # Metóda na riešenie referencie
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).authorizations
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result
    '''
    # Polia modelu
    @strawberry.field(description="""Entity primary key""")
    def id(self, info: strawberry.types.Info) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Proxy users attached to this authorization""")
    async def users(self, info: strawberry.types.Info) -> List["AuthorizationUserGQLModel"]:
        loader = getLoadersFromInfo(info).authorizationusers
        result = await loader.filter_by(authorization_id=self.id)
        return result

    @strawberry.field(description="""Proxy groups attached to this authorization""")
    async def groups(self, info: strawberry.types.Info) -> List["AuthorizationGroupGQLModel"]:
        loader = getLoadersFromInfo(info).authorizationgroups
        result = await loader.filter_by(authorization_id=self.id)
        return result

    @strawberry.field(description="""Proxy role types attached to this authorization""")
    async def role_types(self, info: strawberry.types.Info) -> List["AuthorizationRoleTypeGQLModel"]:
        loader = getLoadersFromInfo(info).authorizationroletypes
        result = await loader.filter_by(authorization_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################

@strawberry.field(description="""Finds an authorization entity by received id""")
async def authorization_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[AuthorizationGQLModel]:
    result = await AuthorizationGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="""Gets a page of authorizations""")
async def authorization_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 20
) -> List["AuthorizationGQLModel"]:
    loader = getLoadersFromInfo(info).authorizations
    result = await loader.page(skip=skip, limit=limit)
    return result
    
#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input(description="""Definition of authorization added to entity""")
class AuthorizationInsertGQLModel:
    id: Optional[strawberry.ID] = None

@strawberry.type(description="""Result of authorization operation""")
class AuthorizationResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of authorization operation""")
    async def authorization(self, info: strawberry.types.Info) -> Union[AuthorizationGQLModel, None]:
        result = await AuthorizationGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Creates a new authorization""")
async def authorization_insert(self, info: strawberry.types.Info, authorization: AuthorizationInsertGQLModel) -> AuthorizationResultGQLModel:
    loader = getLoadersFromInfo(info).authorizations
    row = await loader.insert(authorization)
    result = AuthorizationResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result