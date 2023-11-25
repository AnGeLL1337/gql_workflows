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
from utils.Dataloaders import getLoadersFromInfo

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

