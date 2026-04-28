# 处理节点移除：优雅下线与崩溃恢复

英文标题：Handle Node Removal with Graceful and Crash Recovery
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-4-node-removal>

课程：8. 分片器：水平扩展与数据迁移
任务序号：9
短标题：节点移除
难度：高级
子主题：Consistent Hashing

## 中文导读

本题要求你处理节点从一致性哈希环中移除的两种场景：优雅下线和崩溃恢复。优雅下线时节点可以主动将数据转移给后继节点；崩溃场景下则需要通过副本来恢复数据。这是构建高可用分布式系统必须掌握的能力。

## 题目说明

当一个节点离开哈希环时（无论是优雅下线还是崩溃），它的键范围必须由后继节点接管。这两种场景需要不同的处理方式。

**优雅下线**：
1. 节点宣布即将离开
2. 节点将自己所有的键转移给顺时针方向的后继节点
3. 更新环的拓扑结构
4. 无数据丢失，最小化影响

**崩溃恢复**：
1. 其他节点检测到故障（心跳超时）
2. 后继节点接管崩溃节点的键范围
3. 从副本中恢复数据
4. 创建新的副本以恢复复制因子

```json
Request:  {"type": "ring_remove_node", "msg_id": 1, "node": "n2", "mode": "graceful"}
Response: {"type": "ring_remove_node_ok", "in_reply_to": 1, "keys_migrated": 333, "target_nodes": ["n1", "n3"], "mode": "graceful"}
```

## 涉及概念

- `node removal`
- `graceful shutdown`
- `crash recovery`
- `key takeover`
- `successor promotion`

## 实现提示

- 优雅下线时：节点在离开前将自己的键转移给顺时针后继节点
- 崩溃时：后继节点检测到故障并接管键范围
- 优雅下线更快（预先传输数据），崩溃恢复需要从副本恢复
- 使用虚拟节点时，被移除的虚拟节点上的键会分散到多个后继节点
- 副本机制保证即使在崩溃的情况下也不会丢失数据

## 测试用例

### 1. 优雅移除并迁移键

`ring_remove_node_ok` 应显示键已迁移到剩余节点。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_remove_node","msg_id":2,"node":"n2","mode":"graceful"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 崩溃恢复并接管键范围

崩溃模式应触发从副本进行数据恢复。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_remove_node","msg_id":2,"node":"n3","mode":"crash"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Consistent Hashing: Node Removal](https://www.akamai.com/us/en/multimedia/documents/technical-publication/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf)：Akamai 关于一致性哈希中节点加入和离开策略的论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
