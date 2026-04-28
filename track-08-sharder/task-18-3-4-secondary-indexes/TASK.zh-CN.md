# 在分片数据上实现二级索引

英文标题：Implement Secondary Indexes on Sharded Data
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-4-secondary-indexes>

课程：8. 分片器：水平扩展与数据迁移
任务序号：14
短标题：二级索引
难度：高级
子主题：跨分片查询

## 中文导读

本题要求你在分片数据上实现二级索引（Secondary Index）。当数据按主键分片后，如果想通过其他字段查询（比如按邮箱查用户），就需要二级索引。二级索引有"本地"和"全局"两种方案，各有优劣：本地索引实现简单但查询需要扫描所有分片，全局索引查询快但架构更复杂、写入开销更大。

## 题目说明

当数据按主键（例如 `user_id`）分片后，如果要按二级键（例如 `email`）查询，就需要二级索引。主要有两种策略。

**本地二级索引**：
- 每个分片仅为自己的本地数据维护索引
- 按邮箱查询时必须发送给所有分片（分散-聚集）
- 实现简单，但查询开销大

示例：
```json
Request:  {"type": "secondary_index_query", "msg_id": 1, "index": "email", "value": "alice@example.com"}
Response: {"type": "secondary_index_query_ok", "in_reply_to": 1, "results": [{"user_id": "u42", "email": "alice@example.com"}], "shards_scanned": 3}
```

**全局二级索引**：
- 由一个独立的索引分片维护邮箱到主键（user_id）的映射
- 按邮箱查询时，先查索引分片获取主键，再从数据分片获取完整记录
- 查询更快，但架构更复杂

使用全局索引的示例：
```json
Request:  {"type": "secondary_index_query", "msg_id": 2, "index": "email", "value": "bob@example.com", "use_global": true}
Response: {"type": "secondary_index_query_ok", "in_reply_to": 2, "results": [{"user_id": "u99", "email": "bob@example.com"}], "shards_scanned": 1}
```

**写放大**：
当用户更新邮箱时：
1. 在 `hash(user_id)` 对应的分片上更新主记录
2. 更新二级索引（无论是本地还是全局）
3. 需要两次网络往返，而不是一次

**实现方式**：
- 维护一个索引映射：`Map<index_name, Map<index_value, primary_key>>`
- 本地索引：每个分片有自己的索引映射
- 全局索引：由一个专用的索引分片维护
- 写入时：同时更新记录和所有二级索引

## 涉及概念

- `secondary indexes`
- `global indexes`
- `local indexes`
- `index sharding`
- `write amplification`
- `consistency`

## 实现提示

- 主索引：数据按 user_id 分片
- 邮箱的二级索引：在不知道 user_id 的情况下按邮箱查找
- 本地二级索引：每个分片仅为本地数据维护索引
- 全局二级索引：由独立的索引分片维护邮箱到 user_id 的映射
- 写放大：更新一条记录需要同时更新主索引和二级索引

## 测试用例

### 1. 本地二级索引查找

`secondary_index_query_ok` 应返回用户记录，且 `shards_scanned=3`（分散-聚集查询）。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"secondary_index_query","msg_id":2,"index":"email","value":"alice@example.com"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 全局二级索引查找

`secondary_index_query_ok` 应返回用户记录，且 `shards_scanned=1`（直接查找）。

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

- [Secondary Indexes in Distributed Systems](https://www.mongodb.com/basics/create-index)：分片系统中二级索引的工作原理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
