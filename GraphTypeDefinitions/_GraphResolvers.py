import strawberry
import uuid
import datetime
import typing

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".externals")]
RoleTypeGQLModel = typing.Annotated["RoleTypeGQLModel", strawberry.lazy(".externals")]



@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> uuid.UUID:
    return self.id


async def resolve_user(user_id):
    from .externals import UserGQLModel
    if user_id is None:
        return None
    # Debugging
    # print(f"Resolving user for ID: {user_id}")
    try:
        result = await UserGQLModel.resolve_reference(id=user_id, info=None)
        return result
    except Exception as e:
        # Log the error for debugging
        print(f"Error resolving user: {e}")
        return None


@strawberry.field(description="""Level of authorization""")
def resolve_accesslevel(self) -> int:
    return self.accesslevel


@strawberry.field(description="""Time of last update""")
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange


@strawberry.field(description="""Time of entity introduction""")
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created


@strawberry.field(description="""Who created entity""")
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.createdby)


@strawberry.field(description="""Who made last change""")
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)


resolve_result_id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

# fields for mutations insert and update
resolve_insert_id = strawberry.field(graphql_type=typing.Optional[uuid.UUID], description="primary key (UUID), could be client generated", default=None)
resolve_update_id = strawberry.field(graphql_type=uuid.UUID, description="primary key (UUID), identifies object of operation")
resolve_update_lastchage = strawberry.field(graphql_type=datetime.datetime, description="timestamp of last change = TOKEN")

# fields for mutation result
resolve_cu_result_id = strawberry.field(graphql_type=uuid.UUID, description="primary key of CU operation object")
resolve_cu_result_msg = strawberry.field(graphql_type=str, description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")


'''
def createAttributeScalarResolver(
    scalarType: None = None,
    foreignKeyName: str = None,
    description="Retrieves item by its id",
    permission_classes=()
):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description, permission_classes=permission_classes)
    async def foreignkeyScalar(
        self, info: strawberry.types.Info
    ) -> typing.Optional[scalarType]:
        # 👇 self must have an attribute, otherwise it is fail of definition
        assert hasattr(self, foreignKeyName)
        id = getattr(self, foreignKeyName, None)

        result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
        return result

    return foreignkeyScalar


def createAttributeVectorResolver(
    scalarType: None = None,
    whereFilterType: None = None,
    foreignKeyName: str = None,
    loaderLambda=lambda info: None,
    description="Retrieves items paged",
    skip: int = 0,
    limit: int = 10):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description)
    async def foreignkeyVector(
            self, info: strawberry.types.Info,
            skip: int = skip,
            limit: int = limit,
            where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        params = {foreignKeyName: self.id}
        loader = loaderLambda(info)
        assert loader is not None

        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
        return result

    return foreignkeyVector

'''


def createRootResolver_by_id(scalar_type: typing.Any, description="Retrieves item by its id"):
    assert scalar_type is not None

    @strawberry.field(description=description)
    async def by_id(
            self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalar_type]:
        result = await scalar_type.resolve_reference(info=info, id=id)
        return result

    return by_id


def createRootResolver_by_page(
        scalar_type: typing.Any,
        where_filter_type: typing.Any,
        loader_lambda=lambda info: None,
        description="Retrieves items paged",
        skip: int = 0,
        limit: int = 10):
    assert scalar_type is not None
    assert where_filter_type is not None

    @strawberry.field(description=description)
    async def paged(
            self, info: strawberry.types.Info,
            skip: int = skip, limit: int = limit, where: typing.Optional[where_filter_type] = None
    ) -> typing.List[scalar_type]:
        loader = loader_lambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf)
        return result

    return paged
