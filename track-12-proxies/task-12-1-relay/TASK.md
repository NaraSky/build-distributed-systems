# Implement Basic Relay Proxy

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-1-relay>

Track: 12. Proxies
Task order: 1
Short title: Relay Proxy
Difficulty: beginner
Subtrack: Caching Proxy

## Problem

Build a basic relay proxy that forwards requests to a backend server:

1. Listen for incoming client requests
2. Parse the request to determine backend destination
3. Forward the request to the backend
4. Wait for the backend response
5. Return the response to the client

Handle connection errors and timeouts gracefully.

## Concept Notes

### What is a Proxy?

A proxy sits between clients and servers, intercepting and forwarding requests. Proxies can add functionality like caching, load balancing, security, and logging without modifying client or server code.

### Forward vs Reverse Proxy

A forward proxy acts on behalf of clients (e.g., corporate firewall). A reverse proxy acts on behalf of servers (e.g., NGINX in front of application servers). We will build a reverse proxy.

## Concepts

- proxy
- forwarding
- request handling

## Hints

- Accept incoming requests
- Forward to backend server
- Return response to client

## Test Cases

### 1. Forward request

Proxy forwards GET /api/data to backend and returns response to client

Input:

```json
{"src":"c0","dest":"proxy","body":{"type":"init","msg_id":1,"node_id":"proxy","node_ids":["proxy","backend"]}}
{"src":"client","dest":"proxy","body":{"type":"relay_request","msg_id":2,"path":"/api/data","method":"GET"}}
```

Expected output:

```text
{"src":"proxy","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"proxy","dest":"client","body":{"type":"relay_response","in_reply_to":2,"msg_id":1,"status":200,"path":"/api/data"}}
```

## Resources

- [Proxy Patterns](https://en.wikipedia.org/wiki/Proxy_pattern): Overview of proxy design patterns

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
