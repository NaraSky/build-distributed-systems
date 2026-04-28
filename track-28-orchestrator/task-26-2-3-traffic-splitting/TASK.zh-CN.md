# 实现 Traffic Splitting in 服务 Mesh

英文标题：Implement Traffic Splitting in Service Mesh
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-3-traffic-splitting>

课程：28. 编排器：容器调度与服务网格
任务序号：8
短标题：Traffic Splitting
难度：intermediate
子主题：服务 Mesh

## 中文导读

本题要求你完成 `实现 Traffic Splitting in 服务 Mesh`。

重点关注：`canary deployment`、`traffic splitting`、`A/B testing`、`blue-green deployment`、`weighted routing`。

建议先按提示逐步实现：Weighted routing: pick a random number 0-99; route to v2 if < v2_percentage, else v1。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Traffic splitting lets you roll out a new version gradually instead of switching all users at once. You can send a small percentage to the new version (canary), route specific users by 请求 headers (A/B test), or split 50/50 (blue-green).

Implement a 节点 that routes requests according to splitting rules:

```JSON
// Weighted split: 80% to v1, 20% to v2
{ "type": "route", "msg_id": 1 }
{ traffic_split: {"v1": 80, "v2": 20} }
-> { "type": "routed", "in_reply_to": 1,
    "version": "v1", "reason": "weighted_routing" }

// Header-based routing overrides weight
{ "type": "route", "msg_id": 2,
  "headers": {"x-beta": "true"} }
-> { "type": "routed", "in_reply_to": 2,
    "version": "v2", "reason": "header_match" }

// Update canary percentage (v1 + v2 = 100)
{ "type": "update_canary", "msg_id": 3,
  "service": "api", "percentage": 50 }
-> { "type": "canary_updated", "in_reply_to": 3,
    "service": "api", "v1": 50, "v2": 50 }

// Stable A/B assignment per user
{ "type": "assign_variant", "msg_id": 4, "user_id": "user-123" }
-> { "type": "variant_assigned", "in_reply_to": 4,
    "user_id": "user-123", "variant": "A" }
```

A/B variant assignment must be deterministic: the same user_id must always receive the same variant.

## 涉及概念

- `canary deployment`
- `traffic splitting`
- `A/B testing`
- `blue-green deployment`
- `weighted routing`

## 实现提示

- Weighted routing: pick a random number 0-99; route to v2 if < v2_percentage, else v1
- Header-based routing: check 请求 headers用于a match before falling back to weighted
- update_canary changes the v1/v2 split percentages; v1 + v2 must always sum to 100
- A/B test assignment: hash(user_id) % 2 gives a stable deterministic variant per user
- Header match takes priority over weighted split when both rules are active

## 测试用例

### 1. Weighted traffic split

Should route to v1 (80% weight).

输入：

```json
{"src":"client","dest":"proxy","body":{"type":"route","msg_id":1},"traffic_split":{"v1":80,"v2":20}}
```

期望输出：

```text
{"type": "routed", "in_reply_to": 1, "version": "v1", "reason": "weighted_routing"}
```

### 2. Header-based routing

x-beta header should route to v2.

输入：

```json
{"src":"client","dest":"proxy","body":{"type":"route","msg_id":1,"headers":{"x-beta":"true"}}}
```

期望输出：

```text
{"type": "routed", "in_reply_to": 1, "version": "v2", "reason": "header_match"}
```

## 参考资料

- [Canary Deployments](https://martinfowler.com/bliki/CanaryRelease.html)：Gradual traffic shifting用于safe production rollouts

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
