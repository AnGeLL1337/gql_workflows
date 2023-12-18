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
'''
test_reference_authorization = create_resolve_reference_test(table_name="awauthorizations",
                                                             gqltype="AuthorizationGQLModel")

test_query_authorizations_by_id = create_by_id_test(table_name="awauthorizations", query_endpoint="authorizationById",
                                                    attribute_names=["id"])
'''
test_query_authorization_page = create_page_test(table_name="awauthorizations", query_endpoint="authorizationPage",
                                                 attribute_names=["id"])

test_insert_authorization_group = create_frontend_query(
    query="""mutation($id: UUID!) {
        result: authorizationInsert(authorization: {id: $id}) {
            id
            msg
        }
    }""",
    variables={"id": "a854adb9-b29a-4062-95b3-cfd685071f00"},
    asserts=[]
)

