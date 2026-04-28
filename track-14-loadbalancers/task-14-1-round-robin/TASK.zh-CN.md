# 实现 Round Robin Load Balancer

英文标题：Implement Round Robin Load Balancer
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-1-round-robin>

课程：14. 负载均衡器
任务序号：1
短标题：Round Robin
难度：beginner
子主题：Layer 4 Load Balancing

## 中文导读

本题要求你完成 `实现 Round Robin Load Balancer`。

重点关注：`round robin`、`load balancing`、`stateless`。

建议先按提示逐步实现：Track current position in 服务端 list。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement round robin load balancing:

1. Maintain an ordered list of backend servers
2. Track current 服务端 索引
3. For each 请求, send to 服务端 at current 索引
4. Increment 索引 (wrapping to 0 at end)

Round robin distributes load evenly when requests have similar cost.

## 概念说明

### Round Robin

Round robin is the simplest load balancing algorithm. Requests cycle through servers in order: 1, 2, 3, 1, 2, 3... It works well when servers are identical和requests have similar processing cost.

### Weighted Round Robin

When servers have different capacities, weighted round robin sends proportionally more requests to stronger servers. A 服务端，包含weight 3 gets three turns用于every one turn of a weight-1 服务端.

## 涉及概念

- `round robin`
- `load balancing`
- `stateless`

## 实现提示

- Track current position in 服务端 list
- Increment和wrap on each 请求
-处理empty 服务端 list

## 测试用例

### 1. Even distribution

Load balancer，包含3 backends (s1, s2, s3). Send 6 requests. Verify round-robin distributes evenly: req1->s1, req2->s2, req3->s3, req4->s1, req5->s2, req6->s3. Each backend gets exactly 2 requests.

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"add_servers","msg_id":2,"servers":["s1","s2","s3"]}}
{"src":"c2","dest":"lb","body":{"type":"get_server","msg_id":3}}
{"src":"c3","dest":"lb","body":{"type":"get_server","msg_id":4}}
{"src":"c4","dest":"lb","body":{"type":"get_server","msg_id":5}}
```

期望输出：

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "add_servers_ok", "servers": ["s1", "s2", "s3"], "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "get_server_ok", "server": "s2", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "get_server_ok", "server": "s3", "in_reply_to": 5, "msg_id": 4}}
```

### 2. Wrap around

Load balancer，包含2 backends (s1, s2). Send 5 requests. Verify 计数器 wraps: req1->s1, req2->s2, req3->s1 (wrap), req4->s2, req5->s1. 索引 should reset to 0 after reaching end of 服务端 list.

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2"]}}
{"src":"c1","dest":"lb","body":{"type":"add_servers","msg_id":2,"servers":["s1","s2"]}}
{"src":"c2","dest":"lb","body":{"type":"get_server","msg_id":3}}
{"src":"c3","dest":"lb","body":{"type":"get_server","msg_id":4}}
{"src":"c4","dest":"lb","body":{"type":"get_server","msg_id":5}}
```

期望输出：

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "add_servers_ok", "servers": ["s1", "s2"], "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "get_server_ok", "server": "s2", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 5, "msg_id": 4}}
```

## 参考资料

- [Load Balancing Algorithms](https://www.nginx.com/blog/choosing-nginx-plus-load-balancing-techniques/)：NGINX guide to load balancing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
