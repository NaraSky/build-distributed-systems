# Implement Alert Integrations and On-Call Management

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-5-alert-integrations>

Track: 25. The Tracer
Task order: 10
Short title: Alert Integrations
Difficulty: intermediate
Subtrack: Metrics and Alerting

## Problem

Alert integrations route notifications to the right people and tools. Critical incidents trigger PagerDuty to page the on-call engineer. Non-critical alerts post to Slack for team visibility with action buttons. If no one responds, escalation policies ensure the alert keeps moving up the chain.

Implement a node that handles alert routing and on-call management:

```json
// CRITICAL alert -> PagerDuty incident
{ "type": "create_incident", "msg_id": 1,
  "title": "High error rate", "service": "api",
  "severity": "critical",
  "description": "Error rate is 15% (threshold: 5%)" }
-> { "type": "incident_created", "in_reply_to": 1,
    "incident_id": "INC123", "status": "triggered",
    "assigned_to": "on-call-engineer" }

// WARNING alert -> Slack channel with action buttons
{ "type": "send_alert", "msg_id": 2,
  "channel": "#alerts", "severity": "warning",
  "title": "WARNING: High latency", "service": "api" }
-> { "type": "alert_sent", "in_reply_to": 2,
    "channel": "#alerts", "notification_id": "<uuid>",
    "actions": ["Acknowledge", "View Details"] }

// No response after 15 min -> escalate to next level
{ "type": "escalate_incident", "msg_id": 3,
  "incident_id": "INC123", "current_level": 1,
  "timeout_minutes": 15, "no_response": true }
-> { "type": "incident_escalated", "in_reply_to": 3,
    "incident_id": "INC123",
    "from_level": 1, "to_level": 2,
    "escalated_to": "team-lead@example.com" }
```

## Concepts

- PagerDuty
- Slack
- on-call rotation
- escalation policy
- incident lifecycle

## Hints

- create_incident returns incident_id, status=triggered, and the assigned on-call user
- send_alert formats a Slack message with action buttons: Acknowledge and View Details
- get_on_call looks up who is currently on-call for a team at a specific time
- Escalation: after timeout with no response, escalate to the next level in the policy
- notification_id in Slack response should be unique per message

## Test Cases

### 1. PagerDuty alert integration

Should create PagerDuty incident and assign to on-call engineer.

Input:

```json
{"src":"alerter","dest":"pagerduty","body":{"type":"create_incident","msg_id":1,"title":"High error rate","service":"api","severity":"critical","description":"Error rate is 15% (threshold: 5%)"}}
```

Expected output:

```text
{"type": "incident_created", "in_reply_to": 1, "incident_id": "INC123", "status": "triggered", "assigned_to": "on-call-engineer"}
```

### 2. Slack alert notification

Should send formatted Slack alert with action buttons.

Input:

```json
{"src":"alerter","dest":"slack","body":{"type":"send_alert","msg_id":1,"channel":"#alerts","title":"WARNING: High latency","severity":"warning","description":"P95 latency is 500ms (threshold: 200ms)","service":"api"}}
```

Expected output:

```text
{"type": "alert_sent", "in_reply_to": 1, "channel": "#alerts", "notification_id": ".*", "actions": ["Acknowledge", "View Details"]}
```

## Resources

- [PagerDuty API](https://developer.pagerduty.com/api-reference/): PagerDuty API for incident creation and on-call management
- [Slack API Webhooks](https://api.slack.com/messaging/webhooks): Slack incoming webhooks documentation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
