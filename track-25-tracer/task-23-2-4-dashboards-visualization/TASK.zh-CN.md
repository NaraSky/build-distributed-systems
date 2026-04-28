# 实现 Monitoring Dashboards和Visualization

英文标题：Implement Monitoring Dashboards和Visualization
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-4-dashboards-visualization>

课程：25. 追踪器：可观测性
任务序号：9
短标题：Dashboards
难度：intermediate
子主题：Metrics和Alerting

## 中文导读

本题要求你完成 `实现 Monitoring Dashboards和Visualization`。

重点关注：`dashboard`、`panels`、`template variables`、`auto-refresh`、`time range`。

建议先按提示逐步实现：create_dashboard stores the panel list和returns a unique dashboard_id。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Dashboards aggregate multiple metric queries into a single health view. Each panel runs a different query (请求 rate, error rate, latency)和visualises it as a graph, gauge, or number. Template variables make one dashboard reusable across services or environments.

Implement a 节点 that manages monitoring dashboards:

```JSON
// Create a dashboard，包含two panels
{ "type": "create_dashboard", "msg_id": 1,
  "name": "Service Overview",
  "panels": [
    {"id":1,"title":"请求 Rate","type":"graph",
     "query":"rate(http_requests_total[5m])"},
    {"id":2,"title":"Error Rate","type":"gauge",
     "query":"rate(http_errors_total[5m])"}
  ] }
-> { "type": "dashboard_created", "in_reply_to": 1,
    "dashboard_id": "<uuid>", "panel_count": 2 }

// Query all panels用于the last hour
{ "type": "query_dashboard", "msg_id": 2,
  "dashboard_id": "dash-123", "time_range": "1h" }
-> { "type": "dashboard_data", "in_reply_to": 2,
    "panels": [{"id": 1, "title": "请求 Rate", "data_points": 60}] }

// Set auto-refresh to 30 seconds
{ "type": "refresh_dashboard", "msg_id": 3,
  "dashboard_id": "dash-123", "refresh_interval": "30s" }
-> { "type": "dashboard_refreshed", "in_reply_to": 3,
    "dashboard_id": "dash-123",
    "refresh_interval": "30s", "auto_refresh": true }
```

## 涉及概念

- `dashboard`
- `panels`
- `template variables`
- `auto-refresh`
- `time range`

## 实现提示

- create_dashboard stores the panel list和returns a unique dashboard_id
- query_dashboard runs each panel query用于the time range和returns data_points
- Template variable $service lets one dashboard show data用于any service
- refresh_dashboard configures auto-refresh; return auto_refresh: true to confirm
- panel_count = number of panels provided in the panels array

## 测试用例

### 1. 创建 dashboard，包含panels

Should create dashboard，包含2 panels和return a unique dashboard_id.

输入：

```json
{"src":"ui","dest":"dashboards","body":{"type":"create_dashboard","msg_id":1,"name":"Service Overview","panels":[{"id":1,"title":"Request Rate","type":"graph","query":"rate(http_requests_total[5m])"},{"id":2,"title":"Error Rate","type":"gauge","query":"rate(http_errors_total[5m])"}]}}
```

期望输出：

```text
{"type": "dashboard_created", "in_reply_to": 1, "dashboard_id": ".*", "panel_count": 2}
```

### 2. Query dashboard data

Should return time-series data用于each panel.

输入：

```json
{"src":"viewer","dest":"dashboards","body":{"type":"query_dashboard","msg_id":1,"dashboard_id":"dash-123","time_range":"1h"}}
```

期望输出：

```text
{"type": "dashboard_data", "in_reply_to": 1, "panels": [{"id": 1, "title": "Request Rate", "data_points": 60}]}
```

## 参考资料

- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)：Grafana dashboard concepts: panels, variables,和time ranges

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
