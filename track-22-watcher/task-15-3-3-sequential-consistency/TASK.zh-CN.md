# 验证 ZAB 的顺序一致性

英文标题：Prove ZAB Sequential Consistency
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-3-sequential-consistency>

课程：22. 观察者
任务序号：13
短标题：Sequential Consistency
难度：高级
子主题：一致性与 ZAB 协议

## 中文导读

这道题要求你验证 ZAB 协议提供的顺序一致性保证。通俗地说，顺序一致性意味着"所有人看到的故事情节是一样的"——虽然某台服务器可能稍微慢一拍才看到最新数据，但所有服务器上事件发生的先后顺序绝对不会乱套。这比"最终一致性"强得多：最终一致性下你可能看到 A 和 B 的操作混在一起形成不可能的组合，但在顺序一致性下这绝不会发生。

## 题目说明

ZAB 提供顺序一致性（Sequential Consistency）保证：所有客户端以相同的全局顺序观察到所有更新。这是 ZooKeeper 最根本的一致性承诺。

顺序一致性具体包含三层含义：

1. **客户端内部有序**：同一个客户端发出的更新，一定按照发送顺序被执行，先发的先生效，后发的后生效。
2. **全局顺序统一**：所有客户端看到的更新序列完全相同。也就是说，不同客户端不会在"谁先谁后"这件事上产生分歧。
3. **读取可能略有延迟**：从跟随者读取数据时，可能还没拿到最新的已提交更新，因此读到的是稍旧的数据。这是顺序一致性和线性一致性（Linearizability）的区别——线性一致性要求读到的永远是最新值。

用一个例子来理解：假设客户端 A 依次写入 `/x = 1`、`/y = 2`，客户端 B 依次写入 `/x = 3`、`/y = 4`。在顺序一致性下，所有观察者要么看到"A 的操作全部在 B 之前"，要么看到"B 的操作全部在 A 之前"，绝不会出现交叉乱序的情况。而在最终一致性下，观察者可能看到 `/x=3, /y=2` 这样不一致的混合状态。

协议示例：

```json
Request:  {"type": "consistency_test", "msg_id": 1, "writes": [{"client": "A", "ops": [{"path": "/x", "value": "1"}, {"path": "/y", "value": "2"}]}, {"client": "B", "ops": [{"path": "/x", "value": "3"}, {"path": "/y", "value": "4"}]}]}
Response: {"type": "consistency_test_ok", "in_reply_to": 1, "total_order": ["A:/x=1", "A:/y=2", "B:/x=3", "B:/y=4"], "sequential_consistent": true, "violations": 0}
```

## 涉及概念

- `sequential consistency`
- `total order`
- `linearizability vs sequential`
- `ordering test`
- `consistency verification`

## 实现提示

- 顺序一致性要求所有客户端看到完全相同的更新顺序
- 它比线性一致性弱：从跟随者读取可能得到稍旧的数据
- 测试方法：让两个客户端并发写入，然后验证所有观察者是否以相同顺序看到这些写入
- 这个测试在最终一致性的系统中会失败，但在 ZAB 协议下能够通过
- ZAB 同时保证客户端内部的先进先出顺序和所有已提交写入的全局顺序

## 测试用例

### 1. 顺序一致性验证通过

验证说明：测试结果应显示通过顺序一致性检验，且违规次数为零。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"consistency_test","msg_id":2,"writes":[{"client":"A","ops":[{"path":"/x","value":"1"}]},{"client":"B","ops":[{"path":"/y","value":"2"}]}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 客户端内部的先进先出顺序得到保持

验证说明：在全局顺序中，同一个客户端的第一个操作必须出现在它的第二个操作之前。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"consistency_test","msg_id":2,"writes":[{"client":"A","ops":[{"path":"/a","value":"1"},{"path":"/a","value":"2"}]}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Consistency Guarantees](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkGuarantees)：ZooKeeper 官方文档中关于顺序一致性和排序保证的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
