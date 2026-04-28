# 实现零停机数据库迁移

英文标题：Implement Zero-Downtime Database Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-3-zero-downtime-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：3
短标题：Zero-Downtime Migrations
难度：高级
子主题：Schema Migrations

## 中文导读

这道题要求你实现一个能够在不停机的情况下执行数据库模式变更的节点。在生产环境中，一条简单的 `ALTER TABLE` 语句可能会锁住整张表，导致所有读写操作被阻塞。零停机迁移利用数据库的高级特性（如并发索引创建、批量数据迁移等）来避免这种情况，是大规模系统运维的必备技能。

## 题目说明

一条简单的 `ALTER TABLE ADD COLUMN NOT NULL DEFAULT 'x'` 语句会重写整张表并持有排他锁，阻塞所有读写操作。零停机迁移（Zero-Downtime Migration）利用数据库的特性来执行模式变更，而不会让表离线。

请实现一个执行无锁模式变更的节点：

```json
// 不锁表地创建索引
{ "type": "create_index", "msg_id": 1,
  "table": "users", "column": "email", "concurrently": true }
-> { "type": "index_created", "in_reply_to": 1,
    "index": "idx_email", "duration_seconds": 120,
    "table_locked": false }

// 添加带默认值的非空列，无需重写表
{ "type": "add_column", "msg_id": 2,
  "table": "users", "column": "status",
  "default": "active", "nullable": false }
-> { "type": "column_added", "in_reply_to": 2,
    "duration_seconds": 0.1, "table_rewritten": false }

// 分批迁移数据以避免长时间锁定
{ "type": "migrate_data", "msg_id": 3,
  "table": "users", "batch_size": 1000, "total_rows": 10000 }
-> { "type": "data_migrated", "in_reply_to": 3,
    "total_rows": 10000, "batches": 10, "table_locked": false }
```

锁感知迁移：如果在 `max_lock_duration_ms` 时间内无法获取锁，应中止并回滚，而不是阻塞应用程序。

## 涉及概念

- `concurrent index`
- `lock-free migrations`
- `batch data migration`
- `lock-aware migration`

## 实现提示

- `CREATE INDEX CONCURRENTLY` 可以在不持有排他表锁的情况下构建索引
- 在 PostgreSQL 11 及以上版本中，添加带服务端默认值的列不会重写表
- 批量数据迁移：分块处理行数据（例如 `WHERE id BETWEEN x AND x+1000`），批次之间适当休眠
- 锁感知迁移：设置较短的锁超时时间，如果无法快速获取锁则中止操作
- `table_locked: false` 表示该操作没有阻塞读写访问

## 测试用例

### 1. 并发创建索引

并发索引创建不应锁定表。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"create_index","msg_id":1,"table":"users","column":"email","concurrently":true}}
```

期望输出：

```text
{"type": "index_created", "in_reply_to": 1, "index": "idx_email", "duration_seconds": 120, "table_locked": false}
```

### 2. 添加列且不重写表

添加带服务端默认值的列不应导致表重写。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"add_column","msg_id":1,"table":"users","column":"status","default":"active","nullable":false}}
```

期望输出：

```text
{"type": "column_added", "in_reply_to": 1, "duration_seconds": 0.1, "table_rewritten": false}
```

## 参考资料

- [Zero-Downtime Migrations](https://www.citusdata.com/blog/2018/02/22/seven-tips-for-better-postgresql-migrations/)：生产环境中更安全地执行 PostgreSQL 迁移的七个技巧
- [pt-online-schema-change](https://www.percona.com/doc/percona-toolkit/LATEST/pt-online-schema-change.html)：Percona 在线模式变更工具文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
