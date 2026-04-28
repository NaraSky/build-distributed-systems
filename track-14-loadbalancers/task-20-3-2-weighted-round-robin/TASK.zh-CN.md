# 实现加权轮询负载均衡

英文标题：Implement Weighted Round-Robin Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-2-weighted-round-robin>

课程：14. 负载均衡器
任务序号：12
短标题：Weighted Round-Robin
难度：进阶
子主题：高级均衡算法

## 中文导读

本题要求你实现加权轮询（Weighted Round-Robin）负载均衡。现实中，服务器的配置往往不同——有的是 8 核 32G 的高配机器，有的只是 2 核 8G 的小机器。普通轮询给每台服务器分配一样多的请求，小机器很容易被压垮。加权轮询根据服务器的处理能力分配不同的权重，让强的服务器多干活、弱的服务器少干活，从而物尽其用。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**为什么需要加权轮询**：

当后端服务器的处理能力不同时，普通轮询会有问题。例如 backend-1 和 backend-2 各有 8 核 32G（高配），而 backend-3 只有 2 核 8G（低配）。普通轮询把 33% 的流量分给每台服务器，backend-3 就会被压垮，而 backend-1 和 backend-2 却没有充分利用。使用加权轮询（权重 4、4、2），backend-1 和 backend-2 各承担 40% 的流量，backend-3 只承担 20%，与各自的处理能力匹配。

**平滑加权轮询算法**：
```typescript
name: string,
weight: number,
currentWeight: number
let maxBackend = null;
let maxWeight = -Infinity;
let totalWeight = 0;
// Add weight to each backend's current weight
backend.currentWeight += backend.weight;
totalWeight += backend.weight;
maxWeight = backend.currentWeight;
maxBackend = backend.name;
// Subtract total weight from selected backend
maxBackend.currentWeight -= totalWeight;
return maxBackend.name;
```

**加权路由示例**：
```json
// Configuration:
"backends": [
]
// Request sequence (first 10 requests):
Request: 1 → api-1
Request: 2 → api-2
Request: 3 → api-1
Request: 4 → api-2
Request: 5 → api-1
Request: 6 → api-2
Request: 7 → api-1
Request: 8 → api-2
Request: 9 → api-3 (20% traffic)
Request: 10 → api-3
// Distribution: api-1: 40%, api-2: 40%, api-3: 20%
```

## 涉及概念

- `weighted round-robin`
- `capacity-based routing`
- `backend weights`
- `heterogeneous clusters`
- `traffic proportionality`

## 实现提示

- 根据服务器能力（如 CPU、内存）分配权重
- 权重越高，分配的请求比例越大
- 权重 4、4、2 意味着流量按 40%、40%、20% 分配
- 使用平滑加权轮询算法，使请求分布更均匀（而不是集中分配）
- 支持动态调整权重，且不中断服务

## 测试用例

### 1. 按权重分配

10 个请求的分配结果应为：api-1 收到 4 个，api-2 收到 4 个，api-3 收到 2 个（即 40%、40%、20%）。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"api-1","weight":4},{"name":"api-2","weight":4},{"name":"api-3","weight":2}],"algorithm":"weighted-round-robin"}}
{"src":"client","dest":"lb","body":{"type":"send_requests","msg_id":2,"count":10}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 不等权重分配

14 个请求的分配结果应为：large 收到 10 个，medium 收到 3 个，small 收到 1 个（即 71%、21%、7%）。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"large","weight":10},{"name":"medium","weight":3},{"name":"small","weight":1}],"algorithm":"weighted-round-robin"}}
{"src":"client","dest":"lb","body":{"type":"send_requests","msg_id":2,"count":14}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

## 参考资料

- [Weighted Round-Robin DNS](https://www.nginx.com/blog/nginx-load-balancing-algorithms/)：关于加权负载均衡的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
