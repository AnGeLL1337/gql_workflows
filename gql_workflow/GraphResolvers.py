from uoishelpers.resolvers import (
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
)

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

from DBDefinitions import WorkflowModel, AuthorizationModel

## workflow resolvers
resolveWorkflowsPaged = createEntityGetter(WorkflowModel)
resolveWorkflowById = createEntityByIdGetter(WorkflowModel)
resolveInsertWorkflow = createInsertResolver(WorkflowModel)

## authorization resolvers
resolveAuthorizationsPaged = createEntityGetter(AuthorizationModel)
resolveAuthorizationById = createEntityByIdGetter(AuthorizationModel)
resolveInsertAuthorization = createInsertResolver(AuthorizationModel)
