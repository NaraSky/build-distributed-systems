# 优化高吞吐量 ID 生成

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-5-high-throughput>

课程：2. 标识符：分布式唯一 ID
任务序号：5
短标题：高吞吐量
难度：进阶
子主题：为什么唯一 ID 这么难

## 中文导读

这道题要求你对 ID 生成器进行性能优化。在真实系统中（比如 Twitter），每秒需要生成数百万个 ID。你需要让你的实现在高并发场景下不成为瓶颈，目标是单节点每秒生成 10,000 个以上的 ID。

## 题目说明

优化你的 ID 生成器，使其达到最大吞吐量。像 Twitter 这样的真实系统每秒要生成数百万个 ID。你的实现需要在高并发场景下不成为系统瓶颈。

优化策略：

1. **减少锁竞争** -- 在多线程场景下尽量减少对同一把锁的争用
2. 尽可能使用**原子操作**
3. 考虑**预生成 ID** -- 批量提前生成以备使用
4. 对你的实现进行性能测试和测量

**目标**：单个节点每秒处理 10,000 次以上的 ID 生成请求。

## 概念说明

### 吞吐量优化

ID 生成通常处于**关键路径**上。每次数据库插入、每条消息、每个事件都需要一个 ID。即使是很小的效率损失，乘以数百万次操作后也会变得很严重。

### 瓶颈分析

```text
def generate_id():
    with lock:           # ← Contention point
        timestamp = now()
        sequence += 1
        return id
```

每个并发请求都必须获取同一把锁，这意味着所有 ID 生成操作被串行化了。就好比所有人都要排队通过同一扇门，门再大也会成为瓶颈。

### 优化技巧

  
    技巧
    优势
    复杂度
  
  
    为 msg_id 和 id_gen 使用不同的锁
    减少竞争
    低
  
  
    原子计数器
    无锁递增
    中
  
  
    预分配 ID 范围
    批量摊销开销
    高
  

### Go 语言的优势

Go 的 `sync/atomic` 包提供了无锁原语：

```text
import "sync/atomic"

var counter int64

func getNext() int64 {
    return atomic.AddInt64(&counter, 1)
}
```

在高竞争场景下，这比基于互斥锁的方案快得多。

## 涉及概念

- `performance`
- `throughput`
- `optimization`

## 实现提示

- 尽量减少锁竞争
- 考虑使用无锁方案
- 如果可以，批量生成 ID

## 测试用例

### 1. 生成单个 ID

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## 参考资料

- [Python Threading Best Practices](https://docs.python.org/3/library/threading.html)：Python 线程原语的官方文档
- [Go Atomic Operations](https://pkg.go.dev/sync/atomic)：Go 原子操作的官方文档，用于无锁编程

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
