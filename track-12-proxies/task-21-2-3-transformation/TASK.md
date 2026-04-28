# Implement Request/Response Transformation

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-3-transformation>

Track: 12. Proxies
Task order: 8
Short title: Request/Response Transformation
Difficulty: intermediate
Subtrack: API Gateway

## Problem

API gateways transform requests and responses to bridge the gap between client expectations and backend implementations. This enables legacy integration and protocol translation.

**Transformation types**:
```
1. Format transformation:
   Client (JSON) → Gateway → Backend (XML)

2. Protocol translation:
   Client (REST) → Gateway → Backend (gRPC)

3. Field mapping:
   Client (userId) → Gateway → Backend (user_id)

4. Aggregation:
   Client → Gateway → [Backend A, Backend B] → Gateway → Client
```

**Example: JSON to XML transformation**:
```json
// Client sends JSON:
Request:  {"type": "api_request", "msg_id": 1, "method": "POST", "path": "/api/users", "headers": {"Content-Type": "application/json"}, "body": {"name": "Alice", "email": "alice@example.com"}}

// Gateway transforms to XML and sends to backend:
Backend Request:  {"method": "POST", "path": "/users", "headers": {"Content-Type": "application/xml"}, "body": "<?xml version="1.0"?><user><name>Alice</name><email>alice@example.com</email></user>"}

// Backend responds with XML:
Backend Response:  {"status": 201, "body": "<?xml version="1.0"?><user><id>123</id><name>Alice</name><email>alice@example.com</email></user>"}

// Gateway transforms to JSON and sends to client:
Response: {"type": "api_response", "in_reply_to": 1, "status": 201, "body": {"id": 123, "name": "Alice", "email": "alice@example.com"}}
```

**Field mapping configuration**:
```json
{
  "transformations": {
    "/api/users": {
      "request": {
        "field_mappings": {
          "userId": "user_id",
          "firstName": "first_name",
          "lastName": "last_name"
        },
        "format": "json_to_xml"
      },
      "response": {
        "field_mappings": {
          "user_id": "userId",
          "first_name": "firstName",
          "last_name": "lastName"
        },
        "format": "xml_to_json"
      }
    }
  }
}
```

## Concepts

- request transformation
- response transformation
- protocol translation
- format conversion
- legacy integration

## Hints

- Transform request format before sending to backend (e.g., JSON → XML)
- Transform response format before returning to client (e.g., XML → JSON)
- Protocol translation: REST → gRPC, GraphQL → REST
- Legacy integration: modern JSON clients → legacy XML backends
- Field mapping: rename fields between client and backend schemas

## Test Cases

### 1. JSON to XML transformation

Gateway should transform JSON request to XML before sending to backend.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"transformations":{"/api/users":{"request":{"format":"json_to_xml"},"response":{"format":"xml_to_json"}}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"POST","path":"/api/users","body":{"name":"Alice"}}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Field mapping

Gateway should map userId→user_id in request, user_id→userId in response.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"POST","path":"/api/users","body":{"userId":"user123","firstName":"Alice"}}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "body": {"userId": "user123", "firstName": "Alice"}}}
```

## Resources

- [API Gateway Transformation](https://aws.amazon.com/api-gateway/): AWS API Gateway documentation on request/response transformation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
