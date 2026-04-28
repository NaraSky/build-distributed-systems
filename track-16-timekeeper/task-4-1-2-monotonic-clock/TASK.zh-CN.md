# 实现单调时钟包装器

英文标题：Implement Monotonic Clock Wrapper
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-2-monotonic-clock>

课程：16. 时间守卫：逻辑时钟
任务序号：2
短标题：单调时钟
难度：进阶
子主题：物理时间及其缺陷

## 中文导读

这道题要求你实现一个单调时钟（Monotonic Clock）包装器，保证每次返回的时间值永远不会变小。这就像一个"只能往前拨"的时钟——即使底层系统时钟因为 NTP 校正而回跳了，你的包装器也要确保返回的值不减。同时你需要思考：这种保护措施会丢失什么信息？

## 题目说明

单调时钟包装器对系统时钟进行封装，保证返回的时间值永远不会递减。你的任务是实现这个包装器，并记录它"修正"了多少次回跳。

```json
Request:  {"type": "mono_read", "msg_id": 1}
Response: {"type": "mono_read_ok", "in_reply_to": 1, "time_ms": 1234567, "corrections": 0}
```

## 涉及概念

- `monotonic clock`
- `clock wrapper`
- `information loss`
- `ordering guarantee`

## 实现提示

- 对系统时钟进行包装，始终返回大于或等于上一次返回值的时间
- 策略是取 `max(当前值, 上次返回值)` 作为本次返回值
- 记录包装器阻止了多少次回跳（即进行了多少次修正）
- 信息丢失之处在于：你无法知道时间是否真的发生了回跳
- Python 中的 `time.monotonic()` 原生提供了这种保证

## 测试用例

### 1. 读取单调时钟并返回时间

返回的 `mono_read_ok` 中应包含 `time_ms > 0` 且 `corrections=0`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 两次读取结果不递减

第二次读取的 `time_ms` 应大于或等于第一次。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Monotonic Clocks](https://docs.python.org/3/library/time.html#time.monotonic)：关于单调时钟保证的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
