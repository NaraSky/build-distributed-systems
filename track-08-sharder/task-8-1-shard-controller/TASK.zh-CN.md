# 实现 分片 Controller

英文标题：Implement Shard Controller
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-1-shard-controller>

课程：8. 分片器：水平扩展与数据迁移
任务序号：1
短标题：分片 Controller
难度：advanced
子主题：Range Sharding

## 中文导读

本题要求你完成 `实现 分片 Controller`。

重点关注：`sharding`、`configuration`、`coordination`。

建议先按提示逐步实现：Controller manages 分片-to-group mapping。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a 分片 controller that manages 分片 assignment:

1. Maintain configuration: which replica group owns which shards
2. Support operations: Join (add group), Leave (remove group), Move (reassign 分片)
3. Replicate controller state，包含Raft用于故障 tolerance
4. Distribute shards evenly across groups
5. Provide configuration query API

The controller is the source of truth用于分片 ownership.

## 概念说明

### Sharding

When data exceeds one machine's capacity, split it across multiple machines (shards). Each 分片 handles a subset of keys. Sharding provides horizontal scalability.

### 分片 Controller

The controller decides which 分片 goes where. It is typically a small Raft group用于high availability. Configuration changes are versioned to coordinate migrations.

## 涉及概念

- `sharding`
- `configuration`
- `coordination`

## 实现提示

- Controller manages 分片-to-group mapping
- Use Raft用于controller 复制
- Support join, leave, move operations

## 测试用例

### 1. Join new group

Config version incremented, group g1 added，包含servers [s1, s2], all 10 shards assigned to g1.

输入：

```json
{"src":"c0","dest":"controller","body":{"type":"init","msg_id":1,"node_id":"controller","node_ids":["controller"]}}
{"src":"c1","dest":"controller","body":{"type":"join","msg_id":2,"gid":"g1","servers":["s1","s2"]}}
{"src":"c1","dest":"controller","body":{"type":"query","msg_id":3,"num":-1}}
```

期望输出：

```text
{"src":"controller","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"controller","dest":"c1","body":{"type":"join_ok","in_reply_to":2,"msg_id":1}}
{"src":"controller","dest":"c1","body":{"type":"query_ok","in_reply_to":3,"msg_id":2,"version":1,"groups":{"g1":["s1","s2"]},"shards":{"0":"g1","1":"g1","2":"g1","3":"g1","4":"g1","5":"g1","6":"g1","7":"g1","8":"g1","9":"g1"}}}
```

## 参考资料

- [MIT 6.824 Lab 4](https://pdos.csail.mit.edu/6.824/labs/lab-shard.html)：Sharded KV store lab

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
