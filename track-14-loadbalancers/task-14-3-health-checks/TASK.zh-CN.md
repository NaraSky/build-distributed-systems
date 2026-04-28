# 添加健康检查与故障转移

英文标题：Add Health Checks and Failover
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-3-health-checks>

课程：14. 负载均衡器
任务序号：3
短标题：Health Checks
难度：进阶
子主题：四层负载均衡

## 中文导读

本题要求你为负载均衡器添加健康检查功能。想象一下，如果某台服务器已经宕机了，负载均衡器还傻傻地往它身上发请求，用户就会看到错误。健康检查就像定期给服务器"量体温"，发现不健康的服务器就暂时不给它分配流量，等它恢复了再重新加入。这是保障系统可用性的关键机制。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

为你的负载均衡器添加健康检查功能：

1. 定期向服务器发送健康检查请求
2. 跟踪每台服务器的连续失败次数
3. 当连续失败次数达到阈值 N 时，将服务器标记为不健康
4. 在选择服务器时排除不健康的服务器
5. 当服务器健康检查恢复成功后，重新将其加入可用列表

需要同时支持主动检查（定期探测）和被动检查（观察实际请求的失败情况）两种方式。

## 概念说明

### 健康检查（Health Checking）

健康检查的目的是在把请求路由到某台服务器之前，先确认它是否正常工作。主动检查是定期发送探测请求（比如 HTTP GET /health），看服务器是否响应正常。被动检查则是观察真实请求的处理结果，如果某台服务器频繁返回错误，就认为它不健康。

### 优雅降级（Graceful Degradation）

当部分服务器故障时，负载均衡器会将流量重新分配到健康的服务器上。对于刚恢复的服务器，不应该一下子给它大量流量，而是逐步增加（称为"慢启动"或"流量预热"），避免刚恢复的服务器被突如其来的请求压垮。

## 涉及概念

- `health check`
- `failover`
- `liveness`

## 实现提示

- 定期探测每台服务器的健康状态
- 连续失败达到阈值后标记为不健康
- 将不健康的服务器从轮转列表中移除，直到恢复健康

## 测试用例

### 1. 排除不健康的服务器

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
