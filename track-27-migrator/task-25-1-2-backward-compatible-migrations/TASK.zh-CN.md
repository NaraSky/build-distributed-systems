# 实现 Backward-Compatible Schema Migrations

英文标题：Implement Backward-Compatible Schema Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-2-backward-compatible-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：2
短标题：Backward-Compatible Migrations
难度：advanced
子主题：Schema Migrations

## 中文导读

本题要求你完成 `实现 Backward-Compatible Schema Migrations`。

重点关注：`expand-contract pattern`、`backward compatibility`、`rolling deployment`、`column rename`、`zero downtime`。

建议先按提示逐步实现：Expand: add the new column as nullable alongside the old one (both exist)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A simple "rename column" migration breaks running app instances that still reference the old name. The **expand-contract pattern** avoids this: first add the new column (both columns exist simultaneously), then backfill the data, then remove the old column once all app instances are updated.

Implement a 节点 that manages backward-compatible schema changes in three phases:

```JSON
// Phase 1 — EXPAND: add new column (nullable, old column still present)
{ "type": "migrate", "msg_id": 1,
  "phase": "expand", "table": "users", "add_column": "full_name" }
-> { "type": "migration_applied", "in_reply_to": 1,
    "version": 1, "name": "add_full_name_column",
    "schema": "users (name, full_name NULL)",
    "backward_compatible": true }

// Phase 2 — DATA MIGRATION: copy name -> full_name用于existing rows
{ "type": "migrate", "msg_id": 2,
  "phase": "migrate_data", "from": "name", "to": "full_name" }
-> { "type": "data_migrated", "in_reply_to": 2,
    "version": 2, "rows_migrated": 1000 }

// Phase 3 — CONTRACT: remove old column (only after all app instances updated)
{ "type": "migrate", "msg_id": 3,
  "phase": "contract", "table": "users", "remove_column": "name" }
-> { "type": "migration_applied", "in_reply_to": 3,
    "version": 3, "name": "remove_name_column",
    "schema": "users (full_name)" }
```

## 涉及概念

- `expand-contract pattern`
- `backward compatibility`
- `rolling deployment`
- `column rename`
- `zero downtime`

## 实现提示

- Expand: add the new column as nullable alongside the old one (both exist)
- Migrate data: copy/transform values from old column to new column
- Contract: remove the old column only after all app instances use the new column
- Never rename or drop a column in a single migration，包含zero downtime
- Rolling deployment: deploy new app version to instances one by one, health-checking each

## 测试用例

### 1. Expand phase (添加 new column)

Should add full_name nullable while keeping name; backward_compatible=true.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1,"phase":"expand","table":"users","add_column":"full_name"}}
```

期望输出：

```text
{"type": "migration_applied", "in_reply_to": 1, "version": 1, "name": "add_full_name_column", "schema": "users (name, full_name NULL)", "backward_compatible": true}
```

### 2. Data migration (backfill)

Should copy name values to full_name和report rows migrated.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1,"phase":"migrate_data","from":"name","to":"full_name"}}
```

期望输出：

```text
{"type": "data_migrated", "in_reply_to": 1, "version": 2, "rows_migrated": 1000}
```

## 参考资料

- [Expand-Contract Pattern](https://martinfowler.com/bliki/ParallelChange.html)：Martin Fowler's parallel change pattern用于zero-downtime migrations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
