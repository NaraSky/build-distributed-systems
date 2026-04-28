# 实现 Alert Integrations和On-Call Management

英文标题：Implement Alert Integrations和On-Call Management
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-5-alert-integrations>

课程：25. 追踪器：可观测性
任务序号：10
短标题：Alert Integrations
难度：intermediate
子主题：Metrics和Alerting

## 中文导读

本题要求你完成 `实现 Alert Integrations和On-Call Management`。

重点关注：`PagerDuty`、`Slack`、`on-call rotation`、`escalation policy`、`incident lifecycle`。

建议先按提示逐步实现：create_incident returns incident_id, status=triggered,和the assigned on-call user。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Alert integrations route notifications to the right people和tools. Critical incidents trigger PagerDuty to page the on-call engineer. Non-critical alerts post to Slack用于team visibility，包含action buttons. If no one responds, escalation policies ensure the alert keeps moving up the chain.

Implement a 节点 that handles alert routing和on-call management:

```JSON
// CRITICAL alert -> PagerDuty incident
{ "type": "create_incident", "msg_id": 1,
  "title": "High error rate", "service": "api",
  "severity": "critical",
  "description": "Error rate is 15% (threshold: 5%)" }
-> { "type": "incident_created", "in_reply_to": 1,
    "incident_id": "INC123", "status": "triggered",
    "assigned_to": "on-call-engineer" }

// WARNING alert -> Slack channel，包含action buttons
{ "type": "send_alert", "msg_id": 2,
  "channel": "#alerts", "severity": "warning",
  "title": "WARNING: High latency", "service": "api" }
-> { "type": "alert_sent", "in_reply_to": 2,
    "channel": "#alerts", "notification_id": "<uuid>",
    "actions": ["Acknowledge", "View Details"] }

// No 响应 after 15 min -> escalate to next level
{ "type": "escalate_incident", "msg_id": 3,
  "incident_id": "INC123", "current_level": 1,
  "timeout_minutes": 15, "no_response": true }
-> { "type": "incident_escalated", "in_reply_to": 3,
    "incident_id": "INC123",
    "from_level": 1, "to_level": 2,
    "escalated_to": "team-lead@example.com" }
```

## 涉及概念

- `PagerDuty`
- `Slack`
- `on-call rotation`
- `escalation policy`
- `incident lifecycle`

## 实现提示

- create_incident returns incident_id, status=triggered,和the assigned on-call user
- send_alert formats a Slack 消息，包含action buttons: Acknowledge和View Details
- get_on_call looks up who is currently on-call用于a team at a specific time
- Escalation: after 超时，包含no 响应, escalate to the next level in the policy
- notification_id in Slack 响应 should be unique per 消息

## 测试用例

### 1. PagerDuty alert integration

Should create PagerDuty incident和assign to on-call engineer.

输入：

```json
{"src":"alerter","dest":"pagerduty","body":{"type":"create_incident","msg_id":1,"title":"High error rate","service":"api","severity":"critical","description":"Error rate is 15% (threshold: 5%)"}}
```

期望输出：

```text
{"type": "incident_created", "in_reply_to": 1, "incident_id": "INC123", "status": "triggered", "assigned_to": "on-call-engineer"}
```

### 2. Slack alert notification

Should send formatted Slack alert，包含action buttons.

输入：

```json
{"src":"alerter","dest":"slack","body":{"type":"send_alert","msg_id":1,"channel":"#alerts","title":"WARNING: High latency","severity":"warning","description":"P95 latency is 500ms (threshold: 200ms)","service":"api"}}
```

期望输出：

```text
{"type": "alert_sent", "in_reply_to": 1, "channel": "#alerts", "notification_id": ".*", "actions": ["Acknowledge", "View Details"]}
```

## 参考资料

- [PagerDuty API](https://developer.pagerduty.com/api-reference/)：PagerDuty API用于incident creation和on-call management
- [Slack API Webhooks](https://api.slack.com/messaging/webhooks)：Slack incoming webhooks documentation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
