# Queries

Page Queries:
```graphql
query AuthorizationPage {
  authorizationPage {
    id
    groups {
      id
    }
    roleTypes {
      id
    }
    users {
      id
    }
  }
}

query authorizationGroupPage {
  authorizationGroupPage {
    accesslevel
    authorization {
      id
    }
    changedby {
      id
    }
    created
    createdby {
      id
    }
    group {
      id
    }
    id
    lastchange
  }
}

query authorizationRoletypePage {
  authorizationRoletypePage {
    id
    lastchange
    accesslevel
    authorization {
      id
    }
    changedby {
      id
    }
    created
    createdby {
      id
    }
    group {
      id
    }
    roletype {
      id
    }
  }
}

query authorizationUserPage {
  authorizationUserPage {
    authorization {
      id
    }
    id
    lastchange
    accesslevel
    changedby {
      id
    }
    created
    createdby {
      id
    }
  }
}
```

By ID Queries:
```graphql
query authorizationGroupById {
  authorizationGroupById(id: "4390a9cc-4751-482c-932b-908f0354380e") {
    id
    accesslevel
    lastchange
  }
}

query AuthorizationById {
  authorizationById(id: "a854adb9-b29a-4062-95b3-cfd685071f16") {
    id
    groups {
      id
      accesslevel
    }
    roleTypes {
      id
      accesslevel
    }
    users {
      id
      accesslevel
    }
  }
}

query authorizationRoletypeById {
  authorizationRoletypeById(id: "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b0") {
    id
    lastchange
    accesslevel
    authorization {
      id
    }
    changedby {
      id
    }
    created
    createdby {
      id
    }
    roletype {
      id
    }
  }
}

query authorizationUserById {
  authorizationUserById(id: "16c92914-0f71-437d-ace3-9661abe4c6cd") {
    id
    lastchange
    accesslevel
    authorization {
      id
    }
    changedby {
      id
    }
    created
    createdby {
      id
    }
  }
}
```

Group Queries:
```graphql
mutation authorizationGroupInsert {
  authorizationGroupInsert(
    authorizationGroup: {authorizationId: "a854adb9-b29a-4062-95b3-cfd685071f16", groupId: "2d9dcd22-a4a2-11ed-b9df-0242ac120003", accesslevel: 5, id: "4390a9cc-4751-482c-932b-908f0354380f"}
  ) {
    id
    msg
    authorizationGroup {
      id
      lastchange
      accesslevel
    }
  }
}

mutation authorizationGroupUpdate {
  authorizationGroupUpdate(
    authorizationGroup: {lastchange: "2024-01-21T00:24:52.653712", id: "4390a9cc-4751-482c-932b-908f0354380f", accesslevel: 10}
  ) {
    id
    msg
    authorizationGroup {
      id
      accesslevel
      lastchange
    }
  }
}

mutation authorizationGroupDelete {
  authorizationGroupDelete(
    authorizationGroupId: {id: "4390a9cc-4751-482c-932b-908f0354380f"}) {
    id
    msg
  }
}
```

RoleType Queries:
```graphql
mutation authorizationRoletypeInsert {
  authorizationRoletypeInsert(
    authorizationRoletype: {authorizationId: "a854adb9-b29a-4062-95b3-cfd685071f16", groupId: "2d9dcd22-a4a2-11ed-b9df-0242ac120003", roletypeId: "05a3e0f5-f71e-4caa-8012-229d868aa8ca", accesslevel: 5, id: "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b1"}
  ) {
    id
    msg
    authorizationRoletype {
      id
      lastchange
      accesslevel
    }
  }
}

mutation authorizationRoletypeUpdate {
  authorizationRoletypeUpdate(
    authorizationRoletype: {lastchange: "2024-01-21T00:32:15.027645", id: "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b1", accesslevel: 10}
  ) {
    id
    msg
    authorizationRoletype {
      id
      lastchange
      accesslevel
    }
  }
}

mutation authorizationRoletypeDelete {
  authorizationRoletypeDelete(authorizationRoletypeId: {id: "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b1"}) {
    id
    msg
  }
}
```

User Queries:
```graphql
mutation authorizationUserInsert {
  authorizationUserInsert(
    authorizationUser: {authorizationId: "a854adb9-b29a-4062-95b3-cfd685071f16", userId: "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", accesslevel: 5, id: "16c92914-0f71-437d-ace3-9661abe4c6ce"}
  ) {
    id
    msg
    authorizationUser {
      id
      lastchange
      accesslevel
    }
  }
}

mutation authorizationUserUpdate {
  authorizationUserUpdate(
    authorizationUser: {lastchange: "2024-01-21T00:29:04.984821", id: "16c92914-0f71-437d-ace3-9661abe4c6ce", accesslevel: 10}
  ) {
    id
    msg
    authorizationUser {
      id
      lastchange
      accesslevel
    }
  }
}

mutation authorizationUserDelete {
  authorizationUserDelete(authorizationUserId: {id: "16c92914-0f71-437d-ace3-9661abe4c6ce"}) {
    id
    msg
  }
}
```