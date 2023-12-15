import pytest
from GraphTypeDefinitions import schema

from ..shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    create_context,
)

from ..gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query
)


@pytest.mark.asyncio
async def test_large_query_1():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formrequests']
    row = table[0]
    rowid = f"{row['id']}"
    query = 'query{requestById(id: "' + rowid + '''") { 
        id
        name
        lastchange
        histories {
            request { id }
            form {
                id
                name
                nameEn
                sections {
                    id
                    name
                    order
                    form { id }
                    parts {
                        id
                        name
                        items {
                            id
                            name
                        }
                    }
                }
                type {
                    id
                    name
                    nameEn
                    category {
                        id
                        name
                        nameEn
                    }
                }

            }
        }
    }}'''

    context_value = create_context(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    data = data['requestById']

    print(data, flush=True)

    assert resp.errors is None
    assert data['id'] == rowid
