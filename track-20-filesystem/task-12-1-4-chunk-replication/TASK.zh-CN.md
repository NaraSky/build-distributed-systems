# 实现基于流水线写入的数据块复制

英文标题：Implement Chunk Replication with Pipeline Writes
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-4-chunk-replication>

课程：20. 文件系统：分布式文件存储
任务序号：4
短标题：Chunk Replication
难度：高级
子主题：Distributed File Storage

## 中文导读

这道题要求你实现数据块的复制机制，使用流水线（Pipeline）方式将数据传播到所有副本。GFS 巧妙地将"数据流"和"控制流"分离：数据像水管一样在服务器间链式传递以最大化带宽，而写入顺序由主副本统一决定以保证一致性。

## 题目说明

当客户端写入数据时，主副本块服务器负责协调将数据复制到所有从副本。GFS 使用**流水线**设计，让数据以链式方式在服务器间传递，以最大化网络吞吐量。

写入复制的流程：
1. 客户端将数据发送给**最近的**块服务器（不一定是主副本）
2. 该服务器将数据转发给链中下一个最近的服务器
3. 数据以流水线方式流动：服务器 A -> 服务器 B -> 服务器 C
4. 当所有服务器都缓存了数据后，客户端向主副本发送**写入请求**
5. 主副本为这次写入分配一个序列号（用于排序）
6. 主副本在本地执行写入，然后将序列号转发给从副本
7. 从副本按相同顺序执行写入
8. 所有服务器确认完成后，主副本回复客户端

这种设计将**数据流**（流水线方式，最大化吞吐量）和**控制流**（主副本决定顺序）分开。

```json
Request:  {"type": "chunk_write", "msg_id": 1, "chunk_handle": "ch_001", "offset": 0, "data": "hello world", "primary": "cs1", "secondaries": ["cs2", "cs3"]}
Response: {"type": "chunk_write_ok", "in_reply_to": 1, "bytes_written": 11, "replicas_acked": 3, "serial_number": 1}
```

## 涉及概念

- `chunk replication`
- `pipeline writes`
- `primary-secondary`
- `write acknowledgement`
- `data flow`

## 实现提示

- 主副本接收写入请求后，通过流水线方式将数据转发给从副本
- 流水线的传输路径：客户端 -> 主副本 -> 从副本1 -> 从副本2（数据以链式方式流动）
- 三个副本都必须确认，写入才算成功
- 如果任何一个副本失败，写入即失败，客户端需要重试
- GFS 将数据流（流水线）和控制流（主副本提交顺序）分开处理

## 测试用例

### 1. 写入操作复制到所有服务器

chunk_write_ok 应当显示 replicas_acked: 3。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":2,"chunk_handle":"ch_001","offset":0,"data":"hello","primary":"n1","secondaries":["n2","n3"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 连续写入获得递增的序列号

第二次写入的 serial_number 应当大于第一次。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":2,"chunk_handle":"ch_001","offset":0,"data":"a","primary":"n1","secondaries":["n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":3,"chunk_handle":"ch_001","offset":1,"data":"b","primary":"n1","secondaries":["n2","n3"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [GFS Data Flow Pipeline](https://research.google/pubs/pub51/)：GFS 论文中关于流水线写入以及数据流和控制流分离的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
