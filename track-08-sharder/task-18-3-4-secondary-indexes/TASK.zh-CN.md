# 实现 Secondary Indexes on Sharded Data

英文标题：Implement Secondary Indexes on Sharded Data
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-4-secondary-indexes>

课程：8. 分片器：水平扩展与数据迁移
任务序号：14
短标题：Secondary Indexes
难度：advanced
子主题：Cross-分片 Queries

## 中文导读

本题要求你完成 `实现 Secondary Indexes on Sharded Data`。

重点关注：`secondary indexes`、`global indexes`、`local indexes`、`index sharding`、`write amplification`。

建议先按提示逐步实现：Primary 索引: data is partitioned by user_id。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When data is sharded by a primary key (e.g., `user_id`), querying by a secondary key (e.g., `email`) requires a secondary 索引. There are two main strategies.

**Local secondary 索引**:
- Each 分片 maintains an 索引用于its local data only
- Query by email must be sent to ALL shards (scatter-gather)
- Simple to implement but expensive用于queries

Example:
```JSON
请求:  {"type": "secondary_index_query", "msg_id": 1, "索引": "email", "value": "alice@example.com"}
响应: {"type": "secondary_index_query_ok", "in_reply_to": 1, "results": [{"user_id": "u42", "email": "alice@example.com"}], "shards_scanned": 3}
```

**Global secondary 索引**:
- A separate 索引 分片 that maps email → primary_key (user_id)
- Query by email first looks up the 索引 分片, then fetches from the data 分片
- Faster queries but more complex architecture

Example，包含global 索引:
```JSON
请求:  {"type": "secondary_index_query", "msg_id": 2, "索引": "email", "value": "bob@example.com", "use_global": true}
响应: {"type": "secondary_index_query_ok", "in_reply_to": 2, "results": [{"user_id": "u99", "email": "bob@example.com"}], "shards_scanned": 1}
```

**Write amplification**:
When a user updates their email:
1. Update primary record on 分片 hash(user_id)
2. Update secondary 索引 (either local or global)
3. Two 网络 round-trips instead of one

**Implementation**:
- Maintain an 索引 map: `Map<index_name, Map<index_value, primary_key>>`
- For local indexes: each 分片 has its own 索引 map
- For global indexes: a dedicated 索引 分片
- On write: update both the record和all secondary indexes

## 涉及概念

- `secondary indexes`
- `global indexes`
- `local indexes`
- `index sharding`
- `write amplification`
- `consistency`

## 实现提示

- Primary 索引: data is partitioned by user_id
- Secondary 索引 on email: need to lookup by email without knowing user_id
- Local secondary 索引: each 分片 maintains an 索引用于its local data only
- Global secondary 索引: a separate 索引 分片 that maps email → user_id
- Write amplification: updating a document requires updating both primary和secondary indexes

## 测试用例

### 1. Local secondary 索引 lookup

secondary_index_query_ok should return user record和shards_scanned=3 (scatter-gather).

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"secondary_index_query","msg_id":2,"index":"email","value":"alice@example.com"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Global secondary 索引 lookup

secondary_index_query_ok should return user record和shards_scanned=1 (direct lookup).

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"secondary_index_query","msg_id":2,"index":"email","value":"bob@example.com","use_global":true}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Secondary Indexes in Distributed Systems](https://www.mongodb.com/basics/create-index)：How secondary indexes work in sharded systems

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
