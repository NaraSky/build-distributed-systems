# 实现迁移回滚策略

英文标题：Implement Migration Rollback Strategies
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-5-rollback-strategies>

课程：27. 迁移器：数据与协议演进
任务序号：5
短标题：Rollback Strategies
难度：高级
子主题：Schema Migrations

## 中文导读

这道题要求你实现一个支持多种回滚策略的节点。当生产环境的迁移出了问题，你需要一个回滚方案。不同的情况需要不同的策略：功能开关（Feature Flag）可以即时关闭、蓝绿部署可以秒级切换流量、迁移脚本的 `down()` 函数可以撤销模式变更、数据库还原是最后的手段。掌握这些策略能帮你在紧急情况下快速止损。

## 题目说明

当生产环境中的迁移出现问题时，你需要一个回滚方案。不同的场景需要不同的策略：行为变更可以通过即时关闭功能开关（Feature Flag）来回滚，部署问题可以通过蓝绿部署切换流量来解决，模式变更可以运行迁移的 `down()` 函数来撤销，严重的数据损坏则需要从备份还原数据库。

请实现一个支持四种回滚策略的节点：

```json
// 1. 迁移回滚：执行版本 3 的 down() 函数
{ "type": "rollback", "msg_id": 1, "version": 3 }
-> { "type": "rollback_complete", "in_reply_to": 1,
    "rolled_back_from": 3, "rolled_back_to": 2,
    "duration_seconds": 5 }

// 2. 功能开关回滚：即时禁用功能
{ "type": "disable_feature", "msg_id": 2,
  "feature": "new_checkout" }
-> { "type": "feature_disabled", "in_reply_to": 2,
    "feature": "new_checkout", "rolled_back_instant": true }

// 3. 蓝绿部署：将流量切换回上一个环境
{ "type": "switch_traffic", "msg_id": 3,
  "from": "green", "to": "blue" }
-> { "type": "traffic_switched", "in_reply_to": 3,
    "current_environment": "blue", "downtime_seconds": 0 }

// 4. 从备份还原（最后手段）
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

- 迁移回滚：执行目标版本的 `down()` 函数
- 功能开关回滚：无需重新部署，即时禁用对应的功能开关
- 蓝绿部署：维护两个完全相同的环境，可以在几秒内将流量从新环境切换回旧环境
- 数据库还原是最后手段：从迁移前的备份恢复数据
- 回滚策略从即时（功能开关）到耗时（数据库还原）不等

## 测试用例

### 1. 回滚迁移

应执行版本 3 的 `down()` 函数，将数据库回退到版本 2。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"rollback","msg_id":1,"version":3}}
```

期望输出：

```text
{"type": "rollback_complete", "in_reply_to": 1, "rolled_back_from": 3, "rolled_back_to": 2, "duration_seconds": 5}
```

### 2. 功能开关回滚

应即时禁用功能开关，无需重新部署。

输入：

```json
{"src":"admin","dest":"features","body":{"type":"disable_feature","msg_id":1,"feature":"new_checkout"}}
```

期望输出：

```text
{"type": "feature_disabled", "in_reply_to": 1, "feature": "new_checkout", "rolled_back_instant": true}
```

## 参考资料

- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)：Martin Fowler 介绍的蓝绿部署模式，用于实现零停机回滚

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
