from .gt_utils import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
)

test_reference_authorization = create_resolve_reference_test(table_name="awauthorizations",
                                                             gqltype="AuthorizationGQLModel")

test_query_authorizations_by_id = create_by_id_test(table_name="awauthorizations", query_endpoint="authorizationById",
                                                    attribute_names=["id"])

test_query_authorization_page = create_page_test(table_name="awauthorizations", query_endpoint="authorizationPage",
                                                 attribute_names=["id"])

test_insert_authorization_group = create_frontend_query(
    query="""mutation($id: UUID!) {
        result: authorizationInsert(authorization: {id: $id}) {
            id
            msg
            authorization {
                id
                users{id}
                roleTypes{id}
                groups{id}
            }
        }
    }""",
    variables={"id": "a854adb9-b29a-4062-95b3-cfd685071f00"},
    asserts=[]
)

