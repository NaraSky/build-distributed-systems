# Implement Monitoring Dashboards and Visualization

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-4-dashboards-visualization>

Track: 25. The Tracer
Task order: 9
Short title: Dashboards
Difficulty: intermediate
Subtrack: Metrics and Alerting

## Problem

Dashboards aggregate multiple metric queries into a single health view. Each panel runs a different query (request rate, error rate, latency) and visualises it as a graph, gauge, or number. Template variables make one dashboard reusable across services or environments.

Implement a node that manages monitoring dashboards:

```json
// Create a dashboard with two panels
{ "type": "create_dashboard", "msg_id": 1,
  "name": "Service Overview",
  "panels": [
    {"id":1,"title":"Request Rate","type":"graph",
     "query":"rate(http_requests_total[5m])"},
    {"id":2,"title":"Error Rate","type":"gauge",
     "query":"rate(http_errors_total[5m])"}
  ] }
-> { "type": "dashboard_created", "in_reply_to": 1,
    "dashboard_id": "<uuid>", "panel_count": 2 }

// Query all panels for the last hour
{ "type": "query_dashboard", "msg_id": 2,
  "dashboard_id": "dash-123", "time_range": "1h" }
-> { "type": "dashboard_data", "in_reply_to": 2,
    "panels": [{"id": 1, "title": "Request Rate", "data_points": 60}] }

// Set auto-refresh to 30 seconds
{ "type": "refresh_dashboard", "msg_id": 3,
  "dashboard_id": "dash-123", "refresh_interval": "30s" }
-> { "type": "dashboard_refreshed", "in_reply_to": 3,
    "dashboard_id": "dash-123",
    "refresh_interval": "30s", "auto_refresh": true }
```

## Concepts

- dashboard
- panels
- template variables
- auto-refresh
- time range

## Hints

- create_dashboard stores the panel list and returns a unique dashboard_id
- query_dashboard runs each panel query for the time range and returns data_points
- Template variable $service lets one dashboard show data for any service
- refresh_dashboard configures auto-refresh; return auto_refresh: true to confirm
- panel_count = number of panels provided in the panels array

## Test Cases

### 1. Create dashboard with panels

Should create dashboard with 2 panels and return a unique dashboard_id.

Input:

```json
{"src":"ui","dest":"dashboards","body":{"type":"create_dashboard","msg_id":1,"name":"Service Overview","panels":[{"id":1,"title":"Request Rate","type":"graph","query":"rate(http_requests_total[5m])"},{"id":2,"title":"Error Rate","type":"gauge","query":"rate(http_errors_total[5m])"}]}}
```

Expected output:

```text
{"type": "dashboard_created", "in_reply_to": 1, "dashboard_id": ".*", "panel_count": 2}
```

### 2. Query dashboard data

Should return time-series data for each panel.

Input:

```json
{"src":"viewer","dest":"dashboards","body":{"type":"query_dashboard","msg_id":1,"dashboard_id":"dash-123","time_range":"1h"}}
```

Expected output:

```text
{"type": "dashboard_data", "in_reply_to": 1, "panels": [{"id": 1, "title": "Request Rate", "data_points": 60}]}
```

## Resources

- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/): Grafana dashboard concepts: panels, variables, and time ranges

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
