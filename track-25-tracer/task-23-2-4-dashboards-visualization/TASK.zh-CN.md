# 实现监控仪表盘与可视化

英文标题：Implement Monitoring Dashboards and Visualization
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-4-dashboards-visualization>

课程：25. 追踪器：可观测性
任务序号：9
短标题：Dashboards
难度：进阶
子主题：Metrics and Alerting

## 中文导读

这道题要求你实现监控仪表盘的管理功能。仪表盘将多个指标查询汇聚到一个视图中，让你一眼就能看到系统的健康状况。每个面板运行不同的查询（请求速率、错误率、延迟等），并以图表、仪表或数字的形式展示。模板变量让同一个仪表盘可以在不同服务和环境间复用。

## 题目说明

仪表盘（Dashboard）将多个指标查询汇聚到一个统一的健康视图中。每个面板（Panel）运行不同的查询（请求速率、错误率、延迟），并以图表、仪表或数字的形式展示。模板变量使同一个仪表盘可以跨服务和环境复用。

请实现一个节点来管理监控仪表盘：

```json
// 创建一个包含两个面板的仪表盘
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

// 查询所有面板最近一小时的数据
{ "type": "query_dashboard", "msg_id": 2,
  "dashboard_id": "dash-123", "time_range": "1h" }
-> { "type": "dashboard_data", "in_reply_to": 2,
    "panels": [{"id": 1, "title": "Request Rate", "data_points": 60}] }

// 设置每 30 秒自动刷新
{ "type": "refresh_dashboard", "msg_id": 3,
  "dashboard_id": "dash-123", "refresh_interval": "30s" }
-> { "type": "dashboard_refreshed", "in_reply_to": 3,
    "dashboard_id": "dash-123",
    "refresh_interval": "30s", "auto_refresh": true }
```

## 概念说明

**仪表盘**就像汽车的仪表盘——把速度、油量、转速等关键信息集中展示在一个地方，让你不用翻日志就能快速了解系统状态。**模板变量**相当于一个下拉选择器，切换不同的服务名称就能查看不同服务的指标，不需要为每个服务单独创建仪表盘。

## 涉及概念

- `dashboard`
- `panels`
- `template variables`
- `auto-refresh`
- `time range`

## 实现提示

- create_dashboard 存储面板列表并返回唯一的 dashboard_id
- query_dashboard 在指定时间范围内运行每个面板的查询并返回 data_points
- 模板变量 $service 使同一个仪表盘可以展示任意服务的数据
- refresh_dashboard 配置自动刷新；返回 `auto_refresh: true` 表示确认
- panel_count 等于 panels 数组中提供的面板数量

## 测试用例

### 1. 创建带面板的仪表盘

应当创建包含 2 个面板的仪表盘并返回唯一的 dashboard_id。

输入：

```json
{"src":"ui","dest":"dashboards","body":{"type":"create_dashboard","msg_id":1,"name":"Service Overview","panels":[{"id":1,"title":"Request Rate","type":"graph","query":"rate(http_requests_total[5m])"},{"id":2,"title":"Error Rate","type":"gauge","query":"rate(http_errors_total[5m])"}]}}
```

期望输出：

```text
{"type": "dashboard_created", "in_reply_to": 1, "dashboard_id": ".*", "panel_count": 2}
```

### 2. 查询仪表盘数据

应当返回每个面板的时间序列数据。

输入：

```json
{"src":"viewer","dest":"dashboards","body":{"type":"query_dashboard","msg_id":1,"dashboard_id":"dash-123","time_range":"1h"}}
```

期望输出：

```text
{"type": "dashboard_data", "in_reply_to": 1, "panels": [{"id": 1, "title": "Request Rate", "data_points": 60}]}
```

## 参考资料

- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)：介绍 Grafana 仪表盘的概念，包括面板、变量和时间范围

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
