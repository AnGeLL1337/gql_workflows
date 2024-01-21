import json
import logging
import re
import uuid

import pytest
import sqlalchemy


def append(
        query_name="queryname",
        query=None,
        mutation=None,
        variables={}):
    with open("./queries.txt", "a", encoding="utf-8") as file:
        if (query is not None) and ("mutation" in query):
            json_data = {
                "query": None,
                "variables": variables,
                "mutation": query
            }
        else:
            json_data = {
                "query": query,
                "mutation": mutation,
                "variables": variables
            }
        rpattern = r"((?:[a-zA-Z]+Insert)|(?:[a-zA-Z]+Update)|(?:[a-zA-Z]+ById)|(?:[a-zA-Z]+Page))"
        qstring = query if query else mutation
        query_names = re.findall(rpattern, qstring)
        print(query_names)
        query_name = query_name if len(query_names) < 1 else "query_" + query_names[0]
        if json_data.get("query", None) is None:
            query_name = query_name.replace("query", "mutation")
        query_name = query_name + f"_{query.__hash__()}"
        query_name = query_name.replace("-", "")
        line = f'"{query_name}": {json.dumps(json_data)}, \n'
        file.write(line)


def create_by_id_test(table_name, query_endpoint, attribute_names=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Env_GQLUG_ENDPOINT_URL_8124):
        def testResult(resp):
            print("response", resp)
            errors = resp.get("errors", None)
            assert errors is None

            respdata = resp.get("data", None)
            assert respdata is not None

            respdata = respdata[query_endpoint]
            assert respdata is not None

            for att in attribute_names:
                assert respdata[att] == f'{datarow[att]}'

        schemaExecutor = ClientExecutorDemo
        clientExecutor = SchemaExecutorDemo

        data = DemoData
        datarow = data[table_name][0]
        content = "{" + ", ".join(attribute_names) + "}"
        query = "query($id: UUID!){" f"{query_endpoint}(id: $id)" f"{content}" "}"

        variable_values = {"id": f'{datarow["id"]}'}

        # append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)
        logging.debug(f"query for {query} with {variable_values}")

        resp = await schemaExecutor(query, variable_values)
        testResult(resp)
        resp = await clientExecutor(query, variable_values)
        testResult(resp)

    return result_test


