import strawberry

@strawberry.type
class Mutation:
    from .authorizationGQLModel import authorization_insert
    authorization_insert = authorization_insert

    from .authorizationGroupGQLModel import authorization_add_group
    authorization_add_group = authorization_add_group

    from .authorizationGroupGQLModel import authorization_update_group
    authorization_update_group = authorization_update_group

    from .authorizationGroupGQLModel import authorization_remove_group
    authorization_remove_group = authorization_remove_group

    from .authorizationRoleTypeGQLModel import authorization_add_role
    authorization_add_role = authorization_add_role

    from .authorizationRoleTypeGQLModel import authorization_remove_role
    authorization_remove_role = authorization_remove_role

    from .authorizationUserGQLModel import authorization_add_user
    authorization_add_user = authorization_add_user

    from .authorizationUserGQLModel import authorization_remove_user
    authorization_remove_user = authorization_remove_user


