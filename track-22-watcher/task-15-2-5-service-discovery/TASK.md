# Build a Service Discovery System

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-5-service-discovery>

Track: 22. The Watcher
Task order: 10
Short title: Service Discovery
Difficulty: intermediate
Subtrack: Watches and Sessions

## Problem

Service discovery enables services to find each other dynamically. ZooKeeper ephemeral nodes and watches provide automatic service registration, health monitoring, and notification.

**Service registration**:
1. Service starts and creates: `/services/web/instance-1` as an EPHEMERAL node
2. Node data: `{"host": "10.0.0.1", "port": 8080, "version": "2.1"}`
3. If the service crashes, the ephemeral node is auto-deleted

**Service discovery**:
1. Client calls `GetChildren("/services/web", watch=true)`
2. Client receives the list of instances: `["instance-1", "instance-2"]`
3. Client reads each instance's data for host:port
4. When an instance is added/removed, the client's watch fires

```json
Request:  {"type": "service_register", "msg_id": 1, "service": "web", "instance": "i-001", "host": "10.0.0.1", "port": 8080, "session_id": "s1"}
Response: {"type": "service_register_ok", "in_reply_to": 1, "path": "/services/web/i-001"}

Request:  {"type": "service_discover", "msg_id": 2, "service": "web"}
Response: {"type": "service_discover_ok", "in_reply_to": 2, "instances": [{"instance": "i-001", "host": "10.0.0.1", "port": 8080}, {"instance": "i-002", "host": "10.0.0.2", "port": 8080}]}
```

## Concepts

- service discovery
- ephemeral registration
- service registry
- health monitoring
- client notification

## Hints

- Services register as ephemeral nodes under /services/<service-name>/<instance-id>
- When a service crashes, its ephemeral node is auto-deleted
- Clients watch /services/<service-name>/ and get notified of instance changes
- Each registration stores host:port and metadata in the node data
- This replaces manual configuration with dynamic, self-healing discovery

## Test Cases

### 1. Register and discover service

service_discover_ok should list i-001 with host and port.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"service_register","msg_id":2,"service":"web","instance":"i-001","host":"10.0.0.1","port":8080,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"service_discover","msg_id":3,"service":"web"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Session expiry removes registration

After session expiry, service_discover_ok should not list i-001.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"service_register","msg_id":2,"service":"db","instance":"i-001","host":"10.0.0.5","port":3306,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"session_expire","msg_id":3,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"service_discover","msg_id":4,"service":"db"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Service Discovery](https://curator.apache.org/docs/service-discovery): Apache Curator service discovery framework built on ZooKeeper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
