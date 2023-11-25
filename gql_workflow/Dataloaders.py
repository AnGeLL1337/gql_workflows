
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
import logging
from functools import cache

from gql_workflow.DBDefinitions import (
    WorkflowModel,
    WorkflowStateModel,
    WorkflowStateRoleTypeModel,
    WorkflowStateUserModel,
    WorkflowTransitionModel,
    AuthorizationGroupModel,
    AuthorizationModel,
    AuthorizationRoleTypeModel,
    AuthorizationUserModel
)

dbmodels = {
    "workflows": WorkflowModel,
    "workflowstates": WorkflowStateModel,
    "workflowstateroletypes": WorkflowStateRoleTypeModel,
    "workflowstateusers": WorkflowStateUserModel,
    "workflowtransitions": WorkflowTransitionModel,
    "authorizationgroups": AuthorizationGroupModel,
    "authorizations": AuthorizationModel,
    "authorizationroletypes": AuthorizationRoleTypeModel,
    "authorizationusers": AuthorizationUserModel
}

import datetime
import aiohttp
import asyncio
import os
from aiodataloader import DataLoader
from uoishelpers.resolvers import select, update, delete


def prepareSelect(model, where: dict):
    usedTables = [model.__tablename__]
    from sqlalchemy import select, and_, or_
    baseStatement = select(model)

    # stmt = select(GroupTypeModel).join(GroupTypeModel.groups.property.target).filter(GroupTypeModel.groups.property.target.c.name == "22-5KB")
    # type(GroupTypeModel.groups.property) sqlalchemy.orm.relationships.RelationshipProperty
    # GroupTypeModel.groups.property.entity.class_
    def limitDict(input):
        if isinstance(input, list):
            return [limitDict(item) for item in input]
        if not isinstance(input, dict):
            # print("limitDict", input)
            return input
        result = {key: limitDict(value) if isinstance(value, dict) else value for key, value in input.items() if
                  value is not None}
        return result

    def convertAnd(model, name, listExpr):
        assert len(listExpr) > 0, "atleast one attribute in And expected"
        results = [convertAny(model, w) for w in listExpr]
        return and_(*results)

    def convertOr(model, name, listExpr):
        # print("enter convertOr", listExpr)
        assert len(listExpr) > 0, "atleast one attribute in Or expected"
        results = [convertAny(model, w) for w in listExpr]
        return or_(*results)

    def convertAttributeOp(model, name, op, value):
        # print("convertAttributeOp", type(model))
        # print("convertAttributeOp", model, name, op, value)
        column = getattr(model, name)
        assert column is not None, f"cannot map {name} to model {model.__tablename__}"
        opMethod = getattr(column, op)
        assert opMethod is not None, f"cannot map {op} to attribute {name} of model {model.__tablename__}"
        return opMethod(value)

    def convertRelationship(model, attributeName, where, opName, opValue):
        # print("convertRelationship", model, attributeName, where, opName, opValue)
        # GroupTypeModel.groups.property.entity.class_
        targetDBModel = getattr(model, attributeName).property.entity.class_
        # print("target", type(targetDBModel), targetDBModel)

        nonlocal baseStatement
        if targetDBModel.__tablename__ not in usedTables:
            baseStatement = baseStatement.join(targetDBModel)
            usedTables.append(targetDBModel.__tablename__)
        # return convertAttribute(targetDBModel, attributeName, opValue)
        return convertAny(targetDBModel, opValue)

        # stmt = select(GroupTypeModel).join(GroupTypeModel.groups.property.target).filter(GroupTypeModel.groups.property.target.c.name == "22-5KB")
        # type(GroupTypeModel.groups.property) sqlalchemy.orm.relationships.RelationshipProperty

    def convertAttribute(model, attributeName, where):
        woNone = limitDict(where)
        # print("convertAttribute", model, attributeName, woNone)
        keys = list(woNone.keys())
        assert len(keys) == 1, "convertAttribute: only one attribute in where expected"
        opName = keys[0]
        opValue = woNone[opName]

        ops = {
            "_eq": "__eq__",
            "_lt": "__lt__",
            "_le": "__le__",
            "_gt": "__gt__",
            "_ge": "__ge__",
            "_in": "in_",
            "_like": "like",
            "_ilike": "ilike",
            "_startswith": "startswith",
            "_endswith": "endswith",
        }

        opName = ops.get(opName, None)
        # if opName is None:
        #     print("op", attributeName, opName, opValue)
        #     result = convertRelationship(model, attributeName, woNone, opName, opValue)
        # else:
        result = convertAttributeOp(model, attributeName, opName, opValue)
        return result

    def convertAny(model, where):

        woNone = limitDict(where)
        # print("convertAny", woNone, flush=True)
        keys = list(woNone.keys())
        # print(keys, flush=True)
        # print(woNone, flush=True)
        assert len(keys) == 1, "convertAny: only one attribute in where expected"
        key = keys[0]
        value = woNone[key]

        convertors = {
            "_and": convertAnd,
            "_or": convertOr
        }
        # print("calling", key, "convertor", value, flush=True)
        # print("value is", value, flush=True)
        convertor = convertors.get(key, convertAttribute)
        convertor = convertors.get(key, None)
        modelAttribute = getattr(model, key, None)
        if (convertor is None) and (modelAttribute is None):
            assert False, f"cannot recognize {model}.{key} on {woNone}"
        if (modelAttribute is not None):
            property = getattr(modelAttribute, "property", None)
            target = getattr(property, "target", None)
            # print("modelAttribute", modelAttribute, target)
            if target is None:
                result = convertAttribute(model, key, value)
            else:
                result = convertRelationship(model, key, where, key, value)
        else:
            result = convertor(model, key, value)
        return result

    filterStatement = convertAny(model, limitDict(where))
    result = baseStatement.filter(filterStatement)
    return result

