# 用 CRDT 构建分布式购物车

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-5-shopping-cart>

课程：4. 计数器：分布式状态与 CRDT
任务序号：15
短标题：CRDT 购物车
难度：高级
子主题：更多 CRDT

## 中文导读

这道题让你用 CRDT 解决一个真实的工程问题：分布式购物车。基于 OR-Set，用户可以在网络分区的不同节点上自由地添加和删除商品，网络恢复后购物车会自动合并并收敛到一致的状态。这就是 Amazon Dynamo 论文中经典的购物车案例。

## 题目说明

分布式购物车展示了 CRDT 如何解决实际问题。基于 OR-Set，商品可以在发生网络分区的不同节点上被添加和删除，购物车在网络恢复后始终能收敛到一致状态。

**购物车操作**：
- `add_item(item_id, qty)`：添加一个商品及其数量（使用 OR-Set 的 add 操作，附带唯一标签）
- `remove_item(item_id)`：删除该商品的所有已观察到的条目
- `view_cart()`：返回购物车中所有商品及其数量

**网络分区场景**：
1. 节点 A 和节点 B 之间发生网络分区
2. 用户在 A 上向购物车添加了"牛奶"
3. 用户在 B 上从购物车删除了"面包"
4. 分区恢复，节点合并状态
5. 结果：购物车中有牛奶（在 A 上添加的），没有面包（在 B 上删除的），以及其他原有商品

```json
Request:  {"type": "cart_add", "msg_id": 1, "item": "milk", "qty": 2}
Response: {"type": "cart_add_ok", "in_reply_to": 1, "cart_size": 1}

Request:  {"type": "cart_view", "msg_id": 2}
Response: {"type": "cart_view_ok", "in_reply_to": 2, "items": [{"item": "milk", "qty": 2}, {"item": "bread", "qty": 1}], "total_items": 2}
```

## 涉及概念

- `shopping cart`
- `OR-Set application`
- `partition tolerance`
- `add-remove conflict`
- `convergence`

## 实现提示

- 将购物车建模为一个 OR-Set，其中每个元素是 (商品ID, 数量) 对
- 添加商品：or_set.add((item_id, quantity))
- 删除商品：or_set.remove(item_id) 删除该商品的所有已观察条目
- 在网络分区期间，两边都可以独立地添加和删除商品，购物车始终保持可用
- 分区恢复后合并：添加优先的语义解决冲突

## 测试用例

### 1. 向购物车添加商品

验证 cart_view_ok 的 items 应包含 milk 和 bread。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"cart_add","msg_id":2,"item":"milk","qty":2}}
{"src":"c1","dest":"n1","body":{"type":"cart_add","msg_id":3,"item":"bread","qty":1}}
{"src":"c1","dest":"n1","body":{"type":"cart_view","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 从购物车删除商品

验证删除后 cart_view_ok 不应包含 eggs。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"cart_add","msg_id":2,"item":"eggs","qty":12}}
{"src":"c1","dest":"n1","body":{"type":"cart_remove","msg_id":3,"item":"eggs"}}
{"src":"c1","dest":"n1","body":{"type":"cart_view","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Dynamo Shopping Cart](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：Amazon Dynamo 论文，以购物车作为 CRDT 的经典应用案例

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
