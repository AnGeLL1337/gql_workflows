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

test_reference_authorization_roletypes = create_resolve_reference_test(table_name="awauthorizationroletypes",
                                                                   gqltype="AuthorizationRoleTypeGQLModel")

test_query_authorization_roletypes_by_id = create_by_id_test(table_name="awauthorizationroletypes",
                                                         query_endpoint="authorizationRoletypeById", attribute_names=["id"])
test_query_authorization_roletypes_page = create_page_test(table_name="awauthorizationroletypes",
                                                      query_endpoint="authorizationRoletypePage", attribute_names=["id"])

test_insert_authorization_roletype = create_frontend_query(
    query="""mutation($authorizationId: UUID!, $groupId: UUID!, $roletypeId: UUID!, $accesslevel: Int!) {
        result: authorizationRoletypeInsert(authorizationRoletype: {authorizationId: $authorizationId, 
        groupId: $groupId, roletypeId: $roletypeId, accesslevel: $accesslevel}) {
            id
            msg
            authorizationRoletype {
                id
                accesslevel
                lastchange
            }
        }
    }""",
    variables={"authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16",
               "groupId": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
               "roletypeId": "05a3e0f5-f71e-4caa-8012-229d868aa8ca", "accesslevel": 2},
    asserts=[]
)

test_update_authorization_roletype = create_update_query(
    query="""mutation($id: UUID!, $lastchange: DateTime!, $accesslevel: Int) {
        result: authorizationRoletypeUpdate(authorizationRoletype: {id: $id, lastchange: $lastchange, 
        accesslevel: $accesslevel}) {
            id
            msg
            authorizationRoletype {
                id
                accesslevel
                lastchange
            }
        }
    }""",
    variables={"id": "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b0", "accesslevel": 6},
    table_name="awauthorizationroletypes"
)

