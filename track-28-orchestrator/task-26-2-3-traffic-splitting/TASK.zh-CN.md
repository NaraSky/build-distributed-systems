# 实现服务网格中的流量分割

英文标题：Implement Traffic Splitting in Service Mesh
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-3-traffic-splitting>

课程：28. 编排器：容器调度与服务网格
任务序号：8
短标题：Traffic Splitting
难度：进阶
子主题：Service Mesh

## 中文导读

这道题要求你实现一个按分流规则路由请求的节点。发布新版本时，一次性把所有用户切过去风险很大。流量分割让你可以渐进式地放量，比如先把 5% 的流量导到新版本看看效果，没问题再逐步放大。这是安全上线新版本的核心技术。

## 题目说明

流量分割（Traffic Splitting）让你可以渐进式地发布新版本，而不是一次性切换所有用户。你可以将少量流量导向新版本进行试探（这叫金丝雀部署），根据请求头路由特定用户到不同版本（用于做对比实验），或者按 50/50 分流（蓝绿部署）。

请实现一个按分流规则路由请求的节点：

```json
// 按权重分流：80% 到 v1，20% 到 v2
{ "type": "route", "msg_id": 1 }
{ traffic_split: {"v1": 80, "v2": 20} }
-> { "type": "routed", "in_reply_to": 1,
    "version": "v1", "reason": "weighted_routing" }

// 基于请求头的路由优先于权重分流
{ "type": "route", "msg_id": 2,
  "headers": {"x-beta": "true"} }
-> { "type": "routed", "in_reply_to": 2,
    "version": "v2", "reason": "header_match" }

// 更新金丝雀比例（v1 + v2 = 100）
{ "type": "update_canary", "msg_id": 3,
  "service": "api", "percentage": 50 }
-> { "type": "canary_updated", "in_reply_to": 3,
    "service": "api", "v1": 50, "v2": 50 }

// 每个用户的实验分组稳定不变
{ "type": "assign_variant", "msg_id": 4, "user_id": "user-123" }
-> { "type": "variant_assigned", "in_reply_to": 4,
    "user_id": "user-123", "variant": "A" }
```

实验分组必须是确定性的：同一个用户标识必须始终被分配到同一个实验组。

## 概念说明

流量分割就像一个十字路口的交通管制：你可以控制多少比例的车辆走新修的路，多少走老路。金丝雀部署的名字来源于矿井中的金丝雀，矿工先派金丝雀下井探测有没有毒气，没问题了自己再下去。类似地，先让少量流量去"探路"，确认新版本没问题后再全量切换。

## 涉及概念

- `canary deployment`
- `traffic splitting`
- `A/B testing`
- `blue-green deployment`
- `weighted routing`

## 实现提示

- 按权重路由：生成一个 0 到 99 的随机数，如果小于新版本的百分比则路由到新版本，否则路由到老版本
- 基于请求头的路由：先检查请求头是否匹配，不匹配时再回退到权重路由
- `update_canary` 修改新老版本的分流比例，两者之和必须等于 100
- 实验分组：通过 `hash(user_id) % 2` 为每个用户生成稳定的确定性分组
- 请求头匹配的优先级高于权重分流

## 测试用例

### 1. 按权重分割流量

应路由到 v1（80% 权重）。

输入：

```json
{"src":"client","dest":"proxy","body":{"type":"route","msg_id":1},"traffic_split":{"v1":80,"v2":20}}
```

期望输出：

```text
{"type": "routed", "in_reply_to": 1, "version": "v1", "reason": "weighted_routing"}
```

### 2. 基于请求头的路由

带有 x-beta 头的请求应路由到 v2。

输入：

```json
{"src":"client","dest":"proxy","body":{"type":"route","msg_id":1,"headers":{"x-beta":"true"}}}
```

期望输出：

```text
{"type": "routed", "in_reply_to": 1, "version": "v2", "reason": "header_match"}
```

## 参考资料

- [Canary Deployments](https://martinfowler.com/bliki/CanaryRelease.html)：通过渐进式流量切换安全地发布到生产环境

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
