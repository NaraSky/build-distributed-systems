# 实现 Database Schema Migrations

英文标题：Implement Database Schema Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-1-database-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：1
短标题：Schema Migrations
难度：intermediate
子主题：Schema Migrations

## 中文导读

本题要求你完成 `实现 Database Schema Migrations`。

重点关注：`schema migrations`、`migration versioning`、`up/down migrations`、`transaction safety`、`migration status`。

建议先按提示逐步实现：Migrations are applied in version order; track which ones have run in a migrations table。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Database migrations version-control schema changes. Each migration has an `up()` function that applies the change和a `down()` function that reverses it. A migrations table tracks which versions have been applied so you can apply pending ones or roll back the latest.

Implement a 节点 that manages database schema migrations:

```JSON
// Apply all pending migrations in version order
{ "type": "migrate", "msg_id": 1 }
-> { "type": "migrations_applied", "in_reply_to": 1,
    "count": 2,
    "migrations": [
      {"version": 1, "name": "create_users", "status": "applied"},
      {"version": 2, "name": "add_posts_table", "status": "applied"}
    ]}

// Rollback the most recently applied migration
{ "type": "rollback", "msg_id": 2 }
-> { "type": "migration_rolled_back", "in_reply_to": 2,
    "version": 2, "name": "add_posts_table" }

// Show applied和pending migrations
{ "type": "status", "msg_id": 3 }
-> { "type": "migration_status", "in_reply_to": 3,
    "migrations": [
      {"version": 1, "name": "create_users", "applied": true},
      {"version": 2, "name": "add_posts_table", "applied": false}
    ]}
```

If a migration fails partway through, the 事务 must be rolled back和the migration must NOT be recorded as applied.

## 涉及概念

- `schema migrations`
- `migration versioning`
- `up/down migrations`
- `transaction safety`
- `migration status`

## 实现提示

- Migrations are applied in version order; track which ones have run in a migrations table
- Each migration has an up() function (apply change)和down() function (undo change)
- Wrap each migration in a 事务; rollback the whole migration on any error
- migrate applies all pending migrations in order; rollback undoes the most recent one
- status lists all migrations，包含applied: true/false

## 测试用例

### 1. Apply pending migrations

Should apply both pending migrations in version order.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1}}
```

期望输出：

```text
{"type": "migrations_applied", "in_reply_to": 1, "count": 2, "migrations": [{"version": 1, "name": "create_users", "status": "applied"}, {"version": 2, "name": "add_posts_table", "status": "applied"}]}
```

### 2. Rollback migration

Should rollback the most recently applied migration.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"rollback","msg_id":1}}
```

期望输出：

```text
{"type": "migration_rolled_back", "in_reply_to": 1, "version": 2, "name": "add_posts_table"}
```

## 参考资料

- [Database Migrations](https://martinfowler.com/articles/evodb.html)：Evolutionary database design: managing schema changes over time

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
