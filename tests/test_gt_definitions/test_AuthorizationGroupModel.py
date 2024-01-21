from .gt_utils import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query,
    create_delete_query
)

test_reference_authorization_groups = create_resolve_reference_test(table_name="awauthorizationgroups",
                                                                   gqltype="AuthorizationGroupGQLModel")

test_query_authorization_groups_by_id = create_by_id_test(table_name="awauthorizationgroups",
                                                         query_endpoint="authorizationGroupById", attribute_names=["id"])
test_query_authorization_groups_page = create_page_test(table_name="awauthorizationgroups",
                                                      query_endpoint="authorizationGroupPage", attribute_names=["id"])

test_insert_authorization_group = create_frontend_query(
    query="""mutation($authorizationId: UUID!, $groupId: UUID!, $accesslevel: Int!) {
        result: authorizationGroupInsert(authorizationGroup: {authorizationId: $authorizationId, groupId: $groupId, 
        accesslevel: $accesslevel}) {
            id
            msg
            authorizationGroup {
                id
                accesslevel
                lastchange
                authorization{id}
                group{id}
            }
        }
    }""",
    variables={"authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16",
               "groupId": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", "accesslevel": 4},
    asserts=[]
)

test_update_authorization_group = create_update_query(
    query="""mutation($id: UUID!, $lastchange: DateTime!, $accesslevel: Int) {
        result: authorizationGroupUpdate(authorizationGroup: {id: $id, lastchange: $lastchange, 
        accesslevel: $accesslevel}) {
            id
            msg
            authorizationGroup {
                id
                accesslevel
                lastchange
            }
        }
    }""",
    variables={"id": "4390a9cc-4751-482c-932b-908f0354380e", "accesslevel": 2},
    table_name="awauthorizationgroups"
)

test_delete_authorization_group = create_delete_query(
    query="""mutation($id: UUID!) {
        result: authorizationGroupDelete(
        authorizationGroupId: {id: $id}) {
        id
        msg
    }
}""",
    variables={"id": "4390a9cc-4751-482c-932b-908f0354380e"},
    table_name="awauthorizationgroups"
)