def create_page_test(table_name, query_endpoint, attribute_names=["id"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo):

        def testResult(resp):
            errors = resp.get("errors", None)
            assert errors is None
            respdata = resp.get("data", None)
            assert respdata is not None

            respdata = respdata.get(query_endpoint, None)
            assert respdata is not None
            datarows = data[table_name]

            for rowa, rowb in zip(respdata, datarows):
                for att in attribute_names:
                    assert rowa[att] == f'{rowb[att]}'

        schemaExecutor = SchemaExecutorDemo
        clientExecutor = ClientExecutorDemo

        data = DemoData

        content = "{" + ", ".join(attribute_names) + "}"
        query = "query{" f"{query_endpoint}" f"{content}" "}"

        # append(queryname=f"{queryEndpoint}_{tableName}", query=query)

        resp = await schemaExecutor(query)
        testResult(resp)
        resp = await clientExecutor(query)
        testResult(resp)

    return result_test


def create_resolve_reference_test(table_name: str, gqltype: str, attribute_names=["id"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context,
                          Env_GQLUG_ENDPOINT_URL_8124):
        def testResult(resp):
            print(resp)
            errors = resp.get("errors", None)
            assert errors is None, errors
            respdata = resp.get("data", None)
            assert respdata is not None

            logging.info(respdata)
            respdata = respdata.get('_entities', None)
            assert respdata is not None

            assert len(respdata) == 1
            respdata = respdata[0]

            assert respdata['id'] == rowid

        schemaExecutor = SchemaExecutorDemo
        clientExecutor = ClientExecutorDemo

        content = "{" + ", ".join(attribute_names) + "}"

        data = DemoData
        table = data[table_name]
        for row in table:
            rowid = f"{row['id']}"

            # query = (
            #     'query($id: UUID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' +
            #     ' }])' +
            #     '{' +
            #     f'...on {gqltype}' + content +
            #     '}' +
            #     '}')

            # variable_values = {"id": rowid}

            query = ("query($rep: [_Any!]!)" +
                     "{" +
                     "_entities(representations: $rep)" +
                     "{" +
                     f"    ...on {gqltype} {content}" +
                     "}" +
                     "}"
                     )

            variable_values = {"rep": [{"__typename": f"{gqltype}", "id": f"{rowid}"}]}

            logging.info(f"query representations {query} with {variable_values}")
            resp = await clientExecutor(query, {**variable_values})
            testResult(resp)
            resp = await schemaExecutor(query, {**variable_values})
            testResult(resp)

        # append(queryname=f"{gqltype}_representation", query=query)

    return result_test


def create_frontend_query(query="{}", variables={}, asserts=[]):
    @pytest.mark.asyncio
    async def test_frontend_query(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context,
                                  Env_GQLUG_ENDPOINT_URL_8124):
        logging.debug("createFrontendQuery")
        # async_session_maker = await prepare_in_memory_sqllite()
        # await prepare_demodata(async_session_maker)
        # context_value = createContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        # append(queryname=f"query", query=query, variables=variables)
        resp = await SchemaExecutorDemo(
            query=query,
            variable_values=variables
        )
        # resp = await schema.execute(
        #     query=query,
        #     variable_values=variables,
        #     context_value=context_value
        # )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        logging.info(f"query for \n{query} with \n{variables} got response: \n{respdata}")
        for a in asserts:
            a(respdata)

    return test_frontend_query


def create_update_query(query="{}", variables={}, table_name=""):
    @pytest.mark.asyncio
    async def test_update(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context,
                          Env_GQLUG_ENDPOINT_URL_8124):
        logging.debug("test_update")
        assert variables.get("id", None) is not None, "variables has not id"
        variables["id"] = uuid.UUID(f"{variables['id']}")
        assert "$lastchange: DateTime!" in query, "query must have parameter $lastchange: DateTime!"
        assert "lastchange: $lastchange" in query, "query must use lastchange: $lastchange"
        assert table_name != "", "missing table name"

        async_session_maker = SQLite

        print("variables['id']", variables, flush=True)
        statement = sqlalchemy.text(f"SELECT id, lastchange FROM {table_name} WHERE id=:id").bindparams(
            id=variables['id'])
        # statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
        print("statement", statement, flush=True)
        async with async_session_maker() as session:
            rows = await session.execute(statement)
            row = rows.first()

            print("row", row)
            id = row[0]
            lastchange = row[1]

            print(id, lastchange)

        variables["lastchange"] = lastchange
        variables["id"] = f'{variables["id"]}'
        context_value = Context
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        # append(queryname=f"query_{tableName}", mutation=query, variables=variables)
        resp = await SchemaExecutorDemo(
            query=query,
            variable_values=variables
        )
        # resp = await schema.execute(
        #     query=query,
        #     variable_values=variables,
        #     context_value=context_value
        # )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        assert respdata is not None, "GQL response is empty"
        print("respdata", respdata)
        keys = list(respdata.keys())
        assert len(keys) == 1, "expected update test has one result"
        key = keys[0]
        result = respdata.get(key, None)
        assert result is not None, f"{key} is None (test update) with {query}"
        entity = None
        for key, value in result.items():
            print(key, value, type(value))
            if isinstance(value, dict):
                entity = value
                break
        assert entity is not None, f"expected entity in response to {query}"

        for key, value in entity.items():
            if key in ["id", "lastchange"]:
                continue
            print("attribute check", type(key), f"[{key}] is {value} ?= {variables[key]}")
            assert value == variables[key], f"test on update failed {value} != {variables[key]}"

    return test_update


def create_delete_query(query="{}", variables={}, table_name=""):
    @pytest.mark.asyncio
    async def test_delete(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context,
                          Env_GQLUG_ENDPOINT_URL_8124):
        logging.debug("test_delete")
        assert variables.get("id", None) is not None, "variables has no id"
        variables["id"] = str(uuid.UUID(f"{variables['id']}"))
        assert table_name != "", "missing table name"

        async_session_maker = SQLite

        # Check if the record exists before deletion
        print("Checking record exists before deletion", flush=True)
        check_statement = sqlalchemy.text(f"SELECT id FROM {table_name} WHERE id=:id").bindparams(id=variables['id'])
        print("check_statement", check_statement, flush=True)
        async with async_session_maker() as session:
            await session.execute(check_statement)

        # Execute the delete mutation
        context_value = Context
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        resp = await SchemaExecutorDemo(
            query=query,
            variable_values=variables
        )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        assert respdata is not None, "GQL response is empty"
        print("respdata", respdata)
        keys = list(respdata.keys())
        assert len(keys) == 1, "expected delete test has one result"
        key = keys[0]
        result = respdata.get(key, None)
        assert result is not None, f"{key} is None (test delete) with {query}"

        # Check if the record exists after deletion
        print("Checking record does not exist after deletion", flush=True)
        check_statement_post = sqlalchemy.text(f"SELECT id FROM {table_name} WHERE id=:id").bindparams(id=variables['id'])
        async with async_session_maker() as session:
            check_result_post = await session.execute(check_statement_post)
            record_exists_after_delete = check_result_post.first() is not None
            assert not record_exists_after_delete, "Record still exists after delete"

    return test_delete