# 构建带故障转移的时间预言机服务

英文标题：Build a Time Oracle Service with Failover
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-4-time-oracle>

课程：16. 时间守卫：逻辑时钟
任务序号：19
短标题：时间预言机
难度：高级
子主题：混合逻辑时钟

## 中文导读

本题要求你构建一个集中式的时间预言机（Time Oracle）服务。在分布式系统中，各节点的时钟可能存在不可控的偏差，而时间预言机提供一个全局一致的时间戳来源，解决了这个问题。你还需要实现当主预言机宕机时自动切换到备用预言机的故障转移机制，这是 TiDB 等数据库的核心组件之一。

## 题目说明

构建一个集中式的时间预言机服务，各节点向它查询全局一致的 HLC 时间戳，从而避免节点之间时钟偏差不可控的问题。

系统架构：
- **主预言机**：维护一个 HLC，按请求发放时间戳
- **备用预言机**：监控主预言机，主预言机故障时接管工作
- **普通节点**：向预言机查询时间戳，而不使用本地时钟

故障场景：如果主预言机在发放了时间戳 T 之后崩溃，但备用预言机还不知道这件事，那么备用预言机必须从 T + safety_margin 开始发放时间戳，以避免发出重复的时间戳。

请实现以下处理器：

```json
Request:  {"type": "oracle_get_time", "msg_id": 1}
Response: {"type": "oracle_get_time_ok", "in_reply_to": 1, "pt": 1000, "c": 0, "oracle": "primary"}

Request:  {"type": "oracle_fail_primary", "msg_id": 2}
Response: {"type": "oracle_fail_primary_ok", "in_reply_to": 2, "new_oracle": "backup", "safety_margin_ms": 100}

Request:  {"type": "oracle_get_time", "msg_id": 3}
Response: {"type": "oracle_get_time_ok", "in_reply_to": 3, "pt": 1100, "c": 0, "oracle": "backup"}

Request:  {"type": "oracle_status", "msg_id": 4}
Response: {"type": "oracle_status_ok", "in_reply_to": 4, "primary_alive": false, "active_oracle": "backup", "timestamps_issued": 2}
```

## 涉及概念

- `time oracle`
- `centralized clock`
- `failover`
- `backup oracle`
- `single point of failure`

## 实现提示

- 预言机维护一个 HLC，对外发放全局一致的时间戳
- 各节点向预言机查询时间戳，而不用自己的本地时钟来排序
- 如果主预言机崩溃，备用预言机以更大的计数器接管
- 备用预言机必须从一个保证比主预言机发出过的任何时间戳都大的值开始
- 使用租约机制：预言机只在租约有效期内才是合法的

## 测试用例

### 1. 主预言机发放时间戳

两次 `oracle_get_time_ok` 响应来自主预言机，第二个时间戳必须严格大于第一个。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 故障转移到备用预言机

在 `oracle_fail_primary` 之后，`oracle_get_time_ok` 应显示 oracle 为 backup，且 pt 大于等于上一次主预言机发出的 pt 加上 safety_margin。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"oracle_fail_primary","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [TiDB - Timestamp Oracle Design](https://docs.pingcap.com/tidb/stable/tidb-architecture)：介绍 TiDB 如何使用集中式时间戳预言机来实现事务排序

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
