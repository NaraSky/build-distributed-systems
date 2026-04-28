# 实现服务网格架构

英文标题：Implement Service Mesh Architecture
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-1-service-mesh>

课程：28. 编排器：容器调度与服务网格
任务序号：6
短标题：Service Mesh
难度：高级
子主题：Service Mesh

## 中文导读

这道题要求你实现一个模拟边车代理（Sidecar Proxy）行为的节点。服务网格（Service Mesh）给每个服务都配备一个边车代理，所有流量都通过这些代理流转。代理透明地处理服务发现、重试、熔断和分布式追踪，应用代码完全不需要改动。你可以把边车代理想象成每个服务的"私人助理"，自动处理所有通信细节。

## 题目说明

服务网格（Service Mesh）给每个服务都配备一个边车代理。所有流量都通过这些代理流转，代理透明地处理服务发现、重试、熔断和分布式追踪，无需修改任何应用代码。

请实现一个模拟边车代理行为的节点：

```json
// 边车拦截请求并添加追踪上下文
{ "type": "call", "msg_id": 1, "path": "/api/users/123", "proxy": true }
-> { "type": "proxied", "in_reply_to": 1,
    "proxied_by": "sidecar-a", "trace_id": "<uuid>" }

// 发现某个服务的健康实例
{ "type": "discover", "msg_id": 2, "service": "service-b" }
-> { "type": "discovered", "in_reply_to": 2,
    "service": "service-b",
    "instances": [{"host": "10.0.1.1", "port": 8080},
                  {"host": "10.0.1.2", "port": 8080}] }

// 失败次数过多后熔断器打开
{ "type": "call", "msg_id": 3,
  "force_failures": 6, "circuit_breaker": true }
-> { "type": "circuit_breaker_open", "in_reply_to": 3,
    "service": "service-b", "reason": "Too many failures" }
```

每个通过边车代理转发的请求都必须携带一个唯一的 `trace_id`，以便在跨服务调用时实现端到端追踪。

## 涉及概念

- `service mesh`
- `sidecar proxy`
- `service discovery`
- `circuit breaker`
- `retry`
- `distributed tracing`

## 实现提示

- 边车代理拦截其所属服务的所有入站和出站流量
- `discover` 从服务注册中心查询指定服务的健康实例
- 为每个代理转发的请求添加 `trace_id`，以便跨服务关联追踪
- 当失败次数超过阈值时熔断器打开，打开期间立即返回失败
- 指数退避重试：第一次重试等待 base_ms，第二次等待 base_ms*2，以此类推

## 测试用例

### 1. 边车代理拦截流量

边车应拦截并转发请求，同时附带 trace_id。

输入：

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"path":"/api/users/123"},"proxy":true}
```

期望输出：

```text
{"type": "proxied", "in_reply_to": 1, "proxied_by": "sidecar-a", "trace_id": ".*"}
```

### 2. 服务发现路由到实例

应从服务注册中心返回健康的实例列表。

输入：

```json
{"src":"sidecar","dest":"registry","body":{"type":"discover","msg_id":1,"service":"service-b"}}
```

期望输出：

```text
{"type": "discovered", "in_reply_to": 1, "service": "service-b", "instances": [{"host": "10.0.1.1", "port": 8080}, {"host": "10.0.1.2", "port": 8080}]}
```

## 参考资料

- [Service Mesh Explained](https://www.nginx.com/blog/what-is-a-service-mesh/)：什么是服务网格以及为什么需要它
- [Envoy Proxy](https://www.envoyproxy.io/)：Envoy 代理官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
