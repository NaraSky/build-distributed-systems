# 实现 Query Side Optimization

英文标题：Implement Query Side Optimization
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-3-query-side>

课程：29. 反应器：事件溯源与 CQRS
任务序号：8
短标题：Query Side
难度：intermediate
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你完成 `实现 Query Side Optimization`。

重点关注：`read model`、`query optimization`、`caching`、`denormalization`、`pagination`。

建议先按提示逐步实现：Read models are denormalized: pre-join和pre-aggregate data用于fast reads。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The query side is the read path in CQRS. Instead of querying the write model directly (which is normalized用于writes), it reads from **pre-built read models** (projections) that are denormalized和indexed用于the specific query being served. Query results can also be cached to avoid redundant work.

Implement a 节点 that serves three query types:

```JSON
// Paginated user list from a denormalized listing projection
{ "type": "GetUserListing", "msg_id": 1,
  "params": {"page": 1, "limit": 10} }
-> { "type": "query_result", "in_reply_to": 1,
    "data": [{"id": "user-123", "name": "John Doe"}],
    "cached": false }

// Email lookup via 索引 (second call returns from 缓存)
{ "type": "GetUserByEmail", "msg_id": 2,
  "params": {"email": "john@example.com"} }
-> { "type": "query_result", "in_reply_to": 2,
    "data": {"email": "john@example.com", "userId": "user-123"},
    "cached": true }

// Filtered query: users in a specific city
{ "type": "GetUsersByCity", "msg_id": 3,
  "params": {"city": "NYC"} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": [{"city": "NYC", "userId": "user-123"}],
    "cached": false }
```

The `cached` field indicates whether the result was served from the query 缓存. A query handler never modifies any state.

## 涉及概念

- `read model`
- `query optimization`
- `caching`
- `denormalization`
- `pagination`

## 实现提示

- Read models are denormalized: pre-join和pre-aggregate data用于fast reads
- 缓存 query results，包含a TTL; return cached=true when the result comes from 缓存
- GetUserListing uses pagination (page, limit) to return a slice of the users list
- GetUserByEmail uses an email 索引用于O(1) lookup rather than a full scan
- The query side never writes — it reads from projections built by the event side

## 测试用例

### 1. Query user listing

Should return first page of user listing from read model.

输入：

```json
{"src":"client","dest":"queryside","body":{"type":"GetUserListing","msg_id":1,"params":{"page":1,"limit":10}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": [{"id": "user-123", "name": "John Doe"}], "cached": false}
```

### 2. Query，包含缓存 hit

Email 索引 lookup should return cached=true on repeated query.

输入：

```json
{"src":"client","dest":"queryside","body":{"type":"GetUserByEmail","msg_id":1,"params":{"email":"john@example.com"}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": {"email": "john@example.com", "userId": "user-123"}, "cached": true}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：Query side design和read model optimizations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
