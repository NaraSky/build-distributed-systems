# 实现 Weighted Round-Robin Load Balancing

英文标题：Implement Weighted Round-Robin Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-2-weighted-round-robin>

课程：14. 负载均衡器
任务序号：12
短标题：Weighted Round-Robin
难度：intermediate
子主题：高级 Balancing Algorithms

## 中文导读

本题要求你完成 `实现 Weighted Round-Robin Load Balancing`。

重点关注：`weighted round-robin`、`capacity-based routing`、`backend weights`、`heterogeneous clusters`、`traffic proportionality`。

建议先按提示逐步实现：Assign weights to backends based on capacity (e.g., CPU, memory)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**Why weighted round-robin?**. ```. Problem: backends have different capacities. backend-1: 8 cores, 32GB RAM (high capacity). backend-2: 8 cores, 32GB RAM (high capacity). backend-3: 2 cores, 8GB RAM (low capacity). Standard round-robin sends 33% to each:. - backend-3 gets overwhelmed. - backend-1和backend-2 underutilized. Weighted round-robin (weights: 4, 4, 2):. - backend-1: 40% of traffic. - backend-2: 40% of traffic. - backend-3: 20% of traffic. - Matches capacity ratios. ```. **Smooth weighted round-robin algorithm**:. ```typescript. name: string,. weight: number,. currentWeight: number. let maxBackend = null;. let maxWeight = -Infinity;. let totalWeight = 0;. // Add weight to each backend's current weight. backend.currentWeight += backend.weight;. totalWeight += backend.weight;. maxWeight = backend.currentWeight;. maxBackend = backend.name;. // Subtract total weight from selected backend. maxBackend.currentWeight -= totalWeight;. return maxBackend.name;. ```. **Example weighted routing**:. ```JSON. // Configuration:. "backends": [. ]. // 请求 sequence (first 10 requests):. 请求: 1 → api-1. 请求: 2 → api-2. 请求: 3 → api-1. 请求: 4 → api-2. 请求: 5 → api-1. 请求: 6 → api-2. 请求: 7 → api-1. 请求: 8 → api-2. 请求: 9 → api-3 (20% traffic). 请求: 10 → api-3. // Distribution: api-1: 40%, api-2: 40%, api-3: 20%. ```

## 涉及概念

- `weighted round-robin`
- `capacity-based routing`
- `backend weights`
- `heterogeneous clusters`
- `traffic proportionality`

## 实现提示

- Assign weights to backends based on capacity (e.g., CPU, memory)
- Higher weight = proportionally more requests
- Weights 4, 4, 2 means 40%, 40%, 20% traffic distribution
- Use a smooth weighted round-robin algorithm
-处理weight changes dynamically without disruption

## 测试用例

### 1. Weight-based distribution

10 requests should distribute as: api-1: 4, api-2: 4, api-3: 2 (40%, 40%, 20%).

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"api-1","weight":4},{"name":"api-2","weight":4},{"name":"api-3","weight":2}],"algorithm":"weighted-round-robin"}}
{"src":"client","dest":"lb","body":{"type":"send_requests","msg_id":2,"count":10}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Unequal weights

14 requests should distribute as: large: 10, medium: 3, small: 1 (71%, 21%, 7%).

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

- [Weighted Round-Robin DNS](https://www.nginx.com/blog/nginx-load-balancing-algorithms/)：NGINX weighted load balancing documentation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
