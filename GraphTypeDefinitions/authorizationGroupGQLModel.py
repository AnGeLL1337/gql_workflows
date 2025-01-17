import datetime
import strawberry
import uuid

from typing import Optional, Annotated

from sqlalchemy.util import typing
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

from GraphTypeDefinitions.BaseGQLModel import BaseGQLModel
from ._GraphPermissions import OnlyForAuthentized

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo


# Annotácie na definíciu typov
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
AuthorizationGQLModel = Annotated["AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")]
AuthorizationResultGQLModel = Annotated["AuthorizationResultGQLModel", strawberry.lazy(".authorizationGQLModel")]


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

    @strawberry.field(description="""Authorizations attached to this group""", permission_classes=[OnlyForAuthentized()])
    async def authorization(self, info: strawberry.types.Info) -> Optional["AuthorizationGQLModel"]:
        loader = getLoadersFromInfo(info).authorization
        result = await loader.load(self.authorization_id)
        return result

    @strawberry.field(description="""Proxy groups attached to this group""", permission_classes=[OnlyForAuthentized()])
    def group(self) -> Optional["GroupGQLModel"]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)


#####################################################################
#
# Special fields for query
#
#####################################################################


@createInputs
@dataclass
class AuthorizationGroupWhereFilter:
    authorization_id: typing.Optional[uuid.UUID]
    user_id: typing.Optional[uuid.UUID]
    group_id: typing.Optional[uuid.UUID]
    accesslevel: typing.Optional[int]


authorization_group_by_id = createRootResolver_by_id(
    AuthorizationGroupGQLModel,
    description="Returns authorization group by id")

authorization_group_page = createRootResolver_by_page(scalar_type=AuthorizationGroupGQLModel,
                                                      where_filter_type=AuthorizationGroupWhereFilter,
                                                      loader_lambda=lambda info: getLoadersFromInfo(
                                                          info).authorizationgroups,
                                                      description="Returns authorization group by page")

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


@strawberry.input(description="Input structure for group - U operation")
class AuthorizationGroupUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    accesslevel: typing.Optional[int] = strawberry.field(description="access level", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure - D operation")
class AuthorizationGroupDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")


@strawberry.type(description="""Result model for authorization group deletion""")
class AuthorizationGroupDeleteResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(description="ID of deleted object if msg is ok")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.""")


@strawberry.type(description="Result of CU operation over authorization group")
class AuthorizationGroupResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.
    For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="subject of operation")
    async def authorization_group(self, info: strawberry.types.Info) -> AuthorizationGroupGQLModel:
        return await AuthorizationGroupGQLModel.resolve_reference(info, self.id)


@strawberry.mutation(description="Create a new authorization group", permission_classes=[OnlyForAuthentized()])
async def authorization_group_insert(
        self, info: strawberry.types.Info, authorization_group: AuthorizationGroupInsertGQLModel
) -> AuthorizationGroupResultGQLModel:
    actinguser = getUserFromInfo(info)
    authorization_group.createdby = uuid.UUID(actinguser["id"])

    loader = getLoadersFromInfo(info).authorizationgroups
    row = await loader.insert(authorization_group)
    result = AuthorizationGroupResultGQLModel(id=row.id, msg="ok")
    result.msg = "ok"
    result.id = row.id
    return result


@strawberry.mutation(description="Update the authorization group", permission_classes=[OnlyForAuthentized()])
async def authorization_group_update(
        self, info: strawberry.types.Info, authorization_group: AuthorizationGroupUpdateGQLModel
) -> AuthorizationGroupResultGQLModel:
    actinguser = getUserFromInfo(info)
    authorization_group.changedby = uuid.UUID(actinguser["id"])
    loader = getLoadersFromInfo(info).authorizationgroups
    row = await loader.update(authorization_group)
    result = AuthorizationGroupResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(description="Delete the authorization group", permission_classes=[OnlyForAuthentized()])
async def authorization_group_delete(
        self, info: strawberry.types.Info, authorization_group_id: AuthorizationGroupDeleteGQLModel
) -> AuthorizationGroupDeleteResultGQLModel:
    group_id_to_delete = authorization_group_id.id
    loader = getLoadersFromInfo(info).authorizationgroups
    row = await loader.delete(group_id_to_delete)
    result = AuthorizationGroupDeleteResultGQLModel(id=group_id_to_delete, msg="ok") if row else (
        AuthorizationGroupDeleteResultGQLModel(id=group_id_to_delete, msg="fail, group not found"))
    return result