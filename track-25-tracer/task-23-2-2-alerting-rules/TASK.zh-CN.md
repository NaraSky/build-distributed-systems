# 实现告警规则引擎

英文标题：Implement Alerting Rules Engine
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-2-alerting-rules>

课程：25. 追踪器：可观测性
任务序号：7
短标题：Alerting Rules
难度：进阶
子主题：Metrics and Alerting

## 中文导读

这道题要求你实现一个告警规则引擎。它的核心职责是：当指标超过阈值时触发告警通知，根据严重程度将告警路由到对应的通知渠道，对重复告警进行分组以避免告警风暴，并在指标恢复正常时自动解除告警。告警机制是保障线上服务稳定运行的重要防线。

## 题目说明

告警规则引擎负责评估指标条件，并在阈值被突破时发送通知。它根据严重程度将告警路由到正确的通知渠道，对重复告警进行分组以防止告警风暴，并在条件恢复正常时自动解除告警。

请实现一个节点来评估告警规则并管理通知：

```json
// 错误率超过阈值持续 5 分钟 -> 发出 WARNING 告警
{ "type": "evaluate", "msg_id": 1,
  "metric": "error_rate", "value": 0.08,
  "threshold": 0.05, "duration_sec": 300 }
-> { "type": "alert_triggered", "in_reply_to": 1,
    "rule": "High error rate", "severity": "WARNING", "value": 0.08 }

// 服务宕机 -> CRITICAL 告警 -> 呼叫 PagerDuty
{ "type": "evaluate", "msg_id": 2,
  "metric": "up", "value": 0, "threshold": 0,
  "duration_sec": 60, "service": "api" }
{ routing: {channels: ["pagerduty"]} }
-> { "type": "alert_triggered", "in_reply_to": 2,
    "severity": "CRITICAL", "action": "page_sent", "service": "api" }

// 指标恢复正常 -> 自动解除告警
{ "type": "evaluate", "msg_id": 3,
  "metric": "error_rate", "value": 0.01,
  "threshold": 0.05, "alert_resolved": true }
-> { "type": "alert_resolved", "in_reply_to": 3,
    "rule": "High error rate", "resolution": "Value returned to normal" }
```

## 概念说明

**告警规则引擎**就像一个 24 小时值守的监控员：它持续盯着各项指标，一旦发现某个指标超标（比如错误率连续 5 分钟超过 5%），就立即发出告警。**告警路由**决定了通知发到哪里——紧急的问题直接打电话叫醒值班工程师，普通的问题发到团队群就行。**自动解除**则在指标恢复正常后自动关闭告警，避免无意义的干扰。

## 涉及概念

- `alert rules`
- `threshold evaluation`
- `alert routing`
- `alert grouping`
- `auto-resolution`

## 实现提示

- 当指标超过阈值且持续时间达到 duration_sec 秒时，触发告警
- CRITICAL 级别的告警路由到 PagerDuty（呼叫值班人员）；WARNING 级别的路由到 Slack 或邮件
- 告警分组：具有相同指纹的告警合并为一条通知
- 告警解除：当指标回落到阈值以下时，发送 alert_resolved
- 严重程度由指标值落入的阈值区间决定

## 测试用例

### 1. 阈值告警触发

错误率 0.08 超过阈值 0.05 持续 300 秒，应触发 WARNING 告警。

输入：

```json
{"src":"metrics","dest":"alerter","body":{"type":"evaluate","msg_id":1,"metric":"error_rate","value":0.08,"threshold":0.05,"duration_sec":300}}
```

期望输出：

```text
{"type": "alert_triggered", "in_reply_to": 1, "rule": "High error rate", "severity": "WARNING", "value": 0.08}
```

### 2. 告警路由到 PagerDuty

服务宕机属于 CRITICAL 级别，应通过 PagerDuty 呼叫值班工程师。

输入：

```json
{"src":"metrics","dest":"alerter","body":{"type":"evaluate","msg_id":1,"metric":"up","value":0,"threshold":0,"duration_sec":60,"service":"api"},"routing":{"channels":["pagerduty"]}}
```

期望输出：

```text
{"type": "alert_triggered", "in_reply_to": 1, "severity": "CRITICAL", "action": "page_sent", "service": "api"}
```

## 参考资料

- [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)：介绍 Alertmanager 的路由、分组和去重机制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
