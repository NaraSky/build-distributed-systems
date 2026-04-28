# 实现 Client Migration Strategy

英文标题：Implement Client Migration Strategy
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-5-client-migration>

课程：27. 迁移器：数据与协议演进
任务序号：10
短标题：Client Migration
难度：advanced
子主题：Protocol和API Evolution

## 中文导读

本题要求你完成 `实现 Client Migration Strategy`。

重点关注：`canary deployment`、`traffic splitting`、`migration tracking`、`gradual rollout`、`health checks`。

建议先按提示逐步实现：Canary: route 10% of traffic to v2 (hash user_id % 100 < 10); rest to v1。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Migrating clients from API v1 to v2 should be gradual和safe. Canary deployments start，包含a small percentage of traffic; a/b testing routes specific users deterministically; tracking migration progress shows when it is safe to fully sunset v1.

Implement a 节点 that manages 客户端 migration across API versions:

```JSON
// Canary at 10%: most traffic stays on v1
{ "type": "get_users", "msg_id": 1, "user_id": "user123" }
{ canary_percentage: 10 }
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v1", "canary": false }

// 50/50 traffic split
{ "type": "get_users", "msg_id": 2 }
{ traffic_split: {"v1": 50, "v2": 50} }
-> { "type": "users_response", "in_reply_to": 2,
    "version": "<v1 or v2>" }

// Track how many clients have migrated
{ "type": "get_migration_stats", "msg_id": 3 }
-> { "type": "migration_stats", "in_reply_to": 3,
    "total_clients": 1000,
    "version_percentages": {"v1": 20, "v2": 80},
    "migration_complete": false }

// Gradual rollout，包含health checks between steps
{ "type": "gradual_rollout", "msg_id": 4,
  "steps": [{"percentage":10,"duration_minutes":60},
              {"percentage":50,"duration_minutes":240}] }
-> { "type": "rollout_complete", "in_reply_to": 4,
    "final_percentage": 50, "health_checks_passed": true }
```

## 涉及概念

- `canary deployment`
- `traffic splitting`
- `migration tracking`
- `gradual rollout`
- `health checks`

## 实现提示

- Canary: route 10% of traffic to v2 (hash user_id % 100 < 10); rest to v1
- Traffic split: use a random number per 请求和route by bucket percentage
- migration stats: count requests by version over time; migration_complete when v1 usage drops to 0
- Gradual rollout: each step increases the v2 percentage after checking health metrics
- health_checks_passed: true means no error rate increase was detected during rollout

## 测试用例

### 1. Canary deployment routing

At 10% canary, most users (including user123) should stay on v1.

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"user_id":"user123"},"canary_percentage":10}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": "v1", "canary": false}
```

### 2. Traffic splitting

Should split traffic 50/50和return either v1 or v2.

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1},"traffic_split":{"v1":50,"v2":50}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": ".*"}
```

## 参考资料

- [Canary Release](https://martinfowler.com/bliki/CanaryRelease.html)：Gradual traffic shifting to safely roll out API changes
- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)：Martin Fowler on Blue-Green Deployment

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
