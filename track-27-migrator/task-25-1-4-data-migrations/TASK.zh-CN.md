# 实现 Data Migrations

英文标题：Implement Data Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-4-data-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：4
短标题：Data Migrations
难度：advanced
子主题：Schema Migrations

## 中文导读

本题要求你完成 `实现 Data Migrations`。

重点关注：`data backfill`、`batch processing`、`idempotent migration`、`data validation`、`rollback on failure`。

建议先按提示逐步实现：Backfill in batches: process rows WHERE id > last_processed_id LIMIT batch_size。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Data migrations transform existing data to match a new schema or business rule. Unlike schema migrations, they touch every row. Running them during peak traffic causes lock contention — so they must run in small batches, be idempotent (safe to re-run),和be validated before the old schema is removed.

Implement a 节点 that manages data migrations:

```JSON
// Backfill full_name column用于10,000 existing users in batches
{ "type": "backfill", "msg_id": 1,
  "table": "users", "column": "full_name",
  "batch_size": 1000, "total_rows": 10000 }
-> { "type": "backfill_complete", "in_reply_to": 1,
    "total_processed": 10000, "total_updated": 9500,
    "duration_seconds": 60 }

// Validate the migrated data meets constraints
{ "type": "validate", "msg_id": 2,
  "table": "users",
  "validations": ["no_nulls", "email_format"] }
-> { "type": "validation_results", "in_reply_to": 2,
    "results": [
      {"name": "no_nulls", "passed": true, "failed_rows": 0},
      {"name": "email_format", "passed": true, "failed_rows": 0}
    ]}

// Running migration 3 times produces the same final state
{ "type": "migrate", "msg_id": 3,
  "idempotent": true, "table": "users", "runs": 3 }
-> { "type": "migration_complete", "in_reply_to": 3,
    "rows_updated": 100, "final_state": "unchanged" }
```

## 涉及概念

- `data backfill`
- `batch processing`
- `idempotent migration`
- `data validation`
- `rollback on failure`

## 实现提示

- Backfill in batches: process rows WHERE id > last_processed_id LIMIT batch_size
- Track total_processed和total_updated separately (some rows may already be correct)
- Idempotent: running the migration twice should produce the same result, not double-update
- Validate after migration: check constraints like no_nulls和format rules
- Rollback on validation 故障: restore from backup if post-migration checks fail

## 测试用例

### 1. Backfill data in batches

Should backfill 10000 rows in batches和report processed vs updated counts.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"backfill","msg_id":1,"table":"users","column":"full_name","batch_size":1000,"total_rows":10000}}
```

期望输出：

```text
{"type": "backfill_complete", "in_reply_to": 1, "total_processed": 10000, "total_updated": 9500, "duration_seconds": 60}
```

### 2. Validate migrated data

Both validation rules should pass，包含zero failed rows.

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"validate","msg_id":1,"table":"users","validations":["no_nulls","email_format"]}}
```

期望输出：

```text
{"type": "validation_results", "in_reply_to": 1, "results": [{"name": "no_nulls", "passed": true, "failed_rows": 0}, {"name": "email_format", "passed": true, "failed_rows": 0}]}
```

## 参考资料

- [Database Migrations](https://martinfowler.com/articles/evodb.html)：Evolutionary database design: schema和data migrations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
