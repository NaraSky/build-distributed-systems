# Understand和实现 HLC格式

英文标题：Understand和Implement HLC格式
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-1-hlc-format>

课程：2. 标识符：分布式唯一 ID
任务序号：16
短标题：HLC格式
难度：advanced
子主题：混合逻辑 Clocks (HLC)

## 中文导读

本题要求你完成 `Understand和实现 HLC格式`。

重点关注：`HLC`、`hybrid clock`、`physical time`、`logical counter`。

建议先按提示逐步实现：HLC is a tuple: (physical_time_ms, logical_counter)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Hybrid Logical Clocks (HLC), used in CockroachDB和Spanner, combine physical time，包含a logical 计数器. The format is `(physical_ms, logical_counter)`.

Rules用于updating HLC on a **local event or send**:
1. Get current physical time `pt`
2. If `pt > hlc.pt`: set `hlc.pt = pt`, `hlc.lc = 0`
3. Else: keep `hlc.pt`, increment `hlc.lc += 1`

Implement an HLC，包含`hlc_tick`和`hlc_get` handlers:

```JSON
请求:  {"type": "hlc_tick", "msg_id": 1}
响应: {"type": "hlc_tick_ok", "in_reply_to": 1, "pt": 1234567, "lc": 0}
```

```JSON
请求:  {"type": "hlc_get", "msg_id": 2}
响应: {"type": "hlc_get_ok", "in_reply_to": 2, "pt": 1234567, "lc": 0}
```

## 涉及概念

- `HLC`
- `hybrid clock`
- `physical time`
- `logical counter`

## 实现提示

- HLC is a tuple: (physical_time_ms, logical_counter)
- Physical time comes from the system 时钟
- Logical 计数器 disambiguates events within the same millisecond
- HLC always moves forward, even if 时钟 goes backward
- On send: if pt > max_pt, reset 计数器; else increment 计数器

## 测试用例

### 1. HLC tick returns pt和lc

hlc_tick_ok should contain pt > 0和lc = 0 (first tick gets fresh physical time).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. HLC get returns initial zero state

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_get","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_get_ok", "pt": 0, "lc": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Hybrid Logical Clocks (Kulkarni et al.)](https://cse.buffalo.edu/tech-reports/2014-04.pdf)：Original HLC paper by Kulkarni, Demirbas, et al.

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
