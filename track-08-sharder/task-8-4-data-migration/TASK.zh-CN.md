# 实现 Data Migration

英文标题：Implement Data Migration
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-4-data-migration>

课程：8. 分片器：水平扩展与数据迁移
任务序号：4
短标题：Data Migration
难度：advanced
子主题：Range Sharding

## 中文导读

本题要求你完成 `实现 Data Migration`。

重点关注：`migration`、`data transfer`、`consistency`。

建议先按提示逐步实现：Stop serving 分片 during migration。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement data migration between replica groups:

1. Source group: stop accepting writes用于migrating 分片
2. Create snapshot of 分片 data + 客户端 sessions
3. Send to destination group
4. Destination: install snapshot, start serving 分片
5. Source: delete 分片 data after confirmation

Handle failures: 重试, idempotency, rollback.

## 概念说明

### Data Migration

Moving shards requires moving data. This must be atomic per 分片和consistent. During migration, the 分片 may be unavailable or served by source (stale reads OK) until transfer completes.

### Client Session Transfer

Don't forget 客户端 deduplication state. If sessions aren't migrated, clients may see duplicate execution on 重试. Transfer the 客户端 session table，包含the 分片 data.

## 涉及概念

- `migration`
- `data transfer`
- `consistency`

## 实现提示

- Stop serving 分片 during migration
- Transfer all key-value pairs
- Include 客户端 session state

## 测试用例

### 1. Prepare 分片用于migration

分片 3 locked, snapshot created containing data {x:1,y:2}.

输入：

```json
{"src":"c0","dest":"g1","body":{"type":"init","msg_id":1,"node_id":"g1","node_ids":["g1","g2"]}}
{"src":"c0","dest":"g1","body":{"type":"seed_shard","msg_id":2,"shard":3,"data":{"x":1,"y":2}}}
{"src":"c0","dest":"g1","body":{"type":"prepare_migration","msg_id":3,"shard":3,"target_gid":"g2"}}
```

期望输出：

```text
{"src":"g1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"g1","dest":"c0","body":{"type":"seed_shard_ok","in_reply_to":2,"msg_id":1}}
{"src":"g1","dest":"c0","body":{"type":"prepare_migration_ok","in_reply_to":3,"msg_id":2,"shard":3,"target_gid":"g2","snapshot":{"data":{"x":1,"y":2}}}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
