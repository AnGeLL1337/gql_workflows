import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s',
    datefmt='%Y-%m-%dT%I:%M:%S')

from fastapi import FastAPI, Request
import strawberry
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from DBDefinitions import ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()

appcontext = {}


@asynccontextmanager
async def initEngine(app: FastAPI):
    from DBDefinitions import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()

    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    from utils.DBFeeder import initDB
    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from GraphTypeDefinitions import schema

app = FastAPI(lifespan=initEngine)


async def get_context():
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass

    from utils.Dataloaders import createLoadersContext
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    result = {**context}
    result["user"] = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
    return result


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/gql")

from doc import attachVoyager

attachVoyager(app, path="/gql/doc")

print("All initialization is done")


@app.get('/hello')
def hello(request: Request):
    headers = request.headers
    auth = request.auth
    user = request.scope["user"]
    return {'hello': 'world', 'headers': {**headers}, 'auth': f"{auth}", 'user': user}


# from starlette.authentication import (
#     AuthCredentials, AuthenticationBackend
# )
# from starlette.middleware.authentication import AuthenticationMiddleware


# class BasicAuthBackend(AuthenticationBackend):
#     async def authenticate(self, conn):
#         return AuthCredentials(["authenticated"]), {"name": "John", "surname": "Newbie"}


# app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
'''
import os
DEMO = os.getenv("DEMO", None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")
'''