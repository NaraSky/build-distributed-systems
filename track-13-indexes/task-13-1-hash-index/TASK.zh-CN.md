# 实现哈希索引

英文标题：Implement Hash Index
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-1-hash-index>

课程：13. 索引
任务序号：1
短标题：哈希索引
难度：进阶

## 中文导读

这道题要求你实现一个哈希索引（Hash Index），它将键映射到数据文件中的偏移量。索引是数据库系统的核心组件之一——没有索引，每次查询都要扫描全部数据。哈希索引能提供常数时间的精确查找，是理解存储引擎工作原理的入门基础。

## 题目说明

构建一个哈希索引，将键映射到数据文件的偏移量：

1. 对每个键进行哈希运算，确定它属于哪个桶（Bucket）
2. 在桶中存储键和对应的文件偏移量
3. 查找时根据键返回对应的偏移量
4. 使用链地址法或开放寻址法处理哈希冲突

哈希索引能够提供 O(1) 的精确查找，但不支持范围查询。

## 概念说明

### 为什么需要索引？

没有索引时，查找一条记录需要扫描所有数据，时间复杂度是 O(n)。索引提供了从键到存储位置的快捷路径，将查找时间降低到 O(1)（哈希索引）或 O(log n)（树索引）。这就好比一本书的目录——你可以直接翻到目标页码，而不必从头一页一页找。

### 哈希索引

哈希索引将键映射到文件偏移量。它在精确匹配查询上速度极快。Bitcask 这种日志结构存储引擎就使用了哈希索引。它的代价是：索引必须全部放在内存中，而且无法支持范围查询。

## 涉及概念

- `indexing`
- `hash table`
- `O(1) lookup`

## 实现提示

- 将键映射到数据存储位置
- 处理哈希冲突
- 支持插入、查找和删除操作

## 测试用例

### 1. 插入与查找

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"index_put","msg_id":2,"key":"foo","value":100}}
{"src":"c2","dest":"n1","body":{"type":"index_get","msg_id":3,"key":"foo"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"index_put_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"index_get_ok","in_reply_to":3,"msg_id":2,"value":100}}
```

## 参考资料

- [DDIA Chapter 3](https://dataintensive.net/)：《数据密集型应用系统设计》第三章，关于日志结构存储的存储与检索

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
