# Implement Consistent Hashing for Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-4-consistent-hashing-lb>

Track: 14. Load Balancers
Task order: 14
Short title: Consistent Hashing LB
Difficulty: advanced
Subtrack: Advanced Balancing Algorithms

## Problem

Consistent hashing for load balancing ensures that the same client always routes to the same backend. This is useful for caching layers where session state or cache locality matters.

**Why consistent hashing for LB?**
```
Problem: modulo hashing routes change when backends change
  client_1 → hash("client_1") % 3 = backend-1
  client_2 → hash("client_2") % 3 = backend-2

  Add backend-4:
  client_1 → hash("client_1") % 4 = backend-3 ❌ Different!
  All clients remap = cache cold miss

Solution: consistent hashing
  client_1 → hash ring → backend-1
  client_2 → hash ring → backend-2

  Add backend-4:
  client_1 → hash ring → backend-1 ✓ Same!
  Only 25% of clients remap
```

**Algorithm**:
```typescript
function routeClient(clientId: string, backends: Backend[]): string {
  // Hash client ID to point on ring
  const clientPoint = hash(clientId) % 2^32;

  // Place backends on ring
  const backendPoints = backends.map(b => ({
    backend: b.name,
    point: hash(b.name) % 2^32
  }));

  // Sort by point
  backendPoints.sort((a, b) => a.point - b.point);

  // Find first backend clockwise from client point
  for (const bp of backendPoints) {
    if (bp.point >= clientPoint) {
      return bp.backend;
    }
  }

  // Wrap around to first backend
  return backendPoints[0].backend;
}
```

**Example consistent hashing**:
```json
// Hash ring (simplified):
// 0°    : backend-1
// 120°  : backend-2
// 240°  : backend-3

// Client requests:
Request:  {"type": "http_request", "msg_id": 1, "client_id": "alice", "path": "/api/data", "algorithm": "consistent-hash"}
Response: {"type": "http_response", "in_reply_to": 1, "backend": "backend-2", "hash_ring_position": 45}

// Same client always routes to same backend:
Request:  {"type": "http_request", "msg_id": 2, "client_id": "alice", "path": "/api/data", "algorithm": "consistent-hash"}
Response: {"type": "http_response", "in_reply_to": 2, "backend": "backend-2", "hash_ring_position": 45}

// Different client routes to potentially different backend:
Request:  {"type": "http_request", "msg_id": 3, "client_id": "bob", "path": "/api/data", "algorithm": "consistent-hash"}
Response: {"type": "http_response", "in_reply_to": 3, "backend": "backend-1", "hash_ring_position": 300}
```

## Concepts

- consistent hashing
- session affinity
- cache coherency
- minimal disruption
- backend additions/removals

## Hints

- Hash client_id or session_id to a point on the hash ring
- Route to the first backend clockwise from that point
- Same client always routes to same backend (sticky routing)
- When backend added, only 1/N of clients remap
- Use virtual nodes for better distribution

## Test Cases

### 1. Same client always routes to same backend

All 3 requests from alice should route to the same backend.

Input:

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["backend-1","backend-2","backend-3"],"algorithm":"consistent-hash"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"client_id":"alice"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":3,"client_id":"alice"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":4,"client_id":"alice"}}
```

Expected output:

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Backend addition causes minimal remapping

Adding b4 should only remap ~25% of clients (1-3 clients), not all 10.

Input:

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["b1","b2","b3"],"algorithm":"consistent-hash"}}
{"src":"client","dest":"lb","body":{"type":"test_remap","msg_id":2,"new_backend":"b4","clients":["c1","c2","c3","c4","c5","c6","c7","c8","c9","c10"]}}
```

Expected output:

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

## Resources

- [Consistent Hashing for Load Balancing](https://www.nginx.com/blog/nginx-load-balancing-algorithms/): NGINX documentation on consistent hashing load balancing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
