import uuid

import strawberry
from typing import List, Union, Annotated

from .BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo
from ._GraphPermissions import OnlyForAuthentized
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    createRootResolver_by_id,
    createRootResolver_by_page,
)

# Annotácie na definíciu typov
GroupTypeGQLModel = Annotated["GroupTypeGQLModel", strawberry.lazy(".externals")]
AuthorizationUserGQLModel = Annotated["AuthorizationUserGQLModel", strawberry.lazy(".authorizationUserGQLModel")]
AuthorizationGroupGQLModel = Annotated["AuthorizationGroupGQLModel", strawberry.lazy(".authorizationGroupGQLModel")]
AuthorizationRoleTypeGQLModel = Annotated["AuthorizationRoleTypeGQLModel", strawberry.lazy(
    '.authorizationRoleTypeGQLModel')]


@strawberry.federation.type(
    keys=["id"],
    name="AuthorizationGQLModel",
    description="""Entity representing an access to information"""
)
class AuthorizationGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).authorization

    id = resolve_id

    @strawberry.field(description="""Proxy users attached to this authorization""",
                      permission_classes=[OnlyForAuthentized(isList=True)])
    async def users(self, info: strawberry.types.Info) -> List["AuthorizationUserGQLModel"]:
        loader = getLoadersFromInfo(info).authorizationusers
        result = await loader.filter_by(authorization_id=self.id)
        return result

    @strawberry.field(description="""Proxy groups attached to this authorization""",
                      permission_classes=[OnlyForAuthentized(isList=True)])
    async def groups(self, info: strawberry.types.Info) -> List["AuthorizationGroupGQLModel"]:
        loader = getLoadersFromInfo(info).authorizationgroups
        result = await loader.filter_by(authorization_id=self.id)
        return result

    @strawberry.field(description="""Proxy role types attached to this authorization""",
                      permission_classes=[OnlyForAuthentized(isList=True)])
    async def role_types(self, info: strawberry.types.Info) -> List["AuthorizationRoleTypeGQLModel"]:
        loader = getLoadersFromInfo(info).authorizationroletypes
        result = await loader.filter_by(authorization_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################


@createInputs
@dataclass
class AuthorizationWhereFilter:
    name: str
    name_en: str


authorization_by_id = createRootResolver_by_id(
    AuthorizationGQLModel,
    description="Retrieves the authorization")

authorization_page = createRootResolver_by_page(scalar_type=AuthorizationGQLModel,
                                                where_filter_type=AuthorizationWhereFilter,
                                                loader_lambda=lambda info: getLoadersFromInfo(info).authorization,
                                                description="Retrieves authorizations paged")


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input(description="""Definition of authorization added to entity""")
class AuthorizationInsertGQLModel:
    id: uuid.UUID = strawberry.field(description="""primary key (UUID)""")


@strawberry.type(description="""Result of authorization operation""")
class AuthorizationResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of authorization operation""")
    async def authorization(self, info: strawberry.types.Info) -> Union[AuthorizationGQLModel, None]:
        result = await AuthorizationGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="""Creates a new authorization""",
                     permission_classes=[OnlyForAuthentized()])
async def authorization_insert(
        self, info: strawberry.types.Info,authorization: AuthorizationInsertGQLModel
) -> AuthorizationResultGQLModel:
    loader = getLoadersFromInfo(info).authorization
    row = await loader.insert(authorization)
    result = AuthorizationResultGQLModel(id=row.id, msg="ok")
    return result
