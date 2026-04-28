# 实现数据库模式迁移

英文标题：Implement Database Schema Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-1-database-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：1
短标题：Schema Migrations
难度：进阶
子主题：Schema Migrations

## 中文导读

这道题要求你实现一个管理数据库模式迁移（Schema Migration）的节点。模式迁移就像给数据库做"版本管理"，每次修改表结构都会记录一个版本号，可以按顺序执行未完成的迁移，也可以回滚最近一次的修改。这在实际项目中至关重要，因为它确保了团队协作时数据库结构变更的可追踪性和可逆性。

## 题目说明

数据库迁移（Database Migration）是对数据库模式变更进行版本控制的机制。每个迁移包含一个 `up()` 函数用于执行变更，以及一个 `down()` 函数用于撤销变更。系统通过一张迁移记录表来追踪哪些版本已经被执行过，这样你就可以执行所有待处理的迁移，或者回滚最近一次迁移。

请实现一个管理数据库模式迁移的节点：

```json
// 按版本顺序执行所有待处理的迁移
{ "type": "migrate", "msg_id": 1 }
-> { "type": "migrations_applied", "in_reply_to": 1,
    "count": 2,
    "migrations": [
      {"version": 1, "name": "create_users", "status": "applied"},
      {"version": 2, "name": "add_posts_table", "status": "applied"}
    ]}

// 回滚最近一次执行的迁移
{ "type": "rollback", "msg_id": 2 }
-> { "type": "migration_rolled_back", "in_reply_to": 2,
    "version": 2, "name": "add_posts_table" }

// 查看所有迁移的状态（已执行和待处理）
{ "type": "status", "msg_id": 3 }
-> { "type": "migration_status", "in_reply_to": 3,
    "migrations": [
      {"version": 1, "name": "create_users", "applied": true},
      {"version": 2, "name": "add_posts_table", "applied": false}
    ]}
```

如果某个迁移在执行过程中失败了，必须回滚整个事务（Transaction），并且不能将该迁移记录为已执行。

## 涉及概念

- `schema migrations`
- `migration versioning`
- `up/down migrations`
- `transaction safety`
- `migration status`

## 实现提示

- 迁移按版本号顺序执行，通过一张迁移记录表追踪哪些迁移已经运行过
- 每个迁移包含一个 `up()` 函数（执行变更）和一个 `down()` 函数（撤销变更）
- 每个迁移都要包裹在事务中，任何错误都要回滚整个迁移
- `migrate` 按顺序执行所有待处理的迁移，`rollback` 撤销最近一次执行的迁移
- `status` 列出所有迁移，并标注每个迁移的执行状态

## 测试用例

### 1. 执行待处理的迁移

应按版本顺序执行两个待处理的迁移。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1}}
```

期望输出：

```text
{"type": "migrations_applied", "in_reply_to": 1, "count": 2, "migrations": [{"version": 1, "name": "create_users", "status": "applied"}, {"version": 2, "name": "add_posts_table", "status": "applied"}]}
```

### 2. 回滚迁移

应回滚最近一次执行的迁移。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"rollback","msg_id":1}}
```

期望输出：

```text
{"type": "migration_rolled_back", "in_reply_to": 1, "version": 2, "name": "add_posts_table"}
```

## 参考资料

- [Database Migrations](https://martinfowler.com/articles/evodb.html)：演进式数据库设计，介绍如何管理随时间变化的数据库模式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
