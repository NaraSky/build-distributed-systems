# 实现数据迁移

英文标题：Implement Data Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-4-data-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：4
短标题：Data Migrations
难度：高级
子主题：Schema Migrations

## 中文导读

这道题要求你实现一个管理数据迁移（Data Migration）的节点。与模式迁移不同，数据迁移需要对每一行现有数据进行转换。在高峰流量时直接跑全量迁移会导致严重的锁竞争，因此必须分批执行、保证幂等性（重复执行不会出错），并在移除旧模式前进行数据验证。这是大规模数据库演进中不可或缺的一环。

## 题目说明

数据迁移将现有数据转换为符合新模式或新业务规则的格式。与模式迁移不同，数据迁移需要处理每一行数据。在高峰流量期间执行数据迁移会导致锁竞争，因此必须分小批次执行，保证幂等性（可以安全地重复执行），并在移除旧模式之前验证数据。

请实现一个管理数据迁移的节点：

```json
// 分批为 10000 个现有用户回填 full_name 列
{ "type": "backfill", "msg_id": 1,
  "table": "users", "column": "full_name",
  "batch_size": 1000, "total_rows": 10000 }
-> { "type": "backfill_complete", "in_reply_to": 1,
    "total_processed": 10000, "total_updated": 9500,
    "duration_seconds": 60 }

// 验证迁移后的数据是否满足约束条件
{ "type": "validate", "msg_id": 2,
  "table": "users",
  "validations": ["no_nulls", "email_format"] }
-> { "type": "validation_results", "in_reply_to": 2,
    "results": [
      {"name": "no_nulls", "passed": true, "failed_rows": 0},
      {"name": "email_format", "passed": true, "failed_rows": 0}
    ]}

// 执行迁移 3 次，最终状态应保持不变（幂等性）
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

- 分批回填数据：使用 `WHERE id > last_processed_id LIMIT batch_size` 逐批处理
- 分别追踪已处理总数和实际更新数（有些行可能已经是正确的值）
- 幂等性：执行两次迁移应该产生相同的结果，不会重复更新
- 迁移后进行验证：检查非空约束和格式规则等
- 验证失败时回滚：如果迁移后检查不通过，从备份恢复数据

## 测试用例

### 1. 分批回填数据

应分批回填 10000 行数据，并分别报告已处理数和实际更新数。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"backfill","msg_id":1,"table":"users","column":"full_name","batch_size":1000,"total_rows":10000}}
```

期望输出：

```text
{"type": "backfill_complete", "in_reply_to": 1, "total_processed": 10000, "total_updated": 9500, "duration_seconds": 60}
```

### 2. 验证迁移后的数据

两条验证规则都应通过，且没有失败的行。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"validate","msg_id":1,"table":"users","validations":["no_nulls","email_format"]}}
```

期望输出：

```text
{"type": "validation_results", "in_reply_to": 1, "results": [{"name": "no_nulls", "passed": true, "failed_rows": 0}, {"name": "email_format", "passed": true, "failed_rows": 0}]}
```

## 参考资料

- [Database Migrations](https://martinfowler.com/articles/evodb.html)：演进式数据库设计，涵盖模式迁移和数据迁移

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
