import datetime
import uuid

import strawberry
from typing import List, Optional, Annotated

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
    authorization_id = resolve_authorization_id
    user_id = resolve_user_id
    accesslevel = resolve_accesslevel
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby


#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class AuthorizationUserWhereFilter:
    authorization_id: typing.Optional[uuid.UUID] = None
    user_id: typing.Optional[uuid.UUID] = None
    accesslevel: typing.Optional[int] = None

authorization_user_by_id = createRootResolver_by_id(
    AuthorizationUserGQLModel,
    description="Returns authorization user by id")

authorization_user_page = createRootResolver_by_page(
    scalarType=AuthorizationUserGQLModel,
    whereFilterType=AuthorizationUserWhereFilter,
    description="Returns authorization user by page",
    loaderLambda = lambda info: getLoadersFromInfo(info).authorizationusers
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


@strawberry.type(description="Result of CU operation over authorization user")
class AuthorizationUserResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
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
    result.msg = "ok"
    result.id = row.id
    return result


@strawberry.mutation(description="Update the authorization user")
async def authorization_user_update(
        self, info: strawberry.types.Info, authorization_user: AuthorizationUserUpdateGQLModel
) -> AuthorizationUserResultGQLModel:
    user = getUserFromInfo(info)
    #authorization_user.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authorizationusers
    row = await loader.update(authorization_user)
    result = AuthorizationUserResultGQLModel(id=row.id, msg="ok")
    result.msg = "ok"
    result.id = row.id
    return result

