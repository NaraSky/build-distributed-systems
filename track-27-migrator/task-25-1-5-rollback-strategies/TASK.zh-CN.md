# 实现 Migration Rollback Strategies

英文标题：Implement Migration Rollback Strategies
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-5-rollback-strategies>

课程：27. 迁移器：数据与协议演进
任务序号：5
短标题：Rollback Strategies
难度：advanced
子主题：Schema Migrations

## 中文导读

本题要求你完成 `实现 Migration Rollback Strategies`。

重点关注：`migration rollback`、`feature flags`、`blue-green deployment`、`database restore`、`instant rollback`。

建议先按提示逐步实现：Migration rollback: run the down() function用于the target version。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a migration goes wrong in production, you need a rollback plan. Different situations call用于different strategies: instant feature flag disables用于behavioural changes, blue-green traffic switch用于deployment issues, migration down() functions用于schema changes,和database restore用于catastrophic data corruption.

Implement a 节点 that supports four rollback strategies:

```JSON
// 1. Migration rollback: run down()用于version 3
{ "type": "rollback", "msg_id": 1, "version": 3 }
-> { "type": "rollback_complete", "in_reply_to": 1,
    "rolled_back_from": 3, "rolled_back_to": 2,
    "duration_seconds": 5 }

// 2. Feature flag rollback: disable instantly
{ "type": "disable_feature", "msg_id": 2,
  "feature": "new_checkout" }
-> { "type": "feature_disabled", "in_reply_to": 2,
    "feature": "new_checkout", "rolled_back_instant": true }

// 3. Blue-green: switch traffic back to the previous environment
{ "type": "switch_traffic", "msg_id": 3,
  "from": "green", "to": "blue" }
-> { "type": "traffic_switched", "in_reply_to": 3,
    "current_environment": "blue", "downtime_seconds": 0 }

// 4. Restore from backup (last resort)
{ "type": "restore", "msg_id": 4,
  "backup": "users_backup_20240115" }
-> { "type": "restore_complete", "in_reply_to": 4,
    "restored_rows": 100000, "duration_seconds": 60 }
```

## 涉及概念

- `migration rollback`
- `feature flags`
- `blue-green deployment`
- `database restore`
- `instant rollback`

## 实现提示

- Migration rollback: run the down() function用于the target version
- Feature flag rollback: disable the flag instantly without a deployment
- Blue-green: two identical environments; switch traffic from green back to blue in seconds
- Database restore is the last resort: restore from a pre-migration backup
- Rollback strategies range from instant (feature flag) to slow (database restore)

## 测试用例

### 1. Rollback migration

Should run down()用于version 3和leave database at version 2.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"rollback","msg_id":1,"version":3}}
```

期望输出：

```text
{"type": "rollback_complete", "in_reply_to": 1, "rolled_back_from": 3, "rolled_back_to": 2, "duration_seconds": 5}
```

### 2. Feature flag rollback

Feature flag should be disabled instantly without redeployment.

输入：

```json
{"src":"admin","dest":"features","body":{"type":"disable_feature","msg_id":1,"feature":"new_checkout"}}
```

期望输出：

```text
{"type": "feature_disabled", "in_reply_to": 1, "feature": "new_checkout", "rolled_back_instant": true}
```

## 参考资料

- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)：Martin Fowler's blue-green deployment pattern用于zero-downtime rollback

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
