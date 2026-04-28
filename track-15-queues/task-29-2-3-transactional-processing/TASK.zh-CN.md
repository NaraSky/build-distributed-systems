# 实现事务性消息处理

英文标题：Implement Transactional Message Processing
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-3-transactional-processing>

课程：15. 队列
任务序号：8
短标题：事务性处理
难度：高级
子主题：精确一次投递

## 中文导读

本题要求你实现事务性消息处理，确保"消费消息"和"更新数据库"这两个操作要么同时成功、要么同时失败，从而实现精确一次语义。这就像银行转账一样——扣款和入账必须是一个整体，不能只做一半。掌握这种模式对于构建可靠的分布式系统至关重要。

## 题目说明

事务性消息处理通过协调提交（Coordinated Commit）保证消息消费与数据库更新之间的原子性，从而实现精确一次语义。

**事务性处理要解决的问题**：消息处理和状态更新必须是原子的。下面是一个典型的问题场景：
1. 消费者接收到消息
2. 消费者更新了数据库
3. 消费者在发送确认之前崩溃了
4. 队列重新投递该消息
5. 消费者再次更新数据库，导致数据重复

解决方案是使用事务性处理：将"读取消息、处理消息、更新数据库、提交偏移量"这些操作放在一个原子事务中完成。这样做的好处是：不会出现部分更新、不会重复处理、状态始终一致、实现精确一次语义。

**事务性消费者**：通过在数据库事务中处理消息，确保只有在数据库提交成功后才发送确认。如果出错则回滚事务，不发送确认，消息会被重新投递。

**付款处理示例**：在同一个事务中检查付款是否已存在（保证幂等性）、插入付款记录、更新用户余额，所有数据库操作共享同一个事务以保证原子性。

**队列与数据库的协调**：需要一个协调器来管理队列和数据库之间的配合。处理流程为：启动数据库事务、处理消息、提交数据库事务、确认消息。出错时：回滚数据库事务、不确认消息、消息会被重新投递重试。

**事务隔离级别**：不同的隔离级别（读未提交、读已提交、可重复读、串行化）提供不同程度的并发保护。更高的隔离级别能防止并发修改问题，但可能降低系统吞吐量。

**死信队列处理**：结合重试逻辑，当消息处理多次失败后，将其移入死信队列并确认原消息，防止有毒消息阻塞主队列。

**核心优势**：原子操作保证消息处理和状态更新同时成功或同时失败；只有处理成功后才提交偏移量，避免重复处理；失败时回滚所有部分更新；利用数据库的 ACID 特性保持一致性；协调队列确认与事务提交。

## 涉及概念

- `transactional processing`
- `atomic operations`
- `database transactions`
- `message acknowledgment`
- `exactly-once semantics`

## 实现提示

- 原子操作：在一个事务中完成消息处理和状态更新
- 提交偏移量：只有处理成功后才发送确认
- 失败回滚：如果提交失败，撤销所有处理操作
- 数据库事务：利用 ACID 特性保证一致性
- 队列集成：协调队列和数据库的提交操作

## 测试用例

### 1. 事务性处理消息

应当成功处理消息并提交事务。

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-1","data":{"user_id":"user-123","amount":100}}}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "message_id": "msg-1", "committed": true, "acked": true}
```

### 2. 失败时回滚

应当在处理失败时回滚事务。

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-2","data":{"user_id":"user-456","amount":-1000}}}}
```

期望输出：

```text
{"type": "failed", "in_reply_to": 1, "message_id": "msg-2", "rolled_back": true, "acked": false}
```

## 参考资料

- [Transactional Messaging](https://www.enterpriseintegrationpatterns.com/patterns/messaging/TransactionalClient.html)：事务性客户端模式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
