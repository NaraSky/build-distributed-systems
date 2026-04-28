# 添加 Health Checks和Failover

英文标题：Add Health Checks和Failover
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-3-health-checks>

课程：14. 负载均衡器
任务序号：3
短标题：Health Checks
难度：intermediate
子主题：Layer 4 Load Balancing

## 中文导读

本题要求你完成 `添加 Health Checks和Failover`。

重点关注：`health check`、`failover`、`liveness`。

建议先按提示逐步实现：Periodically probe each 服务端。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Add health checking to your load balancer:

1. Periodically send health check requests to servers
2. Track consecutive failures per 服务端
3. Mark 服务端 unhealthy after N failures
4. Exclude unhealthy servers from selection
5. Re-add servers after successful health checks

Support both active (probing)和passive (observing failures) checks.

## 概念说明

### Health Checking

Health checks detect 服务端 failures before routing requests to them. Active checks send periodic probes (HTTP GET /health). Passive checks observe real 请求 failures.

### Graceful Degradation

When servers fail, the load balancer redistributes traffic to healthy servers. Slow re-introduction (ramping up traffic) prevents overwhelming recovering servers.

## 涉及概念

- `health check`
- `failover`
- `liveness`

## 实现提示

- Periodically probe each 服务端
- Mark unhealthy after consecutive failures
- Remove from rotation until healthy

## 测试用例

### 1. Exclude unhealthy server

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"health_status","msg_id":2,"server":"s1","consecutive_failures":5,"threshold":3}}
{"src":"c2","dest":"lb","body":{"type":"get_healthy_servers","msg_id":3}}
```

期望输出：

```text
{"src":"lb","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"lb","dest":"c1","body":{"type":"health_status_ok","in_reply_to":2,"msg_id":1,"status":"unhealthy"}}
{"src":"lb","dest":"c2","body":{"type":"get_healthy_servers_ok","in_reply_to":3,"msg_id":2,"healthy":["s2","s3"]}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
