# 实现告警集成与值班管理

英文标题：Implement Alert Integrations and On-Call Management
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-5-alert-integrations>

课程：25. 追踪器：可观测性
任务序号：10
短标题：Alert Integrations
难度：进阶
子主题：Metrics and Alerting

## 中文导读

这道题要求你实现告警的外部集成和值班管理。告警触发后，需要路由到正确的人和工具：紧急事件通过 PagerDuty 呼叫值班工程师，非紧急告警发到 Slack 让团队知晓并附带操作按钮。如果没人响应，升级策略会确保告警沿管理链逐级上报。这是保障线上服务可靠运行的最后一环。

## 题目说明

告警集成负责将通知路由到正确的人和工具。紧急事件触发 PagerDuty 呼叫值班工程师；非紧急告警发送到 Slack 供团队了解情况，并附带操作按钮。如果无人响应，升级策略（Escalation Policy）会确保告警沿管理链逐级上报。

请实现一个节点来处理告警路由和值班管理：

```json
// CRITICAL 告警 -> 创建 PagerDuty 事件
{ "type": "create_incident", "msg_id": 1,
  "title": "High error rate", "service": "api",
  "severity": "critical",
  "description": "Error rate is 15% (threshold: 5%)" }
-> { "type": "incident_created", "in_reply_to": 1,
    "incident_id": "INC123", "status": "triggered",
    "assigned_to": "on-call-engineer" }

// WARNING 告警 -> 发送到 Slack 频道并附带操作按钮
{ "type": "send_alert", "msg_id": 2,
  "channel": "#alerts", "severity": "warning",
  "title": "WARNING: High latency", "service": "api" }
-> { "type": "alert_sent", "in_reply_to": 2,
    "channel": "#alerts", "notification_id": "<uuid>",
    "actions": ["Acknowledge", "View Details"] }

// 15 分钟无人响应 -> 升级到下一级别
{ "type": "escalate_incident", "msg_id": 3,
  "incident_id": "INC123", "current_level": 1,
  "timeout_minutes": 15, "no_response": true }
-> { "type": "incident_escalated", "in_reply_to": 3,
    "incident_id": "INC123",
    "from_level": 1, "to_level": 2,
    "escalated_to": "team-lead@example.com" }
```

## 概念说明

**告警集成**就像医院的急救呼叫系统：患者（告警）到来后，分诊台根据严重程度决定通知谁——危急的直接呼叫主治医生（PagerDuty），一般的通知护士站（Slack）。**升级策略**则确保没人接手时，告警会自动上报给更高级别的负责人，避免问题被遗漏。

## 涉及概念

- `PagerDuty`
- `Slack`
- `on-call rotation`
- `escalation policy`
- `incident lifecycle`

## 实现提示

- create_incident 返回 incident_id、status=triggered，以及被分配的值班人员
- send_alert 生成包含操作按钮的 Slack 消息，按钮为 Acknowledge 和 View Details
- get_on_call 查询指定团队在特定时间的当前值班人员
- 升级策略：超时无人响应后，将事件升级到策略中的下一个级别
- Slack 响应中的 notification_id 每条消息应当唯一

## 测试用例

### 1. PagerDuty 告警集成

应当创建 PagerDuty 事件并分配给值班工程师。

输入：

```json
{"src":"alerter","dest":"pagerduty","body":{"type":"create_incident","msg_id":1,"title":"High error rate","service":"api","severity":"critical","description":"Error rate is 15% (threshold: 5%)"}}
```

期望输出：

```text
{"type": "incident_created", "in_reply_to": 1, "incident_id": "INC123", "status": "triggered", "assigned_to": "on-call-engineer"}
```

### 2. Slack 告警通知

应当发送格式化的 Slack 告警消息并附带操作按钮。

输入：

```json
{"src":"alerter","dest":"slack","body":{"type":"send_alert","msg_id":1,"channel":"#alerts","title":"WARNING: High latency","severity":"warning","description":"P95 latency is 500ms (threshold: 200ms)","service":"api"}}
```

期望输出：

```text
{"type": "alert_sent", "in_reply_to": 1, "channel": "#alerts", "notification_id": ".*", "actions": ["Acknowledge", "View Details"]}
```

## 参考资料

- [PagerDuty API](https://developer.pagerduty.com/api-reference/)：PagerDuty 的事件创建和值班管理接口文档
- [Slack API Webhooks](https://api.slack.com/messaging/webhooks)：Slack 传入 Webhook 文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
