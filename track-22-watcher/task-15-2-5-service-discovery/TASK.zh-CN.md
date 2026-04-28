# 构建 a 服务 Discovery System

英文标题：Build a Service Discovery System
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-5-service-discovery>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：10
短标题：服务 Discovery
难度：intermediate
子主题：Watches和Sessions

## 中文导读

本题要求你完成 `构建 a 服务 Discovery System`。

重点关注：`service discovery`、`ephemeral registration`、`service registry`、`health monitoring`、`client notification`。

建议先按提示逐步实现：Services register as ephemeral 节点 under /services/<service-name>/<instance-id>。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Service discovery enables services to find each other dynamically. ZooKeeper ephemeral 节点和watches provide automatic service registration, health monitoring,和notification.

**Service registration**:
1. Service starts和creates: `/services/web/instance-1` as an EPHEMERAL 节点
2. 节点 data: `{"host": "10.0.0.1", "port": 8080, "version": "2.1"}`
3. If the service crashes, the ephemeral 节点 is auto-deleted

**Service discovery**:
1. 客户端 calls `GetChildren("/services/web", watch=true)`
2. 客户端 receives the list of instances: `["instance-1", "instance-2"]`
3. 客户端 reads each instance's data用于host:port
4. When an instance is added/removed, the 客户端's watch fires

```JSON
请求:  {"type": "service_register", "msg_id": 1, "service": "web", "instance": "i-001", "host": "10.0.0.1", "port": 8080, "session_id": "s1"}
响应: {"type": "service_register_ok", "in_reply_to": 1, "path": "/services/web/i-001"}

请求:  {"type": "service_discover", "msg_id": 2, "service": "web"}
响应: {"type": "service_discover_ok", "in_reply_to": 2, "instances": [{"instance": "i-001", "host": "10.0.0.1", "port": 8080}, {"instance": "i-002", "host": "10.0.0.2", "port": 8080}]}
```

## 涉及概念

- `service discovery`
- `ephemeral registration`
- `service registry`
- `health monitoring`
- `client notification`

## 实现提示

- Services register as ephemeral 节点 under /services/<service-name>/<instance-id>
- When a service crashes, its ephemeral 节点 is auto-deleted
- Clients watch /services/<service-name>/和get notified of instance changes
- Each registration stores host:port和元数据 in the 节点 data
- This replaces manual configuration，包含dynamic, self-healing discovery

## 测试用例

### 1. Register和discover 服务

service_discover_ok should list i-001，包含host和port.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"service_register","msg_id":2,"service":"web","instance":"i-001","host":"10.0.0.1","port":8080,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"service_discover","msg_id":3,"service":"web"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Session expiry removes registration

After session expiry, service_discover_ok should not list i-001.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"service_register","msg_id":2,"service":"db","instance":"i-001","host":"10.0.0.5","port":3306,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"session_expire","msg_id":3,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"service_discover","msg_id":4,"service":"db"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Service Discovery](https://curator.apache.org/docs/service-discovery)：Apache Curator service discovery framework built on ZooKeeper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
