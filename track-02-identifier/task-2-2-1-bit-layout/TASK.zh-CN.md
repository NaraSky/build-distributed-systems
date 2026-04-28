# 实现雪花 ID 的位布局

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-1-bit-layout>

课程：2. 标识符：分布式唯一 ID
任务序号：6
短标题：位布局
难度：进阶
子主题：雪花 ID（Twitter 的方案）

## 中文导读

这道题让你动手实现 Twitter 雪花 ID 的核心——64 位整数的位布局。你需要把时间戳、机器 ID 和序列号这三个部分，通过位运算组装成一个整数，也要能把一个整数拆回这三个部分。这是理解雪花 ID 工作原理的关键。

## 题目说明

Twitter 的雪花算法（Snowflake）能够在不需要节点间协调的情况下，生成唯一的、大致有序的 64 位 ID。它的位布局如下：

```
| 1 bit unused | 41 bits timestamp | 10 bits machine ID | 12 bits sequence |
|     0        |   ms since epoch  |    0-1023          |    0-4095        |
```

你需要实现以下功能：

1. **组装**：将三个组成部分（timestamp_ms、machine_id、sequence）组合成一个雪花 ID
2. **拆解**：将一个雪花 ID 还原成它的三个组成部分
3. 处理 Maelstrom 的 `generate` 工作负载，使用雪花 ID 作为生成结果

实现 `generate` 消息处理器：
```json
Request:  {"type": "generate", "msg_id": 1}
Response: {"type": "generate_ok", "in_reply_to": 1, "id": 7041429939834880}
```

以及用于调试的 `decompose` 处理器：
```json
Request:  {"type": "decompose", "msg_id": 2, "id": 7041429939834880}
Response: {"type": "decompose_ok", "in_reply_to": 2, "timestamp_ms": 1678886400000, "machine_id": 1, "sequence": 0}
```

## 涉及概念

- `bit manipulation`
- `Snowflake ID`
- `bit layout`
- `scalability`

## 实现提示

- 使用左移运算（`<<`）将每个部分放置到 64 位整数中的正确位置
- 时间戳占高 41 位，机器 ID 占接下来的 10 位，序列号占最低的 12 位
- 使用按位或运算（`|`）将各部分合并
- 提取各部分时，使用右移运算（`>>`）和按位与运算（`&`）配合掩码
- 每个节点每毫秒最多生成 2^12 = 4096 个 ID

## 测试用例

### 1. 初始化并生成 ID

验证说明：第二行应该是一个 `generate_ok` 响应，包含一个数值类型的 `id` 字段。由于时间戳不同，具体数值会有所变化。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 两次连续生成应产生不同的 ID

验证说明：两个 `generate_ok` 响应应包含不同的 `id` 值，且第二个 ID 应大于等于第一个。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Twitter Snowflake (Original Announcement)](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake)：Twitter 工程博客上介绍雪花 ID 生成方案的原始文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
