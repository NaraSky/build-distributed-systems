# 实现接口优雅降级

英文标题：Implement Graceful API Degradation
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-3-graceful-degradation>

课程：27. 迁移器：数据与协议演进
任务序号：8
短标题：Graceful Degradation
难度：高级
子主题：Protocol and API Evolution

## 中文导读

这道题要求你实现一个在下游服务故障时能优雅降级的节点。在分布式系统中，某个服务挂掉是家常便饭。优雅降级的核心思想是：与其给用户一个冷冰冰的错误页面，不如返回缓存数据、关闭非核心功能或将请求排队稍后处理，让用户得到一个"缩水但可用"的体验。

## 题目说明

优雅降级（Graceful Degradation）让你的接口在下游服务故障时仍能保持可用。与其直接返回错误，不如返回缓存数据、禁用非关键功能，或将请求排队稍后处理。用户得到的是一个略有缩减的体验，而不是完全不可用。

请实现一个在故障条件下能优雅降级的节点：

```json
// 服务故障 -> 打开熔断器，返回缓存数据
{ "type": "get_user", "msg_id": 1,
  "user_id": 123, "force_failures": 6 }
-> { "type": "user_response", "in_reply_to": 1,
    "user": {"id": 123, "name": "John Doe"},
    "circuit_state": "open", "from_cache": true }

// 依赖服务不可用 -> 返回过期的缓存数据
{ "type": "get_product", "msg_id": 2,
  "product_id": 123, "service_unavailable": true }
-> { "type": "product_response", "in_reply_to": 2,
    "product": {"id": 123, "name": "Product"},
    "_cached": true }

// 高负载 -> 禁用耗资源的功能
{ "type": "set_mode", "msg_id": 3,
  "mode": "degraded", "cpu_usage": 85 }
-> { "type": "mode_changed", "in_reply_to": 3,
    "mode": "degraded",
    "disabled_features": ["recommendations", "search"] }
```

## 概念说明

优雅降级就像一架飞机在一个引擎出故障时的应对方式：它不会直接坠毁，而是用剩下的引擎继续飞行，虽然速度慢了一些，但乘客仍然能安全到达目的地。熔断器（Circuit Breaker）就像家里的保险丝，在电路出问题时自动断开以保护整个系统。缓存降级则像超市在供货中断时先卖库存商品，虽然不是最新鲜的，但总比空货架强。

## 涉及概念

- `graceful degradation`
- `circuit breaker`
- `fallback cache`
- `feature flags`
- `request queuing`

## 实现提示

- 熔断器：当失败次数超过阈值后，不再调用故障服务，直接返回缓存数据
- 缓存降级：当依赖服务不可用时，返回过期数据并标记 `_cached: true`
- 功能开关：在高负载时禁用耗资源的非核心功能（如推荐、搜索）
- 请求排队：当服务不可用时，接受请求并排队稍后处理
- `circuit_state: "open"` 表示熔断器已触发，正在使用降级方案

## 测试用例

### 1. 熔断器在多次失败后打开

6 次失败后熔断器打开，返回缓存数据。

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_user","msg_id":1,"user_id":123,"force_failures":6}}
```

期望输出：

```text
{"type": "user_response", "in_reply_to": 1, "user": {"id": 123, "name": "John Doe"}, "circuit_state": "open", "from_cache": true}
```

### 2. 降级到缓存数据

服务不可用时应返回过期的缓存数据。

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_product","msg_id":1,"product_id":123,"service_unavailable":true}}
```

期望输出：

```text
{"type": "product_response", "in_reply_to": 1, "product": {"id": 123, "name": "Product"}, "_cached": true}
```

## 参考资料

- [Graceful Degradation](https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead)：舱壁模式和熔断器模式，用于实现优雅降级
- [Graceful Degradation](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)：亚马逊构建者库中关于优雅降级的指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
