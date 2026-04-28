# 在跟随者读中保证"读己之写"

英文标题：Guarantee Read-Your-Writes with Follower Reads
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-4-read-your-writes>

课程：7. 存储：线性一致键值存储
任务序号：9
短标题：Read-Your-Writes
难度：高级
子主题：读优化

## 中文导读

这道题要求你在跟随者读的基础上保证"读己之写"（Read-Your-Writes）一致性。也就是说，客户端写入一个值后，紧接着去读，一定能读到自己刚写入的值，即使读请求是由跟随者处理的。这通过让客户端携带最后一次写入的提交索引来实现，是兼顾读性能和用户体验的关键技术。

## 题目说明

在使用跟随者读时，确保"读己之写"一致性。客户端在每次读请求中携带 `last_write_index`（最后一次写入对应的提交索引），跟随者只有在自己已经应用到该索引时才处理读请求。

```json
Request:  {"type": "write", "msg_id": 1, "key": "x", "value": "new"}
Response: {"type": "write_ok", "in_reply_to": 1, "commit_index": 10}

Request:  {"type": "ryw_read", "msg_id": 2, "key": "x", "last_write_index": 10, "prefer_follower": true}
Response: {"type": "ryw_read_ok", "in_reply_to": 2, "value": "new", "served_by": "n2", "follower_applied_index": 10, "waited_ms": 50}

Request:  {"type": "ryw_read", "msg_id": 3, "key": "x", "last_write_index": 15, "prefer_follower": true}
Response: {"type": "ryw_read_ok", "in_reply_to": 3, "value": "new", "served_by": "n1", "reason": "follower_behind_redirected_to_leader"}
```

## 涉及概念

- `read-your-writes`
- `session consistency`
- `commit index tracking`
- `client token`

## 实现提示

- 客户端在每次读请求中携带自己上次看到的 commit_index
- 跟随者只有在自己已经应用到至少该索引时，才处理读请求
- 如果跟随者的进度落后，要么等待它赶上，要么将请求重定向到领导者
- 这种方案把跟随者读的可扩展性和"读己之写"保证结合在了一起
- 客户端需要从写响应中记录 commit_index

## 测试用例

### 1. 从跟随者实现"读己之写"

验证 ryw_read_ok 中 follower_applied_index 大于等于 5。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ryw_read","msg_id":2,"key":"x","last_write_index":5,"prefer_follower":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 跟随者落后时重定向到领导者

跟随者不太可能已经应用到索引 999，因此应该重定向到领导者处理。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ryw_read","msg_id":2,"key":"x","last_write_index":999,"prefer_follower":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Session Guarantees for Weakly Consistent Data](https://www.cs.utexas.edu/~lorenzo/corsi/cs380d/papers/SessionGuarantees.pdf)：关于"读己之写"及其他会话一致性保证的形式化定义

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
