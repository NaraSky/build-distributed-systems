# 添加 WAL Segment Files，包含Offset 索引

英文标题：Add WAL Segment Files，包含Offset Index
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-3-segments>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：3
短标题：WAL Segments
难度：advanced
子主题：The Commit 日志 (WAL)

## 中文导读

本题要求你完成 `添加 WAL Segment Files，包含Offset 索引`。

重点关注：`segment files`、`log segmentation`、`offset index`、`fast seeks`、`immutable segments`。

建议先按提示逐步实现：When the active segment exceeds a size threshold (e.g. 64MB), seal it和open a new one。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A single WAL file has a problem: it grows without bound. Once it reaches gigabytes, seeks become slow和cleanup is impossible without rewriting the entire file.

The solution: **segment files**. When a WAL segment exceeds a size threshold, seal it (make it immutable)和open a new active segment. An offset 索引 enables O(1) lookups by mapping each 日志 offset to the correct segment file和byte position.

This is how Kafka, etcd,和most production systems organize their logs:
1. Segments are named by their starting offset (e.g. `00000000.日志`, `00001000.日志`)
2. Each segment has a companion `.索引` file mapping offset -> byte position
3. Old sealed segments can be deleted, compressed, or archived independently
4. The active segment is the only one receiving new writes

```JSON
请求:  {"type": "wal_segment_config", "msg_id": 1, "max_segment_bytes": 67108864}
响应: {"type": "wal_segment_config_ok", "in_reply_to": 1, "max_segment_bytes": 67108864}

请求:  {"type": "wal_segment_info", "msg_id": 2}
响应: {"type": "wal_segment_info_ok", "in_reply_to": 2, "segments": [
    {"file": "00000000.日志", "start_offset": 0, "end_offset": 999, "size_bytes": 67108000, "sealed": true},
    {"file": "00001000.日志", "start_offset": 1000, "end_offset": 1050, "size_bytes": 5120, "sealed": false}
], "active_segment": "00001000.日志"}
```

## 涉及概念

- `segment files`
- `log segmentation`
- `offset index`
- `fast seeks`
- `immutable segments`

## 实现提示

- When the active segment exceeds a size threshold (e.g. 64MB), seal it和open a new one
- Maintain an 索引 mapping (log_offset -> segment_file + byte_offset)用于O(1) seeks
- Sealed segments are immutable — they can be safely compressed, archived, or deleted
- Name segments by their starting offset: 00000000.日志, 00001000.日志, etc.
- This is exactly how Kafka organizes its partition logs on disk

## 测试用例

### 1. Configure segment size threshold

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_segment_config","msg_id":2,"max_segment_bytes":1024}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_segment_config_ok", "in_reply_to": 2, "max_segment_bytes": 1024, "msg_id": 1}}
```

### 2. Segment info shows active segment on empty 日志

wal_segment_info_ok should show at least 1 segment，包含sealed: false (active).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_segment_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Kafka Log Segments](https://kafka.apache.org/documentation/#design_filesystem)：How Kafka organizes partition logs into segment files用于efficient 存储和cleanup

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
