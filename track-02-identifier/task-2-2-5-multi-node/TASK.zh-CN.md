# 多节点雪花 ID 唯一性验证

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-5-multi-node>

课程：2. 标识符：分布式唯一 ID
任务序号：10
短标题：多节点 ID
难度：高级
子主题：雪花 ID（Twitter 的方案）

## 中文导读

雪花 ID 的唯一性依赖于机器 ID 这个组成部分。10 位机器 ID 最多可以支持 1024 台机器同时生成 ID，且无需任何协调。这道题让你验证多个节点生成的 ID 确实是全局唯一的，并实现一个 ID 校验接口来检测重复和排序情况。

## 题目说明

雪花 ID 的唯一性来源于其中的机器 ID 部分。10 位机器 ID 意味着最多可以有 1024 台机器在不需要任何协调的情况下同时生成 ID。

你需要完成以下任务来验证多节点间的唯一性和排序：

1. 从 Maelstrom 的 `node_id` 中提取机器 ID（例如 "n3" 对应机器 ID 为 3）
2. 生成 ID 并验证在单个节点内的唯一性
3. 实现 `verify_ids` 处理器，检查一组 ID 的唯一性和排序情况

```json
Request:  {"type": "verify_ids", "msg_id": 1, "ids": [100, 200, 300, 200]}
Response: {"type": "verify_ids_ok", "in_reply_to": 1, "count": 4, "unique": 3, "is_sorted": false, "duplicates": [200]}
```

## 涉及概念

- `multi-node coordination`
- `uniqueness verification`
- `monotonicity`
- `ID distribution`

## 实现提示

- 每个节点使用从 `node_id` 中提取的专属机器 ID
- 不同节点生成的 ID 天然唯一，因为机器 ID 对应的位不同
- 在单个节点内，ID 必须单调递增
- 跨节点时，ID 只是大致有序的，因为各节点的时钟可能存在偏差
- 使用拆解函数来验证机器 ID 的提取是否正确

## 测试用例

### 1. 验证有序且唯一的 ID 列表

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"verify_ids","msg_id":2,"ids":[10,20,30]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "verify_ids_ok", "count": 3, "unique": 3, "is_sorted": true, "duplicates": [], "in_reply_to": 2, "msg_id": 1}}
```

### 2. 检测 ID 列表中的重复项

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"verify_ids","msg_id":2,"ids":[10,20,10,30]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "verify_ids_ok", "count": 4, "unique": 3, "is_sorted": false, "duplicates": [10], "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Unique ID Generation at Scale](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake)：Twitter 雪花算法的官方发布博文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
