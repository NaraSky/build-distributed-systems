# 构建 Global 缓存

英文标题：Build Global Cache
网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-2-global-cache>

课程：11. 缓存
任务序号：2
短标题：Global 缓存
难度：intermediate

## 中文导读

本题要求你完成 `构建 Global 缓存`。

重点关注：`shared cache`、`cache coherence`、`single point of truth`。

建议先按提示逐步实现：All 节点 access a single 缓存 instance。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a shared 缓存 accessible by all 节点. Instead of each 节点 maintaining its own 缓存, a dedicated 缓存 服务端 handles all 缓存 operations.

Benefits:
1. No duplicate cached data
2. Single point用于invalidation
3. Better memory utilization

Trade-offs:
1. 网络 hop用于every 缓存 access
2. 缓存 服务端 becomes a bottleneck
3. Single point of 故障

## 概念说明

### Global 缓存 Architecture

A global 缓存 centralizes cached data in one or more dedicated servers. All application 节点 contact the 缓存 服务端 instead of maintaining local caches. This is the model used by Redis和Memcached.

### Look-Aside 缓存 Pattern

In look-aside (缓存-aside), the application checks the 缓存,和on miss, queries the database和populates the 缓存. The 缓存 is passive - it does not know about the database.

### Look-Through 缓存 Pattern

In look-through, the 缓存 handles database interaction. On miss, the 缓存 fetches from the database automatically. This simplifies application code but couples 缓存 to database.

## 涉及概念

- `shared cache`
- `cache coherence`
- `single point of truth`

## 实现提示

- All 节点 access a single 缓存 instance
- Use 网络 protocol用于缓存 access
-处理concurrent access safely
- Go/Python tip: avoid holding the lock while calling reply/send - this causes deadlocks，包含non-reentrant locks

## 测试用例

### 1. Global 缓存 get/set

输入：

```json
{"src":"c0","dest":"cache","body":{"type":"init","msg_id":1,"node_id":"cache","node_ids":["cache","n1","n2"]}}
{"src":"n1","dest":"cache","body":{"type":"get","msg_id":2,"key":"x"}}
{"src":"n2","dest":"cache","body":{"type":"set","msg_id":3,"key":"x","value":100}}
{"src":"n1","dest":"cache","body":{"type":"get","msg_id":4,"key":"x"}}
```

期望输出：

```text
{"src":"cache","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"cache","dest":"n1","body":{"type":"get_ok","in_reply_to":2,"msg_id":1,"value":null}}
{"src":"cache","dest":"n2","body":{"type":"set_ok","in_reply_to":3,"msg_id":2}}
{"src":"cache","dest":"n1","body":{"type":"get_ok","in_reply_to":4,"msg_id":3,"value":100}}
```

## 参考资料

- [Redis Documentation](https://redis.io/documentation)：Redis as a global 缓存

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