@cache
def composeAuthUrl():
    hostname = os.environ.get("AUTHURL", "http://localhost:8088/gql")
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname

class AuthorizationLoader(DataLoader):
    query = """
        query ($id: ID!) {
            rolesOnUser(userId: $id) {
                ...role
            }
            rolesOnGroup(groupId: $id) {
                ...role
            }
        }

        fragment role on RoleGQLModel {
            valid
            roletype { id }
            user { id }
            group { id }
        }
    """
    roleUrlEndpoint = composeAuthUrl()

    def __init__(self,
                 roleUrlEndpoint=roleUrlEndpoint,
                 query=query,
                 demo=True):
        super().__init__(cache=True)
        self.roleUrlEndpoint = roleUrlEndpoint
        self.query = query
        self.demo = demo

    async def _load(self, id):
        variables = {"id": f"{id}"}
        headers = {}
        json = {
            "query": self.query,
            "variables": variables
        }
        roleUrlEndpoint = self.roleUrlEndpoint
        async with aiohttp.ClientSession() as session:
            print(f"query {roleUrlEndpoint} for json={json}")
            async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return []
                else:
                    respJson = await resp.json()

        print(respJson)

        assert respJson.get("errors", None) is None
        respdata = respJson.get("data", None)
        assert respdata is not None
        rolesOnUser = respdata.get("rolesOnUser", None)
        rolesOnGroup = respdata.get("rolesOnGroup", None)
        assert rolesOnUser is not None
        assert rolesOnGroup is not None

        return [*rolesOnUser, *rolesOnGroup]

    async def batch_load_fn(self, keys):
        # print('batch_load_fn', keys, flush=True)
        reducedkeys = set(keys)
        awaitables = (self._load(key) for key in reducedkeys)
        results = await asyncio.gather(*awaitables)
        indexedResult = {key: result for key, result in zip(reducedkeys, results)}
        results = [indexedResult[key] for key in keys]
        return results


class Loaders:
    authorizations = None
    authorizationgroups = None
    authorizationroletypes = None
    authorizationusers = None
    pass

def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    class Loaders:

        @property
        @cache
        def authorizations(self):
            return AuthorizationLoader()

        @property
        @cache
        def authorizationgroups(self):
            return createIdLoader(asyncSessionMaker, models["authorizationgroups"])

        @property
        @cache
        def authorizationroletypes(self):
            return createIdLoader(asyncSessionMaker, models["authorizationroletypes"])

        @property
        @cache
        def authorizationusers(self):
            return createIdLoader(asyncSessionMaker, models["authorizationusers"])

        '''
        def createLambda(loaderName, DBModel):
            return lambda self: createIdLoader(asyncSessionMaker, DBModel)

        attrs = {}
        for key, DBModel in models.items():
            attrs[key] = property(cache(createLambda(key, DBModel)))

        Loaders = type('Loaders', (), attrs)   
        return Loaders()
        '''
    return Loaders()

def getLoadersFromInfo(info) -> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders

from functools import cache


demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}
def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        authorization = context["request"].headers.get("Authorization", None)
        if authorization is not None:
            if 'Bearer ' in authorization:
                token = authorization.split(' ')[1]
                if token == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003":
                    result = demouser
                    context["user"] = result
    logging.debug("getUserFromInfo", result)
    return result

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }