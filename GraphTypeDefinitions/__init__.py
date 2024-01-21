import uuid
from typing import Union

import strawberry

from .authorizationGQLModel import AuthorizationGQLModel
from .authorizationGroupGQLModel import AuthorizationGroupGQLModel
from .authorizationRoleTypeGQLModel import AuthorizationRoleTypeGQLModel
from .authorizationUserGQLModel import AuthorizationUserGQLModel

from .externals import UserGQLModel
######################################################################################################################


@strawberry.type(description="""Root query type""")
class Query:

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

    from .authorizationGQLModel import (
        authorization_insert,
    )
    authorization_insert = authorization_insert

    from .authorizationUserGQLModel import (
        authorization_user_insert,
        authorization_user_update,
        authorization_user_delete
    )
    authorization_user_insert = authorization_user_insert
    authorization_user_update = authorization_user_update
    authorization_user_delete = authorization_user_delete

    from .authorizationRoleTypeGQLModel import (
        authorization_roletype_insert,
        authorization_roletype_update,
        authorization_roletype_delete
    )
    authorization_roletype_insert = authorization_roletype_insert
    authorization_roletype_update = authorization_roletype_update
    authorization_roletype_delete = authorization_roletype_delete

    from .authorizationGroupGQLModel import (
        authorization_group_insert,
        authorization_group_update,
        authorization_group_delete
    )
    authorization_group_insert = authorization_group_insert
    authorization_group_update = authorization_group_update
    authorization_group_delete = authorization_group_delete


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

schema = strawberry.federation.Schema(Query, types=(UserGQLModel, ),
                                      mutation=Mutation)
