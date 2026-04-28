# Implement Ephemeral Nodes for Session-Bound State

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-4-ephemeral>

Track: 22. The Watcher
Task order: 4
Short title: Ephemeral Nodes
Difficulty: intermediate
Subtrack: The ZNode Data Model

## Problem

Ephemeral nodes are ZNodes that are automatically deleted when the client session that created them expires. They are the foundation of distributed service registration and failure detection.

**Lifecycle**:
1. Client creates ephemeral node: `Create("/services/web/instance-1", data, EPHEMERAL)`
2. While the client is alive, it sends heartbeats to keep the session active
3. If the client crashes or disconnects, the session eventually expires
4. ZooKeeper automatically deletes all ephemeral nodes created by that session
5. Other clients watching `/services/web/` are notified of the deletion

**Constraints**: ephemeral nodes cannot have children.

```json
Request:  {"type": "znode_create", "msg_id": 1, "path": "/services/web/i-001", "data": "host:8080", "ephemeral": true, "sequential": false, "session_id": "s1"}
Response: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/services/web/i-001", "version": 0}

Request:  {"type": "session_expire", "msg_id": 2, "session_id": "s1"}
Response: {"type": "session_expire_ok", "in_reply_to": 2, "ephemeral_nodes_deleted": ["/services/web/i-001"]}
```

## Concepts

- ephemeral node
- session lifetime
- service registration
- auto-deletion
- failure detection

## Hints

- Ephemeral nodes are automatically deleted when the creating session expires
- A session expires when the server misses heartbeats for the session timeout period
- Ephemeral nodes cannot have children (design constraint)
- Use case: service registers an ephemeral node; when the service crashes, the node disappears
- This enables automatic failure detection without polling

## Test Cases

### 1. Ephemeral node is created

znode_get_ok should show ephemeral: true and data "host".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/svc/i1","data":"host","ephemeral":true,"sequential":false,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":3,"path":"/svc/i1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Session expiry deletes ephemeral nodes

session_expire_ok should list /e in ephemeral_nodes_deleted.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/e","data":"","ephemeral":true,"sequential":false,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"session_expire","msg_id":3,"session_id":"s1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Ephemeral Nodes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#Ephemeral+Nodes): ZooKeeper documentation on ephemeral nodes and session management

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
