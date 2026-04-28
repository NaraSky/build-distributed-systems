# Implement API Versioning

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-1-api-versioning>

Track: 27. The Migrator
Task order: 6
Short title: API Versioning
Difficulty: intermediate
Subtrack: Protocol and API Evolution

## Problem

API versioning lets you evolve your API without breaking existing clients. You support multiple versions simultaneously, warn clients on deprecated ones with `Deprecation` and `Sunset` headers, and eventually stop serving a version after its sunset date with HTTP 410.

Implement a node that routes and manages API versions:

```json
// Route to the correct version handler
{ "type": "get_users", "msg_id": 1, "version": "v2" }
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v2",
    "users": [{"id":1,"email":"user@example.com","full_name":"John Doe"}] }

// Deprecated version: add warning headers
{ "type": "get_users", "msg_id": 2, "version": "v1", "deprecated": true }
-> { "type": "users_response", "in_reply_to": 2,
    "version": "v1",
    "headers": {"Deprecation":"true","Sunset":"2024-12-31"} }

// Version negotiation via Accept header
{ "type": "get_users", "msg_id": 3 }
headers: { "Accept": "application/vnd.myapi.v2+json" }
-> { "type": "users_response", "in_reply_to": 3,
    "version": "v2", "content_type": "application/vnd.myapi.v2+json" }

// Sunset version returns 410 Gone
{ "type": "get_users", "msg_id": 4, "version": "v1", "sunset": true }
-> { "type": "error", "in_reply_to": 4, "status": 410,
    "error": "API version v1.0 has been sunset",
    "current_version": "v2.0" }
```

## Concepts

- API versioning
- URL versioning
- deprecation headers
- content negotiation
- sunset

## Hints

- Route requests by version field or Accept header to the correct handler
- Deprecation header: Deprecation: true plus Sunset: <date> on v1 responses
- Content negotiation: parse version from Accept: application/vnd.myapi.v2+json
- Sunset (410 Gone): once the sunset date passes, reject requests with HTTP 410
- Never remove a version without a sunset date announced in advance

## Test Cases

### 1. Route to correct API version

Should route to v2 handler which returns full_name field.

Input:

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"version":"v2"}}
```

Expected output:

```text
{"type": "users_response", "in_reply_to": 1, "version": "v2", "users": [{"id": 1, "email": "user@example.com", "full_name": "John Doe"}]}
```

### 2. Deprecation headers

Deprecated version should include Deprecation and Sunset headers.

Input:

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"version":"v1","deprecated":true}}
```

Expected output:

```text
{"type": "users_response", "in_reply_to": 1, "version": "v1", "headers": {"Deprecation": "true", "Sunset": "2024-12-31"}}
```

## Resources

- [API Versioning Strategies](https://restfulapi.net/versioning/): URL versioning, header versioning, and media type versioning compared
- [Semantic Versioning](https://semver.org/): Semantic Versioning specification

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
