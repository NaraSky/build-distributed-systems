# 实现指标聚合与汇总

英文标题：Implement Metrics Aggregation and Rollups
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-3-metrics-aggregation>

课程：25. 追踪器：可观测性
任务序号：8
短标题：Metrics Aggregation
难度：进阶
子主题：Metrics and Alerting

## 中文导读

这道题要求你实现指标数据的聚合和汇总。单个数据点过于细粒度，无法直接用于仪表盘展示和告警判断。聚合操作将它们压缩为有意义的摘要信息：跨服务的请求总量、跨实例的平均内存、按时间窗口的周期性汇总。这是从原始数据中提取有效信息的关键能力。

## 题目说明

单个数据点对于仪表盘和告警来说粒度太细。聚合（Aggregation）将它们压缩为有意义的摘要：跨服务的总计、跨实例的平均值，以及将大量数据点按时间窗口压缩成周期性桶的汇总（Rollup）。

请实现一个节点来执行指标聚合操作：

```json
// 按服务名称分组，对请求总数求和
{ "type": "aggregate_metric", "msg_id": 1,
  "metric": "http_requests_total", "aggregator": "sum",
  "group_by": ["service"],
  "services": ["api","web","auth"], "time_range": "1h" }
-> { "type": "aggregation_result", "in_reply_to": 1,
    "results": [{"service":"api","value":50000},
                 {"service":"web","value":30000},
                 {"service":"auth","value":15000}],
    "total": 95000 }

// 计算三个实例的平均内存使用量
{ "type": "aggregate_metric", "msg_id": 2,
  "metric": "memory_usage_bytes", "aggregator": "avg",
  "values": [1073741824, 2147483648, 1610612736] }
-> { "type": "aggregation_result", "in_reply_to": 2,
    "value": 1610612736, "unit": "bytes", "sample_count": 3 }
```

## 概念说明

**聚合**就像做统计报表：你不需要看每一笔交易的细节，只需要知道"今天总共卖了多少""哪个门店卖得最多"。**汇总**则是按时间窗口压缩数据，比如把每秒一个的数据点压缩成每分钟一个摘要，既能看到趋势又节省存储空间。

## 涉及概念

- `aggregation`
- `rollup`
- `sum`
- `average`
- `percentile`
- `time buckets`

## 实现提示

- sum：将所有服务或实例的值相加
- avg：所有值的总和 / 值的个数
- rollup：按时间间隔对数据点分组，然后在每个桶内计算聚合值
- P95：将所有值排序，取索引位置为 `floor(0.95 * count)` 的值
- sum 聚合中的 total 是所有分组的总计值

## 测试用例

### 1. 跨服务求和聚合

应当按服务对请求数求和，并计算出总计值 95000。

输入：

```json
{"src":"query","dest":"metrics","body":{"type":"aggregate_metric","msg_id":1,"metric":"http_requests_total","aggregator":"sum","group_by":["service"],"services":["api","web","auth"],"time_range":"1h"}}
```

期望输出：

```text
{"type": "aggregation_result", "in_reply_to": 1, "results": [{"service": "api", "value": 50000}, {"service": "web", "value": 30000}, {"service": "auth", "value": 15000}], "total": 95000}
```

### 2. 平均值聚合

三个内存值的平均值应当为 1610612736 字节。

输入：

```json
{"src":"query","dest":"metrics","body":{"type":"aggregate_metric","msg_id":1,"metric":"memory_usage_bytes","aggregator":"avg","instances":["api-1","api-2","api-3"],"values":[1073741824,2147483648,1610612736]}}
```

期望输出：

```text
{"type": "aggregation_result", "in_reply_to": 1, "value": 1610612736, "unit": "bytes", "sample_count": 3}
```

## 参考资料

- [PromQL Aggregation](https://prometheus.io/docs/prometheus/latest/querying/basics/)：Prometheus 查询语言的聚合操作符

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
