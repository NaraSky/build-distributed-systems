# Implement Sticky Sessions

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-3-sticky-sessions>

Track: 14. Load Balancers
Task order: 8
Short title: Sticky Sessions
Difficulty: intermediate
Subtrack: Layer 7 Load Balancing

## Problem

Sticky sessions (session affinity) ensure that all requests from a client are routed to the same backend server, essential for stateful services.

**Why sticky sessions?**: Problem occurs when client logs in on backend-1 and session is stored in backend-1 memory. Request 1: GET /login → backend-1 (session created). Request 2: GET /profile → backend-2 (session not found) - this fails. Solution with sticky sessions: Request 2: GET /profile with Cookie: session_id=abc123 → backend-1 (session found) - this works.

**Session mapping implementation**: Maintain Map of session_id to backend. Extract session_id from request cookies. If session_id exists in map, route to known backend for this session. If no session or unknown session, use load balancing to select backend. Store mapping of session_id to selected backend. Set cookie so future requests use this backend.

**Cookie-based routing**: Load balancer reads session_id from request cookie. Looks up backend assigned to this session. Routes request to that backend. If no cookie or unknown session, selects backend using load balancing algorithm (round-robin, least connections, etc.). Sets response cookie with session_id and backend identifier. Client includes this cookie in all subsequent requests.

**Example sticky session flow**: First request (no session cookie): Client sends GET /api/profile without session cookie. Load balancer selects backend-1 using round-robin. Creates session ID abc123. Stores mapping abc123 → backend-1. Returns response with Set-Cookie: session_id=abc123; backend=backend-1. Second request (with session cookie): Client sends GET /api/profile with Cookie: session_id=abc123. Load balancer looks up abc123 in session map. Finds backend-1. Routes request to backend-1. Session data found, request succeeds.

**Handling backend failures**: When backend fails, detect which backends are healthy. For sessions assigned to failed backend, reassign to new healthy backend. Update session mapping with new backend. Update cookie with new backend identifier. This ensures session continuity even during failures. Monitor backend health using health checks. Remove failed backends from rotation until recovery.

**Load balancing integration**: Sticky sessions work with any load balancing algorithm. For new sessions (no cookie), use configured algorithm (round-robin, least connections, IP hash, etc.). For existing sessions (with cookie), override load balancing and use assigned backend. This balances new session distribution while maintaining session affinity.

**Session expiration and cleanup**: Sessions expire after configured timeout (e.g., 30 minutes of inactivity). Clean up expired session mappings to free memory. Track last activity time for each session. Remove sessions when expired or on explicit logout. This prevents unbounded growth of session table.

**Implementation considerations**: Use consistent hashing for backend selection to minimize reassignments on backend changes. Store session mapping in distributed cache for load balancer scalability. Handle cookie theft and session hijacking with security measures (HTTPS, secure cookies, same-site attribute). Support session draining for graceful backend shutdown.

**Stateful service requirements**: Sticky sessions essential for services maintaining in-memory session state (user authentication, shopping carts, multi-step workflows). Alternative approaches include session replication across backends (complex, eventual consistency issues) or external session storage like Redis (adds dependency, network latency). Sticky sessions provide simple solution for many use cases.

**Monitoring and metrics**: Track session count per backend. Monitor session affinity violations (requests routed to wrong backend). Measure session lifecycle (creation, expiration, reassignment). Alert on uneven session distribution. Monitor backend health and session reassignment rate.

## Concepts

- sticky sessions
- session affinity
- cookie-based routing
- session persistence
- stateful services

## Hints

- Extract session_id from request cookies
- Maintain a mapping: session_id → backend
- If session_id exists, route to the same backend
- If no session_id, use normal load balancing and set the cookie
- Handle backend failures: re-assign session to new backend

## Test Cases

### 1. First request creates session

First request should return a Set-Cookie header with session_id and backend.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/profile","cookies":{}}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "set_cookie": "session_id=.*; backend=api-1"}}
```

### 2. Subsequent requests use same backend

Request with session_id=abc123 should route to the same backend (api-1).

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/profile","cookies":{"session_id":"abc123"}}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1"}}
```

## Resources

- [Sticky Sessions](https://www.nginx.com/blog/nginx-sticky-sessions-learning-presence/): NGINX blog on sticky session implementations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
