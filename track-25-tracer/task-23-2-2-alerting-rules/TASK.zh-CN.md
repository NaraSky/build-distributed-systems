# 实现 Alerting Rules Engine

英文标题：Implement Alerting Rules Engine
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-2-alerting-rules>

课程：25. 追踪器：可观测性
任务序号：7
短标题：Alerting Rules
难度：intermediate
子主题：Metrics和Alerting

## 中文导读

本题要求你完成 `实现 Alerting Rules Engine`。

重点关注：`alert rules`、`threshold evaluation`、`alert routing`、`alert grouping`、`auto-resolution`。

建议先按提示逐步实现：Fire alert when metric > threshold用于at least duration_sec seconds。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

An alerting rules engine evaluates metric conditions和fires notifications when thresholds are breached. It routes alerts to the right channel based on severity, groups duplicate alerts to prevent storms,和auto-resolves when conditions return to normal.

Implement a 节点 that evaluates alert rules和manages notifications:

```JSON
// Error rate above threshold用于5 minutes -> WARNING
{ "type": "evaluate", "msg_id": 1,
  "metric": "error_rate", "value": 0.08,
  "threshold": 0.05, "duration_sec": 300 }
-> { "type": "alert_triggered", "in_reply_to": 1,
    "rule": "High error rate", "severity": "WARNING", "value": 0.08 }

// Service down -> CRITICAL -> page PagerDuty
{ "type": "evaluate", "msg_id": 2,
  "metric": "up", "value": 0, "threshold": 0,
  "duration_sec": 60, "service": "api" }
{ routing: {channels: ["pagerduty"]} }
-> { "type": "alert_triggered", "in_reply_to": 2,
    "severity": "CRITICAL", "action": "page_sent", "service": "api" }

// Metric returns to normal -> auto-resolve
{ "type": "evaluate", "msg_id": 3,
  "metric": "error_rate", "value": 0.01,
  "threshold": 0.05, "alert_resolved": true }
-> { "type": "alert_resolved", "in_reply_to": 3,
    "rule": "High error rate", "resolution": "Value returned to normal" }
```

## 涉及概念

- `alert rules`
- `threshold evaluation`
- `alert routing`
- `alert grouping`
- `auto-resolution`

## 实现提示

- Fire alert when metric > threshold用于at least duration_sec seconds
- Route CRITICAL severity to PagerDuty (pager); WARNING to Slack or email
- Grouping: alerts，包含the same fingerprint are merged into one notification
- Resolution: fire alert_resolved when the metric returns below threshold
- severity is determined by which threshold band the value falls in

## 测试用例

### 1. Threshold alert triggered

Error rate 0.08 exceeds threshold 0.05用于300s -> WARNING.

输入：

```json
{"src":"metrics","dest":"alerter","body":{"type":"evaluate","msg_id":1,"metric":"error_rate","value":0.08,"threshold":0.05,"duration_sec":300}}
```

期望输出：

```text
{"type": "alert_triggered", "in_reply_to": 1, "rule": "High error rate", "severity": "WARNING", "value": 0.08}
```

### 2. Alert routing to PagerDuty

Service down is CRITICAL和should page on-call via PagerDuty.

输入：

```json
{"src":"metrics","dest":"alerter","body":{"type":"evaluate","msg_id":1,"metric":"up","value":0,"threshold":0,"duration_sec":60,"service":"api"},"routing":{"channels":["pagerduty"]}}
```

期望输出：

```text
{"type": "alert_triggered", "in_reply_to": 1, "severity": "CRITICAL", "action": "page_sent", "service": "api"}
```

## 参考资料

- [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)：Alertmanager routing, grouping,和deduplication

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
