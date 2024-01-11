import datetime
import uuid

import strawberry
from typing import Optional, Annotated, List

from sqlalchemy.util import typing

from GraphTypeDefinitions.BaseGQLModel import BaseGQLModel
from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_authorization_id,
    resolve_group_id,
    resolve_roletype_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from . import AuthorizationGroupGQLModel

# Anotace na definici typů
AuthorizationGQLModel = Annotated["AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]


@strawberry.input(description="Definition of roletype update")
class AuthorizationRoleTypeUpdateGQLModel:
    lastchange: datetime.datetime
    accesslevel: typing.Optional[int] = None


@strawberry.federation.type(
    keys=["id"],
    name="AuthorizationRoleTypeGQLModel",
    description="""Entity representing an access to information"""
)
class AuthorizationRoleTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).authorizationroletypes

    id = resolve_id
    # group_id = resolve_group_id
    # roletype_id = resolve_roletype_id
    # authorization_id = resolve_authorization_id
    accesslevel = resolve_accesslevel
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(description="""Authorizations attached to this roletype""")
    async def authorization(self, info: strawberry.types.Info) -> Optional["AuthorizationGQLModel"]:
        loader = getLoadersFromInfo(info).authorization
        result = await loader.load(self.authorization_id)
        return result

    @strawberry.field(description="""Proxy group attached to this roletype""")
    async def group(self) -> Optional["GroupGQLModel"]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)

    @strawberry.field(description="""Proxy roletype attached to this roletype""")
    def roletype(self) -> Optional["RoleTypeGQLModel"]:
        from .externals import RoleTypeGQLModel
        return RoleTypeGQLModel(id=self.roletype_id)


#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
from .utils import createInputs


@createInputs
@dataclass
class AuthorizationRoleTypeWhereFilter:
    authorization_id: uuid.UUID
    group_id: uuid.UUID
    roletype_id: uuid.UUID
    accesslevel: int


authorization_roletype_by_id = createRootResolver_by_id(
    AuthorizationRoleTypeGQLModel,
    description="""Returns authorization roletype by ID""")

authorization_roletype_page = createRootResolver_by_page(
    scalarType=AuthorizationRoleTypeGQLModel,
    whereFilterType=AuthorizationRoleTypeWhereFilter,
    description="""Returns authorization roletype by page""",
    loaderLambda=lambda info: getLoadersFromInfo(info).authorizationroletypes
)


#####################################################################
#
# Mutation section
#
#####################################################################

@strawberry.input(description="Input structure - C operation")
class AuthorizationRoleTypeInsertGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated",
                                               default=None)
    authorization_id: uuid.UUID = strawberry.field(description="id of authorization")
    group_id: uuid.UUID = strawberry.field(description="id of group")
    roletype_id: uuid.UUID = strawberry.field(description="id of roletype")
    accesslevel: int = strawberry.field(description="access level")
    createdby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure - U operation")
class AuthorizationRoleTypeUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="time of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    accesslevel: typing.Optional[int] = strawberry.field(description="access level", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Input structure - D operation")
class AuthorizationRoleTypeDeleteGQLModel:
    id: uuid.UUID

@strawberry.type(description="""Result model for authorization role type deletion""")
class AuthorizationRoleTypeDeleteResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of authorization role type deletion""")
    async def roletype(self, info: strawberry.types.Info) -> AuthorizationRoleTypeGQLModel | None:
        result = await RoleTypeGQLModel.resolve_reference(info, self.id)
        return result  


@strawberry.type(description="Result of CU operation over authorization roletype")
class AuthorizationRoleTypeResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
    For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="subject of operation")
    async def authorization_roletype(self, info: strawberry.types.Info) -> AuthorizationRoleTypeGQLModel:
        return await AuthorizationRoleTypeGQLModel.resolve_reference(info, self.id)


@strawberry.mutation(description="Create a new authorization roletype")
async def authorization_roletype_insert(
        self, info: strawberry.types.Info, authorization_roletype: AuthorizationRoleTypeInsertGQLModel
) -> AuthorizationRoleTypeResultGQLModel:
    user = getUserFromInfo(info)
    '''
    if user is None:
        return AuthorizationRoleTypeResultGQLModel(id=None, msg="Fail, no authenticated user")
        '''
    authorization_roletype.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authorizationroletypes
    row = await loader.insert(authorization_roletype)
    result = AuthorizationRoleTypeResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(description="Update an existing authorization roletype")
async def authorization_roletype_update(
        self, info: strawberry.types.Info, authorization_roletype: AuthorizationRoleTypeUpdateGQLModel
) -> AuthorizationRoleTypeResultGQLModel:
    user = getUserFromInfo(info)
    '''
    if user is None:
        return AuthorizationRoleTypeResultGQLModel(id=None, msg="fail, no authenticated user")
        '''
    authorization_roletype.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authorizationroletypes
    row = await loader.update(authorization_roletype)
    '''
    if row is None:
        return AuthorizationRoleTypeResultGQLModel(id=authorization_roletype.id, msg="fail, bad lastchange")
        '''
    result = AuthorizationRoleTypeResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(description="Delete an existing authorization roletype")
async def authorization_roletype_delete(
        self, info: strawberry.types.Info, authorization_roletype_id: str
) -> AuthorizationRoleTypeResultGQLModel:
    user = getUserFromInfo(info)
    if user is None:
        return AuthorizationRoleTypeResultGQLModel(id=None, msg="fail, no authenticated user")
    loader = getLoadersFromInfo(info).authorizationroletypes
    row = await loader.delete(authorization_roletype_id)
    if not row:
        return AuthorizationRoleTypeResultGQLModel(id=authorization_roletype_id, msg="fail, roletype not found")
    result = AuthorizationRoleTypeResultGQLModel(id=authorization_roletype_id, msg="ok")
    return result