# 构建 Complete Sharded 键值 存储

英文标题：Build Complete Sharded Key-Value Store
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-5-sharded-kv>

课程：8. 分片器：水平扩展与数据迁移
任务序号：5
短标题：Sharded KV
难度：advanced
子主题：Range Sharding

## 中文导读

本题要求你完成 `构建 Complete Sharded 键值 存储`。

重点关注：`sharded storage`、`routing`、`end-to-end`。

建议先按提示逐步实现：Route requests to correct 分片。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a complete sharded KV store:

1. 客户端 determines 分片用于key
2. 客户端 routes to replica group owning 分片
3. If wrong group, get new config和重试
4.处理concurrent config changes
5. Ensure linearizability within each 分片

This combines all previous components into a working system.

## 概念说明

### Putting It Together

A sharded KV store has: (1) 分片 controller managing configuration, (2) multiple replica groups each handling some shards, (3) clients that route requests based on configuration.

### Client 重试

When a group receives a 请求用于a 分片 it doesn't own, it returns an error. The 客户端 refreshes configuration和retries. This may happen multiple times during reconfiguration.

## 涉及概念

- `sharded storage`
- `routing`
- `end-to-end`

## 实现提示

- Route requests to correct 分片
-处理"wrong group" errors
- 重试 on configuration changes

## 测试用例

### 1. Route to correct 分片

代理 routes 请求 to correct group based on 分片 assignment.

输入：

```json
{"src":"client","dest":"proxy","body":{"type":"init","msg_id":1,"node_id":"proxy","node_ids":["proxy"]}}
{"src":"controller","dest":"proxy","body":{"type":"config","msg_id":2,"version":1,"shards":{"0":"g1","1":"g1","2":"g1","3":"g1","4":"g2","5":"g2"}}}
{"src":"c1","dest":"proxy","body":{"type":"get","msg_id":3,"key":"mykey"}}
```

期望输出：

```text
{"src":"proxy","dest":"client","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"proxy","dest":"controller","body":{"type":"config_ok","in_reply_to":2,"msg_id":1}}
{"src":"proxy","dest":"c1","body":{"type":"get_ok","in_reply_to":3,"msg_id":2,"key":"mykey"}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
