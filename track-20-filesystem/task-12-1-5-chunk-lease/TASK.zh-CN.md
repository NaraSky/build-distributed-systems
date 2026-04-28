# 实现 Chunk Leases用于Primary Assignment

英文标题：Implement Chunk Leases用于Primary Assignment
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-5-chunk-lease>

课程：20. 文件系统：分布式文件存储
任务序号：5
短标题：Chunk Lease
难度：advanced
子主题：Distributed File Storage

## 中文导读

本题要求你完成 `实现 Chunk Leases用于Primary Assignment`。

重点关注：`lease`、`primary election`、`lease renewal`、`lease expiry`、`consistency window`。

建议先按提示逐步实现：A lease grants one chunk 服务端 the "primary" role用于60 seconds。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A chunk lease grants one chunk 服务端 the exclusive right to define the mutation order用于a chunk. This avoids per-operation 共识 while maintaining consistency.

Lease lifecycle:
1. **Grant**: master assigns a 60-second lease to one chunk 服务端 (the primary)
2. **Use**: the primary defines the serial order用于all mutations on that chunk
3. **Renew**: primary sends heartbeats to master; master extends the lease
4. **Expire**: if the primary fails to renew within 60s, the lease expires
5. **Re-grant**: master waits用于the old lease to expire, then grants to another 服务端

Safety guarantee: at most ONE primary exists用于each chunk at any time. If the master loses contact，包含the primary, it simply waits用于the lease to expire before granting to a new 服务端.

```JSON
请求:  {"type": "lease_grant", "msg_id": 1, "chunk_handle": "ch_001", "服务端": "cs1"}
响应: {"type": "lease_grant_ok", "in_reply_to": 1, "chunk_handle": "ch_001", "primary": "cs1", "expires_in_ms": 60000}

请求:  {"type": "lease_renew", "msg_id": 2, "chunk_handle": "ch_001", "服务端": "cs1"}
响应: {"type": "lease_renew_ok", "in_reply_to": 2, "new_expires_in_ms": 60000}

请求:  {"type": "lease_check", "msg_id": 3, "chunk_handle": "ch_001"}
响应: {"type": "lease_check_ok", "in_reply_to": 3, "primary": "cs1", "remaining_ms": 45000, "expired": false}
```

## 涉及概念

- `lease`
- `primary election`
- `lease renewal`
- `lease expiry`
- `consistency window`

## 实现提示

- A lease grants one chunk 服务端 the "primary" role用于60 seconds
- The primary is the only 服务端 that can define the mutation order用于a chunk
- The primary must renew the lease before it expires (by heartbeating the master)
- If the lease expires, the master can grant it to another 服务端 — preventing split-brain
- Leases avoid the cost of per-operation 共识 while maintaining consistency

## 测试用例

### 1. Grant lease to chunk server

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_grant","msg_id":2,"chunk_handle":"ch_001","server":"n2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lease_grant_ok", "in_reply_to": 2, "chunk_handle": "ch_001", "primary": "n2", "msg_id": 1}}
```

### 2. Renew lease before expiry

lease_renew_ok should show new_expires_in_ms: 60000 (lease extended).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_grant","msg_id":2,"chunk_handle":"ch_002","server":"n2"}}
{"src":"c1","dest":"n1","body":{"type":"lease_renew","msg_id":3,"chunk_handle":"ch_002","server":"n2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Leases in Distributed Systems](https://dl.acm.org/doi/10.1145/74851.74870)：Classic paper on leases as a 故障-tolerant mechanism用于distributed caches

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
