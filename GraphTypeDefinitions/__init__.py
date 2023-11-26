import uuid
from typing import Union

import strawberry

from .authorizationGQLModel import AuthorizationGQLModel
from .authorizationGroupGQLModel import AuthorizationGroupGQLModel
from .authorizationRoleTypeGQLModel import AuthorizationRoleTypeGQLModel
from .authorizationUserGQLModel import AuthorizationUserGQLModel


@strawberry.type(description="""Root query type""")
class Query:
    @strawberry.field(description="""Say hello to the world""")
    async def say_hello_authorizations(
            self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    from .authorizationGQLModel import (
        authorization_by_id,
        authorization_page
    )
    authorization_by_id = authorization_by_id
    authorization_page = authorization_page

    from .authorizationGroupGQLModel import (
        authorization_group_by_id,
        authorization_group_page
    )
    authorization_group_by_id = authorization_group_by_id
    authorization_group_page = authorization_group_page

    from .authorizationUserGQLModel import (
        authorization_user_by_id,
        authorization_user_page
    )
    authorization_user_by_id = authorization_user_by_id
    authorization_user_page = authorization_user_page

    from .authorizationRoleTypeGQLModel import (
        authorization_roletype_by_id,
        authorization_roletype_page
    )
    authorization_roletype_by_id = authorization_roletype_by_id
    authorization_roletype_page = authorization_roletype_page

######################################################################################################################
#
#
# Mutations
#
#
######################################################################################################################

@strawberry.type(description="""Root mutation type""")
class Mutation:

    from .authorizationUserGQLModel import (
        authorization_user_insert,
        authorization_user_update
    )
    authorization_user_insert = authorization_user_insert
    authorization_user_update = authorization_user_update

    from .authorizationRoleTypeGQLModel import (
        authorization_roletype_insert,
        authorization_roletype_update
    )
    authorization_roletype_insert = authorization_roletype_insert
    authorization_roletype_update = authorization_roletype_update

'''
    from .authorizationUserGQLModel import authorization_add_user
    authorization_add_user = authorization_add_user

    from .authorizationUserGQLModel import authorization_remove_user
    authorization_remove_user = authorization_remove_user
    
    from .workflowGQLModel import workflow_insert
    workflow_insert = workflow_insert

    from .workflowGQLModel import workflow_update
    workflow_update = workflow_update

    from .workflowStateGQLModel import workflow_state_insert
    workflow_state_insert = workflow_state_insert

    from .workflowStateGQLModel import workflow_state_update
    workflow_state_update = workflow_state_update

    # from .WorkflowStateRoleTypeGQLModel import *

    from .workflowTransitionGQLModel import workflow_transition_insert
    workflow_transition_insert = workflow_transition_insert

    from .workflowTransitionGQLModel import workflow_transition_update
    workflow_transition_update = workflow_transition_update

    # from .WorkflowStateUserGQLModel import *
    from .workflowStateUserGQLModel import workflow_state_add_user
    workflow_state_add_user = workflow_state_add_user

    from .workflowStateUserGQLModel import workflow_state_remove_user
    workflow_state_remove_user = workflow_state_remove_user

    from .workflowStateRoleTypeGQLModel import workflow_state_add_role
    workflow_state_add_role = workflow_state_add_role

    from .workflowStateRoleTypeGQLModel import workflow_state_remove_role
    workflow_state_remove_role = workflow_state_remove_role
'''

schema = strawberry.federation.Schema(Query, types=[
    AuthorizationGQLModel, AuthorizationGroupGQLModel, AuthorizationRoleTypeGQLModel, AuthorizationUserGQLModel],
                                      mutation=Mutation)