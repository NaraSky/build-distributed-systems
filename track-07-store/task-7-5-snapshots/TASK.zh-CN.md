# 实现基于快照的日志压缩

英文标题：Implement Log Compaction with Snapshots
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-5-snapshots>

课程：7. 存储：线性一致键值存储
任务序号：5
短标题：Snapshots
难度：高级
子主题：线性一致键值存储

## 中文导读

这道题要求你实现基于快照（Snapshot）的日志压缩机制。随着系统运行，Raft 日志会不断增长。如果不做清理，日志最终会占满所有存储空间。快照机制把已经应用到状态机的日志条目压缩为一个紧凑的状态快照，从而控制日志的大小。

## 题目说明

实现基于快照的日志压缩功能：

1. 定期对状态机的当前状态创建快照
2. 记录快照对应的日志索引和任期号
3. 丢弃快照之前的所有日志条目
4. 节点恢复时，先从快照恢复状态，再重放快照之后的日志
5. 当某个跟随者（Follower）落后太多、领导者已经丢弃了它需要的日志条目时，通过 InstallSnapshot 消息将快照发送给该跟随者

这样就能防止日志无限增长。

## 概念说明

### 日志压缩

Raft 日志会随着命令不断到来而持续增长。快照机制将已经应用的日志条目压缩为一个紧凑的状态表示。恢复时只需要快照加上快照之后的日志即可。打个比方，这就像记账本，你不需要保留从开业至今的每一笔流水，只要知道上个月底的余额，再加上这个月的交易记录就够了。

### InstallSnapshot 远程调用

当一个跟随者落后太多，领导者已经把它所需的日志条目丢弃掉了，这时领导者会把快照直接发给该跟随者。跟随者用快照替换自己的状态，然后从快照之后的位置继续同步日志。

## 涉及概念

- `snapshot`
- `log compaction`
- `recovery`

## 实现提示

- 定期对状态机创建快照
- 丢弃快照之前的日志条目
- 向进度落后的跟随者发送快照

## 测试用例

### 1. 创建快照

创建一个快照，其 lastIncludedIndex=5、lastIncludedTerm=2，包含状态 {"x":1,"y":2}。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"seed_state","msg_id":2,"state":{"x":1,"y":2},"commit_index":5,"term":2}}
{"src":"c0","dest":"n1","body":{"type":"take_snapshot","msg_id":3,"up_to_index":5}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"seed_state_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"snapshot_ok","in_reply_to":3,"msg_id":2,"last_included_index":5,"last_included_term":2}}
```

## 参考资料

- [Raft Section 7](https://raft.github.io/raft.pdf)：Raft 论文中关于日志压缩的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
