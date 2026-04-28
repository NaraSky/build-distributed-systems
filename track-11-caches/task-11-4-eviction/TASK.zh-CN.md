# 添加 Eviction Strategies (LRU, TTL)

英文标题：Add Eviction Strategies (LRU, TTL)
网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-4-eviction>

课程：11. 缓存
任务序号：4
短标题：Eviction
难度：intermediate

## 中文导读

本题要求你完成 `添加 Eviction Strategies (LRU, TTL)`。

重点关注：`LRU`、`TTL`、`eviction`、`cache capacity`。

建议先按提示逐步实现：Track access time用于LRU。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement 缓存 eviction policies to manage limited memory. When the 缓存 is full和a new entry must be added, an eviction policy decides what to remove.

Implement two eviction strategies:
1. TTL (Time-To-Live): Remove entries after they expire
2. LRU (Least Recently Used): Remove entries not accessed recently

Combine them: honor TTL,和when at capacity, evict LRU entries.

## 概念说明

### Why Eviction?

Memory is finite. Without eviction, caches would grow unbounded. Eviction policies determine which entries to remove when space is needed.

### LRU (Least Recently Used)

LRU evicts the entry that has not been accessed用于the longest time. The assumption is that recently accessed data will be accessed again (temporal locality). LRU is the most common eviction policy.

### LFU (Least Frequently Used)

LFU tracks access counts和evicts entries，包含the lowest frequency. This works well用于stable access patterns but can keep old cold entries that were once popular.

## 涉及概念

- `LRU`
- `TTL`
- `eviction`
- `cache capacity`

## 实现提示

- Track access time用于LRU
- Use ordered dict or doubly-linked list
- Evict when capacity is reached

## 测试用例

### 1. LRU eviction

LRU 缓存，包含max_size=3. Sequence: set(a,1), set(b,2), set(c,3) [缓存 full], get(a), get(c) [a和c accessed recently], set(d,4) [should evict b as least recently used]. Verify b is evicted, a和c remain in 缓存, d is added.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [LRU Cache Implementation](https://leetcode.com/problems/lru-cache/)：LeetCode LRU 缓存 problem

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
