import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .authorizationGQLModel import authorization_by_id
    authorization_by_id = authorization_by_id

    from .authorizationGQLModel import authorization_page
    authorization_page = authorization_page

    from .authorizationGroupGQLModel import authorization_group_by_id
    authorization_group_by_id = authorization_group_by_id

    from .authorizationGroupGQLModel import authorization_group_page
    authorization_group_page = authorization_group_page

    from .authorizationUserGQLModel import authorization_user_by_id
    authorization_user_by_id = authorization_user_by_id

    from .authorizationUserGQLModel import authorization_user_page
    authorization_user_page = authorization_user_page
    
    from .authorizationRoleTypeGQLModel import authorization_roletype_by_id
    authorization_roletype_by_id = authorization_roletype_by_id

    from .authorizationRoleTypeGQLModel import authorization_roletype_page
    authorization_roletype_page = authorization_roletype_page

    from .workflowGQLModel import workflow_by_id
    workflow_by_id = workflow_by_id

    from .workflowGQLModel import workflow_page
    workflow_page = workflow_page
    
