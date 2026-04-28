# 实现数据块的创建与分配

英文标题：Implement Chunk Creation and Allocation
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-3-chunk-creation>

课程：20. 文件系统：分布式文件存储
任务序号：3
短标题：Chunk Creation
难度：高级
子主题：Distributed File Storage

## 中文导读

这道题要求你实现数据块的创建与分配逻辑。当客户端创建文件或追加数据时，主节点需要决定把新的数据块放在哪些服务器上。这个"放置策略"直接影响系统的容错能力和性能。

## 题目说明

当客户端创建文件或追加新的数据块时，主节点需要在合适的块服务器上分配存储空间。

数据块创建的流程：
1. 客户端向主节点发送 `allocate_chunk` 请求
2. 主节点根据放置策略选择 3 台块服务器：
   - 优先选择磁盘使用率低于平均值的服务器
   - 将副本分散到不同的机架上以提高容错能力（如果支持机架感知）
   - 优先为主副本选择网络距离较近的服务器
3. 主节点创建数据块的元数据，并分配一个唯一的数据块句柄
4. 主节点指定其中一台服务器作为**主副本（Primary）**（通过租约机制）
5. 将数据块句柄和服务器地址返回给客户端
6. 客户端直接向主副本写入数据

```json
Request:  {"type": "allocate_chunk", "msg_id": 1, "file": "/data/log.dat", "chunk_index": 0}
Response: {"type": "allocate_chunk_ok", "in_reply_to": 1, "chunk_handle": "ch_00042", "primary": "cs1", "secondaries": ["cs2", "cs3"], "lease_expires_ms": 60000}
```

## 涉及概念

- `chunk allocation`
- `placement policy`
- `rack awareness`
- `primary assignment`

## 实现提示

- 客户端向主节点请求新的数据块；主节点将其分配到 3 台服务器上并返回地址
- 放置策略：将副本分散到不同机架上以提高容错能力
- 主节点选择一台块服务器作为主副本并授予租约
- 客户端直接向主副本写入数据，主节点不参与数据传输
- 返回的地址按顺序排列：先是主副本，然后是从副本

## 测试用例

### 1. 分配数据块并返回主副本和从副本

allocate_chunk_ok 应当包含唯一的 chunk_handle、一个 primary 和 2 个 secondaries。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":2,"file":"/data/log.dat","chunk_index":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 多次分配产生唯一的数据块句柄

每次分配应当生成不同的 chunk_handle。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":2,"file":"/a.dat","chunk_index":0}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":3,"file":"/b.dat","chunk_index":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [GFS Chunk Allocation](https://research.google/pubs/pub51/)：GFS 论文中关于数据块创建、放置和副本管理的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
