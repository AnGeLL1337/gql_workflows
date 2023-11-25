import datetime
import strawberry
from typing import List, Optional, Annotated

from sqlalchemy.util import typing
from uoishelpers import uuid

from utils.Dataloaders import getUserFromInfo


# Funkcia na získanie DataLoaderov
def getLoaders(info):
    return info.context["all"]

# Annotácie na definíciu typov
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
AuthorizationGQLModel = Annotated["AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")]
AuthorizationResultGQLModel = Annotated["AuthorizationResultGQLModel", strawberry.lazy(".authorizationGQLModel")]

# Definícia GQL modelu AuthorizationGroupGQLModel
@strawberry.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)

class AuthorizationGroupGQLModel:
    # Metóda na riešenie referencie
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).authorizationgroups
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    # Polia modelu
    @strawberry.field(description="""Entity primary key""")
    def id(self, info: strawberry.types.Info) -> strawberry.ID:
        return self.id
    
    @strawberry.field(description="""Read, write, or other?""")
    def accesslevel(self, info: strawberry.types.Info) -> int:
        return self.accesslevel
   
    @strawberry.field(description="""To which authorization this access definition belongs""")
    async def authorization(self, info: strawberry.types.Info) -> Optional[AuthorizationGQLModel]:
        result = await gql_workflow.GraphTypeDefinitions.AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
        return result
    
    @strawberry.field(description="""Group which has this access""")
    async def group(self, info: strawberry.types.Info) -> GroupGQLModel:
        result = gql_workflow.GraphTypeDefinitions.GroupGQLModel(id=self.group_id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################

@strawberry.field(description="""Gets a page of group authorizations """)
async def authorization_group_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 20
) -> List["AuthorizationGroupGQLModel"]:
    loader = getLoaders(info).authorizationgroups
    result = await loader.page(skip=skip, limit=limit)
    return result

@strawberry.field(description="Retrieves a group authorization by its id")
async def authorization_group_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Optional[AuthorizationGroupGQLModel]:
    result = await AuthorizationGroupGQLModel.resolve_reference(info=info, id=id)
    return result
#####################################################################
#
# Mutation section
#
#####################################################################

@strawberry.input(description="""Definition of authorization added to group""")
class AuthorizationAddGroupGQLModel:
    """Vstupný model pre pridanie alebo aktualizáciu skupiny v autorizácii."""
    authorization_id: strawberry.ID  # Identifikátor autorizácie
    group_id: strawberry.ID  # Identifikátor skupiny
    accesslevel: int  # Úroveň prístupu

@strawberry.input(description="""Definition of authorization update group""")
class AuthorizationUpdateGroupGQLModel:
    """Vstupný model pre aktualizáciu skupiny v autorizácii."""
    authorization_id: strawberry.ID = strawberry.field(description="Identifikátor autorizácie")
    group_id: strawberry.ID = strawberry.field(description="Identifikátor skupiny")
    lastchange: datetime.datetime
    accesslevel: typing.Optional[int] = strawberry.field(description="Úroveň prístupu")

@strawberry.input(description="""Definition of authorization removed from group""")
class AuthorizationRemoveGroupGQLModel:
    """Vstupný model pre odstránenie skupiny z autorizácie."""
    authorization_id: strawberry.ID  # Identifikátor autorizácie
    group_id: strawberry.ID  # Identifikátor skupiny


@strawberry.mutation(description="""Adds or updates a group at the authorization""")
async def authorization_add_group(self, info: strawberry.types.Info, authorization: AuthorizationAddGroupGQLModel) \
        -> Optional["AuthorizationResultGQLModel"]:
    """Mutácia pre pridanie alebo aktualizáciu skupiny v autorizácii."""
    loader = getLoaders(info).authorizationgroups
    existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
    result = gql_workflow.GraphTypeDefinitions.AuthorizationResultGQLModel()
    result.msg = "ok"
    row = next(existing, None)
    if  row is None:
        row = await loader.insert(authorization)
        result.id = authorization.authorization_id
    else:
        row = await loader.update(row, {"accesslevel": authorization.accesslevel})
        if row is None:
            result.id = None
            result.msg = "fail"
        result.id = authorization.authorization_id
    return result

@strawberry.mutation(description="""Updates a group at the authorization""")
async def authorization_update_group(self, info: strawberry.types.Info, authorization: AuthorizationUpdateGroupGQLModel) \
        -> Optional["AuthorizationResultGQLModel"]:
    loader = getLoaders(info).authorizationgroups  # Načítaj skupinu pomocou loaderu
    existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
    #existing = next(existing, None)

    if existing:
        # Priraď user ID alebo iný identifikátor z info do `changedby`
        user = getUserFromInfo(info)
        existing.changedby = uuid.UUID(user["id"])

        existing.lastchange = datetime.datetime.now()  # Nastav lastchange na aktuálny čas

        result = gql_workflow.GraphTypeDefinitions.AuthorizationResultGQLModel(id=existing.group_id, msg="ok")  # Vytvor výsledok s ID skupiny a predvolenou správou "ok"

        row = await loader.update(existing)  # Aktualizuj skupinu pomocou definovaného loaderu

        result.msg = "fail" if row is None else "ok"  # Nastav správu výsledku podľa úspechu aktualizácie
        return result  # Vráť výsledok

    return gql_workflow.GraphTypeDefinitions.AuthorizationResultGQLModel(id=None, msg="Group not found")  # Ak skupina neexistuje, vráť výsledok s oznamom, že skupina nebola nájdená


@strawberry.mutation(description="""Remove the group from the authorization""")
async def authorization_remove_group(self, info: strawberry.types.Info, authorization: AuthorizationRemoveGroupGQLModel) -> Optional["AuthorizationResultGQLModel"]:
    """Mutácia pre odstránenie skupiny z autorizácie."""
    loader = getLoaders(info).authorizationgroups
    existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
    existing = next(existing, None)
    result = gql_workflow.GraphTypeDefinitions.AuthorizationResultGQLModel()
    result.id = authorization.authorization_id
    if existing is None:
        result.msg = "fail"
    else:
        await loader.delete(existing.id)
        result.msg = "ok"
    return result