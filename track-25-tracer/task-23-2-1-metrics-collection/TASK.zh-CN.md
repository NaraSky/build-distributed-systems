# 实现指标采集

英文标题：Implement Metrics Collection
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-1-metrics-collection>

课程：25. 追踪器：可观测性
任务序号：6
短标题：Metrics Collection
难度：进阶
子主题：Metrics and Alerting

## 中文导读

这道题要求你实现系统指标（Metrics）的采集功能。指标用于量化系统的运行状态：处理了多少请求、速度有多快、占用了多少内存。你需要掌握三种最基本的指标类型——计数器、仪表盘和直方图，它们几乎覆盖了所有监控场景。

## 题目说明

指标（Metrics）用来量化系统的行为：处理了多少请求、响应有多快、消耗了多少内存。三种类型的指标几乎涵盖了所有需求：计数器（Counter，只增不减）、仪表（Gauge，可增可减）和直方图（Histogram，数值分布，如请求耗时的分布）。

请实现一个节点来记录和查询指标：

```json
// 计数器：每收到一个请求，值加 1
{ "type": "counter", "msg_id": 1,
  "name": "http_requests_total", "value": 1,
  "labels": {"method": "POST", "service": "api"} }
-> { "type": "metric_recorded", "in_reply_to": 1,
    "name": "http_requests_total", "value": 1 }

// 仪表：当前堆内存使用量（字节）
{ "type": "gauge", "msg_id": 2,
  "name": "memory_usage_bytes", "value": 1073741824,
  "labels": {"service": "api", "type": "heap"} }
-> { "type": "metric_recorded", "in_reply_to": 2,
    "name": "memory_usage_bytes", "value": 1073741824 }

// 直方图：记录一次请求耗时的观测值
{ "type": "histogram", "msg_id": 3,
  "name": "request_duration_ms", "value": 123,
  "labels": {"endpoint": "/api/users"} }
-> { "type": "metric_recorded", "in_reply_to": 3,
    "name": "request_duration_ms", "count": 1, "sum": 123 }
```

## 概念说明

可以用生活中的例子来理解这三种指标类型：**计数器**就像汽车的里程表，只会往上走，适合记录请求总数、错误总数等；**仪表**就像温度计，可以上下波动，适合记录内存使用量、队列深度等当前状态；**直方图**就像考试成绩的分布图，告诉你大部分请求的耗时落在哪个区间。

## 涉及概念

- `counter`
- `gauge`
- `histogram`
- `labels`
- `percentile`

## 实现提示

- 计数器：只能递增，适用于请求计数、错误计数、发送字节数
- 仪表：可增可减，适用于内存使用量、队列深度、连接数
- 直方图：记录数值分布，适用于请求耗时、响应体大小
- 标签（Labels）是键值对，为指标添加维度（可按服务、接口、状态码过滤）
- P95 表示第 95 百分位的值：95% 的请求在这个时间内完成

## 测试用例

### 1. 计数器指标

计数器应当记录递增值并返回确认。

输入：

```json
{"src":"service","dest":"metrics","body":{"type":"counter","msg_id":1,"name":"http_requests_total","value":1,"labels":{"method":"POST","service":"api"}}}
```

期望输出：

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "http_requests_total", "value": 1}
```

### 2. 仪表指标

仪表应当记录当前值。

输入：

```json
{"src":"service","dest":"metrics","body":{"type":"gauge","msg_id":1,"name":"memory_usage_bytes","value":1073741824,"labels":{"service":"api","type":"heap"}}}
```

期望输出：

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "memory_usage_bytes", "value": 1073741824}
```

### 3. 直方图指标

直方图应当记录观测值并更新计数和总和。

输入：

```json
{"src":"service","dest":"metrics","body":{"type":"histogram","msg_id":1,"name":"request_duration_ms","value":123,"labels":{"endpoint":"/api/users"}}}
```

期望输出：

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "request_duration_ms", "count": 1, "sum": 123}
```

## 参考资料

- [Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/)：详细介绍计数器、仪表、直方图和摘要这几种指标类型

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
