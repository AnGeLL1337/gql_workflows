import datetime
import strawberry
import uuid

from typing import List, Optional, Annotated

from sqlalchemy.util import typing

from GraphTypeDefinitions.BaseGQLModel import BaseGQLModel
from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_authorization_id,
    resolve_group_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)
from utils.Dataloaders import getLoadersFromInfo, getGroupFromInfo


# Annotácie na definíciu typov
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
AuthorizationGQLModel = Annotated["AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")]
AuthorizationResultGQLModel = Annotated["AuthorizationResultGQLModel", strawberry.lazy(".authorizationGQLModel")]

@strawberry.input(description="Definition of group update")
class AuthorizationGroupUpdateGQLModel:
    lastchange: datetime.datetime
    accesslevel: typing.Optional[int] = None


# Definícia GQL modelu AuthorizationGroupGQLModel
@strawberry.federation.type(
    keys=["id"], 
    name="AuthorizationGroupGQLModel",
    description="""Entity representing an access to information"""
)

class AuthorizationGroupGQLModel(BaseGQLModel):
    # Metóda na riešenie referencie
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).authorizationgroups

    id = resolve_id
    accesslevel = resolve_accesslevel
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(description="""Authorizations attached to this group""")
    async def authorization(self, info: strawberry.types.Info) -> Optional["AuthorizationGQLModel"]:
        loader = getLoadersFromInfo(info).authorization
        result = await loader.load(self.authorization_id)
        return result

    @strawberry.field(description="""Proxy groups attached to this group""")
    def group(self) -> Optional["GroupGQLModel"]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)


#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass

class AuthorizationGroupWhereFilter:
    authorization_id: typing.Optional[uuid.UUID] = None
    user_id: typing.Optional[uuid.UUID] = None
    group_id: typing.Optional[uuid.UUID] = None
    accesslevel: typing.Optional[int] = None

authorization_group_by_id = createRootResolver_by_id(
    AuthorizationGroupGQLModel,
    description="Returns authorization group by id")

authorization_group_page = createRootResolver_by_page(
    scalarType=AuthorizationGroupGQLModel,
    whereFilterType=AuthorizationGroupWhereFilter,
    description="Returns authorization group by page",
    loaderLambda = lambda info: getLoadersFromInfo(info).authorizationgroups
)

#####################################################################
#
# Mutation section
#
#####################################################################

@strawberry.input(description="Input structure - C operation")
class AuthorizationGroupInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated",
                                                      default=None)
    authorization_id: uuid.UUID = strawberry.field(description="id of authorization")
    group_id: uuid.UUID = strawberry.field(description="id of group")
    accesslevel: int = strawberry.field(description="access level")
    createdby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure - U operation")
class AuthorizationGroupUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    accesslevel: typing.Optional[int] = strawberry.field(description="access level", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberry.type(description="Result of CU operation over authorization group")
class AuthorizationGroupResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
    For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="subject of operation")
    async def authorization_group(self, info: strawberry.types.Info) -> AuthorizationGroupGQLModel:
        return await AuthorizationGroupGQLModel.resolve_reference(info, self.id)


@strawberry.mutation(description="Create a new authorization group")
async def authorization_group_insert(
        self, info: strawberry.types.Info, authorization_group: AuthorizationGroupInsertGQLModel
) -> AuthorizationGroupResultGQLModel:
    group = getGroupFromInfo(info)
    authorization_group.createdby = uuid.UUID(group["id"])
    loader = getLoadersFromInfo(info).authorizationgroups
    row = await loader.insert(authorization_group)
    result = AuthorizationGroupResultGQLModel(id=row.id, msg="ok")
    result.msg = "ok"
    result.id = row.id
    return result


@strawberry.mutation(description="Update the authorization user")
async def authorization_group_update(
        self, info: strawberry.types.Info, authorization_group: AuthorizationGroupUpdateGQLModel
) -> AuthorizationGroupResultGQLModel:
    group = getGroupFromInfo(info)
    loader = getLoadersFromInfo(info).authorizationgroups
    row = await loader.update(authorization_group)
    result = AuthorizationGroupResultGQLModel(id=row.id, msg="ok")
    return result