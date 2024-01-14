import datetime
import uuid

import strawberry
from typing import Optional, Annotated, List

from sqlalchemy.util import typing

from GraphTypeDefinitions.BaseGQLModel import BaseGQLModel
from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_authorization_id,
    resolve_user_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

# Anotace na definici typů
AuthorizationGQLModel = Annotated["AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")]
AuthorizationUserGQLModel = Annotated["AuthorizationUserGQLModel", strawberry.lazy(".authorizationUserGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]


@strawberry.input(description="Definition of user update")
class AuthorizationUserUpdateGQLModel:
    lastchange: datetime.datetime
    accesslevel: typing.Optional[int] = None


@strawberry.federation.type(
    keys=["id"],
    name="AuthorizationUserGQLModel",
    description="""Entity representing an access to information"""
)
class AuthorizationUserGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).authorizationusers

    id = resolve_id
    accesslevel = resolve_accesslevel
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(description="""Authorization attached to this user""")
    async def authorization(self, info: strawberry.types.Info) -> Optional["AuthorizationGQLModel"]:
        loader = getLoadersFromInfo(info).authorization
        result = await loader.load(self.authorization_id)
        return result


#####################################################################
#
# Special fields for query
#
#####################################################################


@strawberry.field(description="""Retrieve user by id""")
async def authorization_user_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[AuthorizationUserGQLModel]:
    return await AuthorizationUserGQLModel.resolve_reference(info=info, id=id)


from dataclasses import dataclass
from .utils import createInputs


@createInputs
@dataclass
class AuthorizationUserWhereFilter:
    authorization_id: uuid.UUID
    user_id: uuid.UUID
    accesslevel: int


'''
authorization_user_by_id = createRootResolver_by_id(
    AuthorizationUserGQLModel,
    description="Returns authorization user by id")
'''

authorization_user_page = createRootResolver_by_page(
    scalarType=AuthorizationUserGQLModel,
    whereFilterType=AuthorizationUserWhereFilter,
    description="Returns authorization user by page",
    loaderLambda=lambda info: getLoadersFromInfo(info).authorizationusers
)


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input(description="Input structure - C operation")
class AuthorizationUserInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated",
                                                      default=None)
    authorization_id: uuid.UUID = strawberry.field(description="id of authorization")
    user_id: uuid.UUID = strawberry.field(description="id of user")
    accesslevel: int = strawberry.field(description="access level")
    createdby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure - U operation")
class AuthorizationUserUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    accesslevel: typing.Optional[int] = strawberry.field(description="access level", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure - D operation")
class AuthorizationUserDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")


@strawberry.type(description="""Result model for authorization user deletion""")
class AuthorizationUserDeleteResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(description="ID of deleted object if msg is ok")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.""")


@strawberry.type(description="Result of CU operation over authorization user")
class AuthorizationUserResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
    For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="subject of operation")
    async def authorization_user(self, info: strawberry.types.Info) -> AuthorizationUserGQLModel:
        return await AuthorizationUserGQLModel.resolve_reference(info, self.id)


@strawberry.mutation(description="Create a new authorization user")
async def authorization_user_insert(
        self, info: strawberry.types.Info, authorization_user: AuthorizationUserInsertGQLModel
) -> AuthorizationUserResultGQLModel:
    user = getUserFromInfo(info)
    authorization_user.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authorizationusers
    row = await loader.insert(authorization_user)
    result = AuthorizationUserResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(description="Update the authorization user")
async def authorization_user_update(
        self, info: strawberry.types.Info, authorization_user: AuthorizationUserUpdateGQLModel
) -> AuthorizationUserResultGQLModel:
    user = getUserFromInfo(info)
    authorization_user.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authorizationusers
    row = await loader.update(authorization_user)
    result = AuthorizationUserResultGQLModel(id=row.id, msg="ok") if row else (
        AuthorizationUserResultGQLModel(id=authorization_user.id, msg="fail, bad lastchange"))
    return result


@strawberry.mutation(description="Delete the authorization user")
async def authorization_user_delete(
        self, info: strawberry.types.Info, authorization_user_id: AuthorizationUserDeleteGQLModel
) -> AuthorizationUserDeleteResultGQLModel:
    user_id_to_delete = authorization_user_id.id
    loader = getLoadersFromInfo(info).authorizationusers
    row = await loader.delete(user_id_to_delete)
    result = AuthorizationUserDeleteResultGQLModel(id=user_id_to_delete, msg="ok") if row else (
        AuthorizationUserDeleteResultGQLModel(id=user_id_to_delete, msg="fail, user not found"))
    return result
