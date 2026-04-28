# 实现查询端优化

英文标题：Implement Query Side Optimization
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-3-query-side>

课程：29. 反应器：事件溯源与 CQRS
任务序号：8
短标题：查询端
难度：进阶
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你实现 CQRS 中查询端的优化逻辑。查询端是系统的"读取路径"，它不直接查询写入模型，而是从预先构建好的读取模型（投影）中获取数据。这些读取模型经过反范式化处理和索引优化，查询速度非常快。再结合缓存机制，可以进一步减少重复计算。

## 题目说明

查询端是 CQRS 中的读取路径。它不直接查询写入模型（写入模型是为写入优化的范式化结构），而是从**预先构建的读取模型**（投影）中读取数据。这些读取模型是反范式化的，并且为特定查询场景建立了索引。查询结果还可以被缓存，以避免重复计算。

你需要实现一个支持三种查询类型的节点：

```json
// 从反范式化的列表投影中分页查询用户
{ "type": "GetUserListing", "msg_id": 1,
  "params": {"page": 1, "limit": 10} }
-> { "type": "query_result", "in_reply_to": 1,
    "data": [{"id": "user-123", "name": "John Doe"}],
    "cached": false }

// 通过索引按邮箱查找（第二次调用从缓存返回）
{ "type": "GetUserByEmail", "msg_id": 2,
  "params": {"email": "john@example.com"} }
-> { "type": "query_result", "in_reply_to": 2,
    "data": {"email": "john@example.com", "userId": "user-123"},
    "cached": true }

// 过滤查询：查找特定城市的用户
{ "type": "GetUsersByCity", "msg_id": 3,
  "params": {"city": "NYC"} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": [{"city": "NYC", "userId": "user-123"}],
    "cached": false }
```

`cached` 字段标识结果是否来自查询缓存。查询处理器绝不修改任何状态。

## 涉及概念

- `read model`
- `query optimization`
- `caching`
- `denormalization`
- `pagination`

## 实现提示

- 读取模型是反范式化的：提前做好关联查询和数据聚合，以加快读取速度
- 为查询结果添加带过期时间的缓存；当结果来自缓存时返回 cached=true
- GetUserListing 使用分页参数（page 和 limit）返回用户列表的一个切片
- GetUserByEmail 使用邮箱索引实现常数时间查找，而不是全表扫描
- 查询端绝不执行写操作，它只从事件端构建的投影中读取数据

## 测试用例

### 1. 查询用户列表

应从读取模型中返回用户列表的第一页。

输入：

```json
{"src":"client","dest":"queryside","body":{"type":"GetUserListing","msg_id":1,"params":{"page":1,"limit":10}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": [{"id": "user-123", "name": "John Doe"}], "cached": false}
```

### 2. 查询命中缓存

重复的邮箱索引查找应返回 cached=true。

输入：

```json
{"src":"client","dest":"queryside","body":{"type":"GetUserByEmail","msg_id":1,"params":{"email":"john@example.com"}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": {"email": "john@example.com", "userId": "user-123"}, "cached": true}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：查询端设计与读取模型优化

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
