# Queries

**AuthorizationPage:**
```graphql
query AuthorizationPage {
  authorizationPage {
    id
    roleTypes {
      id
      accesslevel
      created
      authorization {
        id
      }
    }
    users {
      id
      accesslevel
      created
      lastchange
    }
    groups {
      id
      accesslevel
      created
      lastchange
    }
  }
}
```
**AuthorizationGroupPage:**
```graphql
query authorizationGroupPage {
  authorizationGroupPage {
    accesslevel
    created
    id
    lastchange
    authorization {
      id
    }
    group {
      id
    }
  }
}
```
**AuthorizationRoletypePage:**
```graphql
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
```
**AuthorizationUserPage:**
```graphql
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

**AuthorizationGroupById:**
```graphql
query authorizationGroupById($groupId: UUID!) {
  authorizationGroupById(id: $groupId) {
    id
    accesslevel
    lastchange
  }
}, 
variables={"groupId": "4390a9cc-4751-482c-932b-908f0354380e"}
```

**AuthorizationById:**
```graphql
query AuthorizationById($authorizationId: UUID!) {
  authorizationById(id: $authorizationId) {
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
},
variables={"authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16"}
```

**AuthorizationRoletypeById:**
```graphql
query authorizationRoletypeById($roletypeId: UUID!) {
  authorizationRoletypeById(id: $roletypeId) {
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
},
variables={"roletypeId": "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b0"}
```

**AuthorizationUserById:**
```graphql
query authorizationUserById($userId: UUID!) {
  authorizationUserById(id: $userId) {
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
},
variables={"userId": "16c92914-0f71-437d-ace3-9661abe4c6cd"}
```

**AuthorizationGroupInsert:**
```graphql
mutation authorizationGroupInsert($authorizationId: UUID!, $groupId: UUID!, $accesslevel: Int!, $id: UUID) {
  authorizationGroupInsert(
    authorizationGroup: {authorizationId: $authorizationId, groupId: $groupId, accesslevel: $accesslevel, id: $id}
  ) {
    id
    msg
    authorizationGroup {
      id
      lastchange
      accesslevel
    }
  }
},
variables={
    "authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16",
    "groupId": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
    "accesslevel": 5,
    "id": "4390a9cc-4751-482c-932b-908f0354380f"
}
```

**AuthorizationGroupUpdate:**
```graphql
mutation authorizationGroupUpdate($lastchange: DateTime!, $id: UUID!, $accesslevel: Int) {
  authorizationGroupUpdate(
    authorizationGroup: {lastchange: $lastchange, id: $id, accesslevel: $accesslevel}
  ) {
    id
    msg
    authorizationGroup {
      id
      accesslevel
      lastchange
    }
  }
},
variables={
    "lastchange": "2024-01-21T00:32:15.027645",
    "id": "4390a9cc-4751-482c-932b-908f0354380f",
    "accesslevel": 10
}
```

**AuthorizationGroupDelete:**
```graphql
mutation authorizationGroupDelete($id: UUID!) {
  authorizationGroupDelete(
    authorizationGroupId: {id: $id}) {
    id
    msg
  }
},
variables={"id": "4390a9cc-4751-482c-932b-908f0354380f"}
```

**AuthorizationRoletypeInsert**:
```graphql
mutation authorizationRoletypeInsert($authorizationId: UUID!, $groupId: UUID!, $roletypeId: UUID!, $accesslevel: Int!, $id: UUID) {
  authorizationRoletypeInsert(
    authorizationRoletype: {authorizationId: $authorizationId, groupId: $groupId, roletypeId: $roletypeId, accesslevel: $accesslevel, id: $id}
  ) {
    id
    msg
    authorizationRoletype {
      id
      lastchange
      accesslevel
    }
  }
},
variables={
    "authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16",
    "groupId": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
    "roletypeId": "05a3e0f5-f71e-4caa-8012-229d868aa8ca",
    "accesslevel": 5,
    "id": "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b1"
}
```

**AuthorizationRoletypeUpdate**:
```graphql
mutation authorizationRoletypeUpdate($lastchange: DateTime!, $id: UUID!, $accesslevel: Int) {
  authorizationRoletypeUpdate(
    authorizationRoletype: {lastchange: $lastchange, id: $id, accesslevel: $accesslevel}
  ) {
    id
    msg
    authorizationRoletype {
      id
      lastchange
      accesslevel
    }
  }
},
variables={
    "lastchange": "2024-02-08T20:10:43.519105",
    "id": "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b1",
    "accesslevel": 10
}
```

**AuthorizationRoletypeDelete**:
```graphql
mutation authorizationRoletypeDelete($id: UUID!) {
  authorizationRoletypeDelete(authorizationRoletypeId: {id: $id}) {
    id
    msg
  }
},
variables={"id": "1125f3ed-cf55-4a57-9eb7-7e8f1447b9b1"}
```

**authorizationUserInsert**:
```graphql
mutation authorizationUserInsert($authorizationId: UUID!, $userId: UUID!, $accesslevel: Int!, $id: UUID) {
  authorizationUserInsert(
    authorizationUser: {authorizationId: $authorizationId, userId: $userId, accesslevel: $accesslevel, id: $id}
  ) {
    id
    msg
    authorizationUser {
      id
      lastchange
      accesslevel
    }
  }
},
variables={
  "authorizationId": "a854adb9-b29a-4062-95b3-cfd685071f16",
  "userId": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
  "accesslevel": 5,
  "id": "16c92914-0f71-437d-ace3-9661abe4c6ce"
}
```

**authorizationUserUpdate**:
```graphql
mutation authorizationUserUpdate($lastchange: DateTime!, $id: UUID!, $accesslevel: Int) {
  authorizationUserUpdate(
    authorizationUser: {lastchange: $lastchange, id: $id, accesslevel: $accesslevel}
  ) {
    id
    msg
    authorizationUser {
      id
      lastchange
      accesslevel
    }
  }
},
variables={
  "lastchange": "2024-02-08T19:56:24.132917",
  "id": "16c92914-0f71-437d-ace3-9661abe4c6ce",
  "accesslevel": 10
}
```

**authorizationUserDelete**:
```graphql
mutation authorizationUserDelete($id: UUID!) {
  authorizationUserDelete(authorizationUserId: {id: $id}) {
    id
    msg
  }
},
variables={"id": "16c92914-0f71-437d-ace3-9661abe4c6ce"}
```