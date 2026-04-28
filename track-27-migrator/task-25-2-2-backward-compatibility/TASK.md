# Implement Backward-Compatible API Changes

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-2-backward-compatibility>

Track: 27. The Migrator
Task order: 7
Short title: Backward Compatibility
Difficulty: intermediate
Subtrack: Protocol and API Evolution

## Problem

Backward compatibility means old clients continue to work after an API update. The golden rule: only make **additive** changes (new optional fields, new endpoints). Renaming, removing, or changing the type of existing fields breaks old clients.

Implement a node that serves both old and new clients from the same endpoint:

```json
// v1 client: gets the fields it knows about (no new fields needed)
{ "type": "get_users", "msg_id": 1 }  // from client_v1
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v1",
    "users": [{"id":1,"email":"user@example.com","name":"John Doe"}] }

// v2 client: gets new fields added in v2
{ "type": "get_users", "msg_id": 2 }  // from client_v2
-> { "type": "users_response", "in_reply_to": 2,
    "version": "v2",
    "users": [{"id":1,"email":"user@example.com",
               "full_name":"John Doe","phone":"+1234567890"}] }

// Deprecated field: return both old and new, flag old as deprecated
{ "type": "create_user", "msg_id": 3,
  "user": {"email":"new@example.com","name":"Jane"} }
-> { "type": "user_created", "in_reply_to": 3,
    "user": {"id":2,"full_name":"Jane"},
    "__deprecated": ["name"] }
```

## Concepts

- backward compatibility
- additive changes
- field deprecation
- consumer-driven contracts

## Hints

- Old clients must work without modification when new optional fields are added
- New clients receive the new fields; old clients ignore them
- Deprecated fields: return the old field alongside the new one, flag it in __deprecated
- Contract validation: ensure API response matches the expected contract version
- Never remove or rename required fields — add new optional ones instead

## Test Cases

### 1. Add optional field (backward compatible)

Old client should receive only the fields it knows about.

Input:

```json
{"src":"client_v1","dest":"api","body":{"type":"get_users","msg_id":1}}
```

Expected output:

```text
{"type": "users_response", "in_reply_to": 1, "users": [{"id": 1, "email": "user@example.com", "name": "John Doe"}], "version": "v1"}
```

### 2. New client uses new fields

New client should receive full_name and phone added in v2.

Input:

```json
{"src":"client_v2","dest":"api","body":{"type":"get_users","msg_id":1}}
```

Expected output:

```text
{"type": "users_response", "in_reply_to": 1, "users": [{"id": 1, "email": "user@example.com", "full_name": "John Doe", "phone": "+1234567890"}], "version": "v2"}
```

## Resources

- [Consumer-Driven Contracts](https://martinfowler.com/articles/consumerDrivenContracts.html): Testing backward compatibility with consumer-driven contract tests
- [OpenAPI Specification](https://swagger.io/specification/): OpenAPI/Swagger specification

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
