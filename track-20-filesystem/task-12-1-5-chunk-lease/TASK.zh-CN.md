# 实现数据块租约机制以指定主副本

英文标题：Implement Chunk Leases for Primary Assignment
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-5-chunk-lease>

课程：20. 文件系统：分布式文件存储
任务序号：5
短标题：Chunk Lease
难度：高级
子主题：Distributed File Storage

## 中文导读

这道题要求你实现数据块的租约（Lease）机制。租约就像一个"限时授权"：主节点把某个数据块的写入权限授予一台块服务器，有效期 60 秒。这样就不需要每次写入都进行共识协商，同时又能保证同一时刻只有一个主副本在控制写入顺序。

## 题目说明

数据块租约（Lease）授予一台块服务器对某个数据块的独占写入排序权。这避免了每次操作都需要进行共识协商，同时保证了一致性。

租约的生命周期：
1. **授予（Grant）**：主节点将一个 60 秒的租约授予一台块服务器（即主副本）
2. **使用（Use）**：主副本为该数据块上的所有变更操作定义序列顺序
3. **续约（Renew）**：主副本通过心跳向主节点续约；主节点延长租约有效期
4. **过期（Expire）**：如果主副本在 60 秒内未能续约，租约过期
5. **重新授予（Re-grant）**：主节点等待旧租约过期后，将租约授予另一台服务器

安全保证：任何时刻，每个数据块最多只有一个主副本。如果主节点与主副本失去联系，它只需等待租约过期后再授予新的服务器，这样就不会出现"脑裂"问题。

```json
Request:  {"type": "lease_grant", "msg_id": 1, "chunk_handle": "ch_001", "server": "cs1"}
Response: {"type": "lease_grant_ok", "in_reply_to": 1, "chunk_handle": "ch_001", "primary": "cs1", "expires_in_ms": 60000}

Request:  {"type": "lease_renew", "msg_id": 2, "chunk_handle": "ch_001", "server": "cs1"}
Response: {"type": "lease_renew_ok", "in_reply_to": 2, "new_expires_in_ms": 60000}

Request:  {"type": "lease_check", "msg_id": 3, "chunk_handle": "ch_001"}
Response: {"type": "lease_check_ok", "in_reply_to": 3, "primary": "cs1", "remaining_ms": 45000, "expired": false}
```

## 涉及概念

- `lease`
- `primary election`
- `lease renewal`
- `lease expiry`
- `consistency window`

## 实现提示

- 租约将"主副本"角色授予一台块服务器，有效期 60 秒
- 主副本是唯一能为某个数据块上的变更操作定义顺序的服务器
- 主副本必须在租约过期前通过心跳向主节点续约
- 如果租约过期，主节点可以将其授予另一台服务器，从而避免脑裂
- 租约机制避免了每次操作都进行共识协商的开销，同时保证了一致性

## 测试用例

### 1. 向块服务器授予租约

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

### 2. 在过期前续约

lease_renew_ok 应当显示 new_expires_in_ms: 60000（租约已被延长）。

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

- [Leases in Distributed Systems](https://dl.acm.org/doi/10.1145/74851.74870)：关于租约机制的经典论文，讨论了租约作为分布式缓存容错机制的设计

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
