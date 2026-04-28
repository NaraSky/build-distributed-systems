# 构建全局缓存

网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-2-global-cache>

课程：11. 缓存
任务序号：2
短标题：全局缓存
难度：进阶

## 中文导读

这道题要求你实现一个所有节点共享的全局缓存服务，而不是让每个节点各自维护缓存。全局缓存能避免数据重复存储，也更容易做缓存失效管理，但代价是每次访问缓存都需要网络通信。这是理解集中式缓存架构的关键一步。

## 题目说明

实现一个所有节点都能访问的共享缓存。与上一题中每个节点各自维护缓存不同，这里由一个专门的缓存服务器来处理所有缓存操作。

优点：
1. 不会出现重复的缓存数据
2. 只需在一个地方做缓存失效处理
3. 内存利用率更高

缺点：
1. 每次访问缓存都需要一次网络通信
2. 缓存服务器可能成为性能瓶颈
3. 缓存服务器本身是单点故障

## 概念说明

### 全局缓存架构

全局缓存（Global Cache）将缓存数据集中存储在一台或多台专门的服务器上。所有应用节点都通过网络访问这些缓存服务器，而不是维护自己的本地缓存。这就是 Redis 和 Memcached 所采用的模型。

### 旁路缓存模式

在旁路缓存模式（Cache-Aside）中，应用程序先查缓存，如果没命中，就自己去查数据库，然后把结果写入缓存。缓存本身是被动的，它并不知道数据库的存在。

### 透读缓存模式

在透读缓存模式（Read-Through）中，缓存负责与数据库交互。当缓存未命中时，缓存自动从数据库获取数据。这种模式简化了应用代码，但让缓存和数据库产生了耦合。

## 涉及概念

- `shared cache`
- `cache coherence`
- `single point of truth`

## 实现提示

- 所有节点访问同一个缓存实例
- 使用网络协议进行缓存访问
- 安全地处理并发访问
- 注意：在使用非可重入锁的语言中，不要在持有锁的情况下调用回复或发送方法，否则可能导致死锁

## 测试用例

### 1. 全局缓存读写

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

- [Redis Documentation](https://redis.io/documentation)：关于使用 Redis 作为全局缓存的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
