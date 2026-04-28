# 实现 etcd MVCC用于Versioned 键值 存储

英文标题：Implement etcd MVCC用于Versioned Key-Value Store
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-5-mvcc>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：15
短标题：etcd MVCC
难度：advanced
子主题：Consistency和the ZAB Protocol

## 中文导读

本题要求你完成 `实现 etcd MVCC用于Versioned 键值 存储`。

重点关注：`MVCC`、`multi-version concurrency`、`revision`、`compaction`、`historical reads`。

建议先按提示逐步实现：Every key has multiple versions, indexed by a global revision 计数器。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

etcd's MVCC (Multi-Version Concurrency Control) stores every version of every key. This enables historical reads和safe watch catch-up.

**How it works**:
1. Every modification increments a global revision 计数器
2. `Put("/config", "v1")` stores the value at revision 42
3. `Put("/config", "v2")` stores the value at revision 43
4. `Get("/config")` returns "v2" at revision 43 (latest)
5. `Get("/config", revision=42)` returns "v1" (historical read)

**Compaction**: old revisions are removed to save space. `Compact(revision=40)` deletes all versions before revision 40. Historical reads before revision 40 will fail.

**Watch safety**: a watcher at revision 42 can always catch up, even if it temporarily disconnects, by requesting changes since revision 42.

```JSON
请求:  {"type": "etcd_put", "msg_id": 1, "key": "/cfg", "value": "v1"}
响应: {"type": "etcd_put_ok", "in_reply_to": 1, "revision": 1}

请求:  {"type": "etcd_get", "msg_id": 2, "key": "/cfg", "revision": 1}
响应: {"type": "etcd_get_ok", "in_reply_to": 2, "key": "/cfg", "value": "v1", "mod_revision": 1}

请求:  {"type": "etcd_compact", "msg_id": 3, "revision": 5}
响应: {"type": "etcd_compact_ok", "in_reply_to": 3, "compacted_to": 5, "versions_removed": 12}
```

## 涉及概念

- `MVCC`
- `multi-version concurrency`
- `revision`
- `compaction`
- `historical reads`

## 实现提示

- Every key has multiple versions, indexed by a global revision 计数器
- Put increments the global revision和stores the key at that revision
- Get(key, revision=N) retrieves the value at revision N (historical read)
- Compact(revision=N) removes all versions before N to save space
- MVCC enables safe watches: even if a watch falls behind, it can catch up from a known revision

## 测试用例

### 1. Historical read returns old version

etcd_get_ok at revision 1 should return value "v1".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/k","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":3,"key":"/k","value":"v2"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_get","msg_id":4,"key":"/k","revision":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compact removes old versions

etcd_compact_ok should show compacted_to和versions_removed >= 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_compact","msg_id":2,"revision":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [etcd MVCC](https://etcd.io/docs/v3.5/learning/data_model/)：etcd documentation on MVCC data model和revision-based versioning

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
