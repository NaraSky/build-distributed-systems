# Guarantee Read-Your-Writes，包含Follower Reads

英文标题：Guarantee Read-Your-Writes，包含Follower Reads
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-4-read-your-writes>

课程：7. 存储：线性一致 KV Store
任务序号：9
短标题：Read-Your-Writes
难度：advanced
子主题：Read Optimization

## 中文导读

本题要求你完成 `Guarantee Read-Your-Writes，包含Follower Reads`。

重点关注：`read-your-writes`、`session consistency`、`commit index tracking`、`client token`。

建议先按提示逐步实现：Clients send their last-seen commit_index，包含each read 请求。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Ensure read-your-writes consistency even when使用Follower reads. Clients send their `last_write_index`，包含each read. Followers only serve if they have applied that 索引.

```JSON
请求:  {"type": "write", "msg_id": 1, "key": "x", "value": "new"}
响应: {"type": "write_ok", "in_reply_to": 1, "commit_index": 10}

请求:  {"type": "ryw_read", "msg_id": 2, "key": "x", "last_write_index": 10, "prefer_follower": true}
响应: {"type": "ryw_read_ok", "in_reply_to": 2, "value": "new", "served_by": "n2", "follower_applied_index": 10, "waited_ms": 50}

请求:  {"type": "ryw_read", "msg_id": 3, "key": "x", "last_write_index": 15, "prefer_follower": true}
响应: {"type": "ryw_read_ok", "in_reply_to": 3, "value": "new", "served_by": "n1", "reason": "follower_behind_redirected_to_leader"}
```

## 涉及概念

- `read-your-writes`
- `session consistency`
- `commit index tracking`
- `client token`

## 实现提示

- Clients send their last-seen commit_index，包含each read 请求
- Followers only serve the read if they have applied at least that 索引
- If the Follower is behind, it either waits or redirects to the Leader
- This combines the scalability of Follower reads，包含read-your-writes guarantee
- The 客户端 tracks the commit_index from write responses

## 测试用例

### 1. Read-your-writes from follower

ryw_read_ok should show the read was served，包含follower_applied_index >= 5.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ryw_read","msg_id":2,"key":"x","last_write_index":5,"prefer_follower":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Follower behind redirects to Leader

Follower unlikely to have 索引 999. Should redirect to Leader.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ryw_read","msg_id":2,"key":"x","last_write_index":999,"prefer_follower":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Session Guarantees用于Weakly Consistent Data](https://www.cs.utexas.edu/~lorenzo/corsi/cs380d/papers/SessionGuarantees.pdf)：Formal definition of read-your-writes和other session guarantees

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
