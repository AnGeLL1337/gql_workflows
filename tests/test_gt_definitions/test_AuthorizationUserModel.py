import pytest
from GraphTypeDefinitions import schema


from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    create_context,
)

from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query
)

test_reference_authorization_users = create_resolve_reference_test(table_name="awauthorizationusers",
                                                                   gqltype="AuthorizationUserGQLModel")

test_query_authorization_users_by_id = create_by_id_test(table_name="awauthorizationusers",
                                                         query_endpoint="authorizationUserById", attribute_names=["id"])
test_query_authorization_user_page = create_page_test(table_name="awauthorizationusers",
                                                      query_endpoint="authorizationUserPage", attribute_names=["id"])

test_insert_authorization_user = create_frontend_query(
    query="""mutation($authorizationId: UUID!, $userId: UUID!, $accesslevel: Int!) {
        result: authorizationUserInsert(authorizationUser: {authorizationId: $authorizationId, userId: $userId, 
        accesslevel: $accesslevel}) {
            id
            msg
            authorizationUser {
                id
                accesslevel
                lastchange
            }
        }
    }""",
    variables={"authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16",
               "userId": "2d9dc5ca-a4a2-11ed-b9df-0242ac120001", "accesslevel": 4},
    asserts=[]
)

test_update_authorization_user = create_update_query(
    query="""mutation($id: UUID!, $lastchange: DateTime!, $accesslevel: Int) {
        result: authorizationUserUpdate(authorizationUser: {id: $id, lastchange: $lastchange, 
        accesslevel: $accesslevel}) {
            id
            msg
            authorizationUser {
                id
                accesslevel
                lastchange
            }
        }
    }""",
    variables={"id": "16c92914-0f71-437d-ace3-9661abe4c6cd", "accesslevel": 6},
    table_name="awauthorizationusers"
)

