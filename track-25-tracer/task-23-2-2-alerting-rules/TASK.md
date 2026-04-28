# Implement Alerting Rules Engine

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-2-alerting-rules>

Track: 25. The Tracer
Task order: 7
Short title: Alerting Rules
Difficulty: intermediate
Subtrack: Metrics and Alerting

## Problem

An alerting rules engine evaluates metric conditions and fires notifications when thresholds are breached. It routes alerts to the right channel based on severity, groups duplicate alerts to prevent storms, and auto-resolves when conditions return to normal.

Implement a node that evaluates alert rules and manages notifications:

```json
// Error rate above threshold for 5 minutes -> WARNING
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

## Concepts

- alert rules
- threshold evaluation
- alert routing
- alert grouping
- auto-resolution

## Hints

- Fire alert when metric > threshold for at least duration_sec seconds
- Route CRITICAL severity to PagerDuty (pager); WARNING to Slack or email
- Grouping: alerts with the same fingerprint are merged into one notification
- Resolution: fire alert_resolved when the metric returns below threshold
- severity is determined by which threshold band the value falls in

## Test Cases

### 1. Threshold alert triggered

Error rate 0.08 exceeds threshold 0.05 for 300s -> WARNING.

Input:

```json
{"src":"metrics","dest":"alerter","body":{"type":"evaluate","msg_id":1,"metric":"error_rate","value":0.08,"threshold":0.05,"duration_sec":300}}
```

Expected output:

```text
{"type": "alert_triggered", "in_reply_to": 1, "rule": "High error rate", "severity": "WARNING", "value": 0.08}
```

### 2. Alert routing to PagerDuty

Service down is CRITICAL and should page on-call via PagerDuty.

Input:

```json
{"src":"metrics","dest":"alerter","body":{"type":"evaluate","msg_id":1,"metric":"up","value":0,"threshold":0,"duration_sec":60,"service":"api"},"routing":{"channels":["pagerduty"]}}
```

Expected output:

```text
{"type": "alert_triggered", "in_reply_to": 1, "severity": "CRITICAL", "action": "page_sent", "service": "api"}
```

## Resources

- [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/): Alertmanager routing, grouping, and deduplication

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
