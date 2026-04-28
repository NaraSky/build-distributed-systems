# 实现 HLC Receive Rule

英文标题：Implement HLC Receive Rule
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-2-hlc-receive>

课程：2. 标识符：分布式唯一 ID
任务序号：17
短标题：HLC Receive
难度：advanced
子主题：混合逻辑 Clocks (HLC)

## 中文导读

本题要求你完成 `实现 HLC Receive Rule`。

重点关注：`HLC merge`、`receive rule`、`clock synchronization`、`causal consistency`。

建议先按提示逐步实现：On receive: take max of local pt, received pt,和current physical time。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The HLC receive rule is more complex than Lamport's. On receiving a 消息，包含HLC `(msg.pt, msg.lc)`:

1. `new_pt = max(local.pt, msg.pt, now_ms())`
2. If `new_pt == local.pt == msg.pt`: `new_lc = max(local.lc, msg.lc) + 1`
3. Elif `new_pt == local.pt`: `new_lc = local.lc + 1`
4. Elif `new_pt == msg.pt`: `new_lc = msg.lc + 1`
5. Else (new physical time): `new_lc = 0`

Implement a `hlc_receive` handler:
```JSON
请求:  {"type": "hlc_receive", "msg_id": 1, "remote_pt": 1000, "remote_lc": 5}
响应: {"type": "hlc_receive_ok", "in_reply_to": 1, "pt": 1000, "lc": 6}
```

## 涉及概念

- `HLC merge`
- `receive rule`
- `clock synchronization`
- `causal consistency`

## 实现提示

- On receive: take max of local pt, received pt,和current physical time
- If the max pt equals local pt和received pt, increment lc from max of both lc values
- If max pt equals only one side, take that sides lc和increment
- If max pt is the new physical time, reset lc to 0
- HLC must always advance - never go backward

## 测试用例

### 1. Receive from ahead remote advances local

Remote pt is far future. new_pt=remote_pt, new_lc=remote_lc+1=6.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"n2","dest":"n1","body":{"type":"hlc_receive","msg_id":2,"remote_pt":9999999999999,"remote_lc":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "hlc_receive_ok", "pt": 9999999999999, "lc": 6, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Receive from behind remote uses local

After tick, local pt is current time. Remote pt=0 is behind. new_pt=max(local,0,now). lc depends on whether now advanced.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"hlc_receive","msg_id":3,"remote_pt":0,"remote_lc":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CockroachDB和HLC](https://www.cockroachlabs.com/blog/living-without-atomic-clocks/)：How CockroachDB uses HLC用于事务 ordering

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
