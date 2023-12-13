import logging
import json

from fastapi.testclient import TestClient


def create_gql_client() -> TestClient:
    import DBDefinitions

    def compose_connection_string():
        return "sqlite+aiosqlite:///:memory:"

    DBDefinitions.ComposeConnectionString = compose_connection_string

    import main

    client = TestClient(main.app, raise_server_exceptions=False)

    return client


def create_client_function() -> callable:
    client = create_gql_client()

    async def result(query: str, variables: dict = None) -> dict:
        input_json = {
            "query": query,
            "variables": variables
        }
        headers = {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.debug(f"query client for {query} with {variables}")

        response = client.post("/gql", json=input_json, headers=headers)
        return response.json()

    return result


def update_introspection_query():
    from .introspection import query
    client = create_gql_client()
    input_json = {
        "query": query,
        "variables": {}
    }
    response = client.post("/gql", json=input_json)
    response_json = response.json()
    data = response_json["data"]
    print(response_json)
    with open("introspection.json", "w", encoding="utf-8") as f:
        datastr = json.dumps(data)
        f.write(datastr)


update_introspection_query()
