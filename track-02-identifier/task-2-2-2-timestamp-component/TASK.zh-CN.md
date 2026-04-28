# 实现自定义纪元的时间戳组件

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-2-timestamp-component>

课程：2. 标识符：分布式唯一 ID
任务序号：7
短标题：自定义纪元
难度：进阶
子主题：雪花 ID（Twitter 的方案）

## 中文导读

这道题聚焦于雪花 ID 中的时间戳部分。41 位时间戳从什么时间开始计算，直接影响 ID 系统能用多少年。如果从 Unix 纪元（1970 年）开始，就白白浪费了 50 多年。这道题让你实现一个从 2024 年开始的自定义纪元，从而最大化利用有限的位数。

## 题目说明

雪花 ID 中的时间戳部分使用 41 位来表示自**自定义纪元（Custom Epoch）**以来的毫秒数。如果使用 Unix 纪元（1970-01-01），会浪费超过 50 年的时间戳空间。如果把起点设为 2024 年，系统就能获得大约 69 年的可用时间。

你需要完成以下任务：

1. 实现基于自定义纪元（2024-01-01 00:00:00 UTC）的时间戳生成
2. 验证时间戳能放进 41 位以内
3. 实现 `time_info` 消息处理器，返回当前的时间戳状态信息

```json
Request:  {"type": "time_info", "msg_id": 1}
Response: {"type": "time_info_ok", "in_reply_to": 1, 
           "current_ms": 1234567, 
           "custom_epoch_ms": 1704067200000,
           "max_timestamp_ms": 2199023255551,
           "years_remaining": 69}
```

同时实现使用自定义纪元时间戳的 `generate` 处理器，并验证生成的 ID 是单调递增的：
```json
Request:  {"type": "generate", "msg_id": 1}
Response: {"type": "generate_ok", "in_reply_to": 1, "id": 1234567890}
```

## 涉及概念

- `timestamp`
- `epoch`
- `time representation`
- `overflow planning`

## 实现提示

- 自定义纪元从 2024 年开始，41 位大约可用 69 年才会溢出
- 如果用 Unix 纪元（1970 年），就浪费了 54 年的时间戳空间
- 使用 `time.time() * 1000` 获取当前的毫秒级时间戳
- 用当前时间戳减去自定义纪元，得到相对毫秒数
- 在组装 ID 之前，检查时间戳是否能放进 41 位

## 测试用例

### 1. 生成一个数值型 ID

验证说明：`generate_ok` 响应应包含一个大于 0 的数值型 `id` 字段。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 获取时间信息，包含纪元和剩余年数

验证说明：响应应包含 `custom_epoch_ms=1704067200000`、`max_timestamp_ms=2199023255551`、`current_ms > 0` 以及 `years_remaining > 0`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"time_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)：Lamport 关于分布式系统中逻辑时钟和事件排序的经典论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
