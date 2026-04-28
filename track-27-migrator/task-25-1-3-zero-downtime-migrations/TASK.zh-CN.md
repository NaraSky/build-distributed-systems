# 实现 Zero-Downtime Database Migrations

英文标题：Implement Zero-Downtime Database Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-3-zero-downtime-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：3
短标题：Zero-Downtime Migrations
难度：advanced
子主题：Schema Migrations

## 中文导读

本题要求你完成 `实现 Zero-Downtime Database Migrations`。

重点关注：`concurrent index`、`lock-free migrations`、`batch data migration`、`lock-aware migration`。

建议先按提示逐步实现：CREATE 索引 CONCURRENTLY builds the 索引 without holding an exclusive table lock。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A naive `ALTER TABLE ADD COLUMN NOT NULL DEFAULT 'x'` rewrites the entire table和holds an exclusive lock, blocking all reads和writes. Zero-downtime migrations use PostgreSQL features to make schema changes without taking the table offline.

Implement a 节点 that performs lock-safe schema changes:

```JSON
// Create 索引 without locking the table
{ "type": "create_index", "msg_id": 1,
  "table": "users", "column": "email", "concurrently": true }
-> { "type": "index_created", "in_reply_to": 1,
    "索引": "idx_email", "duration_seconds": 120,
    "table_locked": false }

// Add NOT NULL column，包含default — no table rewrite needed
{ "type": "add_column", "msg_id": 2,
  "table": "users", "column": "status",
  "default": "active", "nullable": false }
-> { "type": "column_added", "in_reply_to": 2,
    "duration_seconds": 0.1, "table_rewritten": false }

// Migrate data in batches to avoid long locks
{ "type": "migrate_data", "msg_id": 3,
  "table": "users", "batch_size": 1000, "total_rows": 10000 }
-> { "type": "data_migrated", "in_reply_to": 3,
    "total_rows": 10000, "batches": 10, "table_locked": false }
```

Lock-aware migration: if a lock cannot be acquired within `max_lock_duration_ms`, abort和roll back rather than blocking the application.

## 涉及概念

- `concurrent index`
- `lock-free migrations`
- `batch data migration`
- `lock-aware migration`

## 实现提示

- CREATE 索引 CONCURRENTLY builds the 索引 without holding an exclusive table lock
- Adding a column，包含a 服务端-side default does not rewrite the table in PostgreSQL 11+
- Batch data migration: process rows in chunks (e.g. WHERE id BETWEEN x AND x+1000); sleep between batches
- Lock-aware migration: set a short lock 超时; abort if a lock cannot be acquired quickly
- table_locked: false confirms the operation did not block read/write access

## 测试用例

### 1. 创建 索引 concurrently

Concurrent 索引 creation should not lock the table.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"create_index","msg_id":1,"table":"users","column":"email","concurrently":true}}
```

期望输出：

```text
{"type": "index_created", "in_reply_to": 1, "index": "idx_email", "duration_seconds": 120, "table_locked": false}
```

### 2. 添加 column without table rewrite

Adding column，包含服务端-side default should not rewrite the table.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"add_column","msg_id":1,"table":"users","column":"status","default":"active","nullable":false}}
```

期望输出：

```text
{"type": "column_added", "in_reply_to": 1, "duration_seconds": 0.1, "table_rewritten": false}
```

## 参考资料

- [Zero-Downtime Migrations](https://www.citusdata.com/blog/2018/02/22/seven-tips-for-better-postgresql-migrations/)：Seven tips用于safer PostgreSQL migrations in production
- [pt-online-schema-change](https://www.percona.com/doc/percona-toolkit/LATEST/pt-online-schema-change.html)：Percona pt-online-schema-change documentation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
