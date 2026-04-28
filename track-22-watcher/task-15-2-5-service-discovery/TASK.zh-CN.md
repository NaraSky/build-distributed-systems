# 构建服务发现系统

英文标题：Build a Service Discovery System
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-5-service-discovery>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：10
短标题：Service Discovery
难度：进阶
子主题：Watches and Sessions

## 中文导读

这道题要求你构建一个服务发现系统。在微服务架构中，服务实例可能随时上线或下线，客户端需要动态地知道哪些服务实例可用。利用 ZooKeeper 的临时节点和监听器，服务上线时注册、下线时自动注销，客户端实时收到变更通知，替代了传统的手动配置。

## 题目说明

服务发现（Service Discovery）使服务之间能够动态地找到彼此。ZooKeeper 的临时节点和监听器提供了自动的服务注册、健康监控和变更通知能力。

**服务注册**：
1. 服务启动后创建：`/services/web/instance-1` 作为临时节点
2. 节点数据：`{"host": "10.0.0.1", "port": 8080, "version": "2.1"}`
3. 如果服务崩溃，临时节点会被自动删除

**服务发现**：
1. 客户端调用 `GetChildren("/services/web", watch=true)`
2. 客户端获得实例列表：`["instance-1", "instance-2"]`
3. 客户端读取每个实例的数据获取地址信息
4. 当有实例上线或下线时，客户端的监听器被触发

```json
Request:  {"type": "service_register", "msg_id": 1, "service": "web", "instance": "i-001", "host": "10.0.0.1", "port": 8080, "session_id": "s1"}
Response: {"type": "service_register_ok", "in_reply_to": 1, "path": "/services/web/i-001"}

Request:  {"type": "service_discover", "msg_id": 2, "service": "web"}
Response: {"type": "service_discover_ok", "in_reply_to": 2, "instances": [{"instance": "i-001", "host": "10.0.0.1", "port": 8080}, {"instance": "i-002", "host": "10.0.0.2", "port": 8080}]}
```

## 涉及概念

- `service discovery`
- `ephemeral registration`
- `service registry`
- `health monitoring`
- `client notification`

## 实现提示

- 服务以临时节点的形式注册在 /services/<服务名>/<实例ID> 下
- 当服务崩溃时，其临时节点会被自动删除
- 客户端监听 /services/<服务名>/，当实例发生变化时收到通知
- 每次注册时将地址和元数据存储在节点数据中
- 这用动态的、自我修复的发现机制替代了手动配置

## 测试用例

### 1. 注册并发现服务

service_discover_ok 应当列出 i-001 及其 host 和 port。

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

### 2. 会话过期时移除注册

会话过期后，service_discover_ok 不应当再列出 i-001。

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

- [ZooKeeper Service Discovery](https://curator.apache.org/docs/service-discovery)：基于 ZooKeeper 构建的 Apache Curator 服务发现框架

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
