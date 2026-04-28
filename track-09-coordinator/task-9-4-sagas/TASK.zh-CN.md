# 实现 Saga 模式

网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-4-sagas>

课程：9. 协调器：分布式事务
任务序号：4
短标题：Sagas
难度：高级
子主题：两阶段提交

## 中文导读

这道题要求你实现 Saga 模式，这是微服务架构中处理分布式事务最常用的方案之一。它的核心思路是把一个大事务拆成一连串小事务，每个小事务都配备一个"补偿操作"。如果中途某一步失败了，就按相反的顺序逐个执行补偿，把已完成的步骤"撤销"掉，从而保证系统最终回到一致的状态。

## 题目说明

在分布式系统中，跨多个服务的事务不能像单机数据库那样用一个事务来包裹。Saga 模式（Saga Pattern）提供了一种务实的解决方案：把一个大事务拆分成一系列本地事务，每个本地事务负责完成一个步骤的工作，同时定义好对应的补偿操作（Compensating Transaction）——也就是"如何撤销这一步"。

所有步骤按顺序依次执行。如果每一步都成功了，事务就完成了。如果某一步失败了，就从失败的地方开始，按相反的顺序逐个调用前面已完成步骤的补偿操作。比如一个电商下单流程包含"预留库存、扣款、发货"三步，如果在扣款这一步失败了，就需要调用"释放库存"来撤销第一步的预留。

与两阶段提交不同，Saga 不需要长时间持有全局锁，各步骤独立提交。这意味着它的性能更好、可扩展性更强，但代价是只能保证最终一致性（Eventual Consistency），而非严格的强一致性。在实际的微服务架构中，这种取舍通常是值得的。

## 涉及概念

- saga
- compensation
- eventual consistency

## 实现提示

- 每个步骤都必须定义对应的补偿操作，确保可以撤销
- 失败时按相反顺序执行已完成步骤的补偿
- 采用最终一致性模型：各步骤独立提交，不需要全局锁

## 测试用例

### 1. 按顺序执行所有步骤

验证：三个步骤（预留库存、扣款、发货）应当按顺序全部执行成功。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"saga_execute","msg_id":2,"saga_id":"saga1","steps":[{"name":"reserve_inventory","action":"reserve","compensation":"release"},{"name":"charge_payment","action":"charge","compensation":"refund"},{"name":"ship_order","action":"ship","compensation":"cancel_shipment"}]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"saga_execute_ok","in_reply_to":2,"msg_id":1,"saga_id":"saga1","status":"completed","steps_executed":["reserve_inventory","charge_payment","ship_order"]}}
```

## 参考资料

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)：微服务架构中 Saga 模式的详细文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
