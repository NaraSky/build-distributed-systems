#处理缓存 Invalidation和Consistency

英文标题：Handle Cache Invalidation和Consistency
网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-5-invalidation>

课程：11. 缓存
任务序号：5
短标题：Invalidation
难度：advanced

## 中文导读

本题要求你完成 `Handle 缓存 Invalidation和Consistency`。

重点关注：`invalidation`、`consistency`、`write-through`、`write-behind`。

建议先按提示逐步实现：Invalidate on every write。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement 缓存 invalidation strategies to maintain consistency between 缓存和database. When data changes, cached copies must be updated or removed.

Three main strategies:
1. Write-Through: Update 缓存和DB synchronously
2. Write-Behind: Update 缓存, async update DB
3. 缓存-Aside，包含Invalidation: Delete 缓存, update DB

Also handle 缓存 stampede: when many requests hit an expired key simultaneously.

## 概念说明

### 缓存 Invalidation

"There are only two hard things in Computer Science: 缓存 invalidation和naming things." - Phil Karlton. Keeping 缓存 consistent，包含the source of truth is notoriously difficult.

### Write-Through

Every write goes to both 缓存和database synchronously. Simple to reason about but adds latency to writes. 缓存 is always consistent but writes are slow.

### Write-Behind (Write-Back)

Writes go to 缓存 immediately, then asynchronously to database. Fast writes but risk of data loss if 缓存 fails before flush. Requires careful durability handling.

### 缓存 Stampede

When a popular key expires, many requests simultaneously miss和hit the database. Solutions include: locking (only one fetches), early expiration (refresh before actual expiry), or probabilistic early expiration.

## 涉及概念

- `invalidation`
- `consistency`
- `write-through`
- `write-behind`

## 实现提示

- Invalidate on every write
- Consider eventual vs strong consistency
-处理缓存 stampede scenarios

## 测试用例

### 1. Write-through consistency

Write-through pattern: Set key "x"，包含value 100. Verify write goes to BOTH 缓存和database synchronously. Get key "x" from 缓存 should return 100. Database should also contain x=100. 缓存和DB are always consistent.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [XFetch Paper](https://cseweb.ucsd.edu/~avattani/papers/cache_stampede.pdf)：Optimal probabilistic 缓存 stampede prevention
- [Redis Patterns](https://redis.io/topics/data-types-intro)：Caching patterns，包含Redis

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
