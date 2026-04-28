# 构建 a Distributed Shopping Cart，包含CRDTs

英文标题：Build a Distributed Shopping Cart，包含CRDTs
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-5-shopping-cart>

课程：4. 计数器：分布式状态与 CRDT
任务序号：15
短标题：CRDT Shopping Cart
难度：advanced
子主题：More CRDTs

## 中文导读

本题要求你完成 `构建 a Distributed Shopping Cart，包含CRDTs`。

重点关注：`shopping cart`、`OR-Set application`、`partition tolerance`、`add-remove conflict`、`convergence`。

建议先按提示逐步实现：Model the cart as an OR-Set of (item_id, quantity) pairs。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A distributed shopping cart demonstrates CRDTs solving a real-world problem.使用an OR-Set, items can be added和removed from the cart across partitioned 节点,和the cart always converges after healing.

**Cart operations**:
- `add_item(item_id, qty)`: add an item，包含a quantity (uses OR-Set add，包含unique tag)
- `remove_item(item_id)`: remove all observed entries用于the item
- `view_cart()`: return all items in the cart，包含quantities

**Partition scenario**:
1. 节点 A和B are partitioned
2. User on A adds "milk" to cart
3. User on B removes "bread" from cart
4. Partition heals, 节点 merge
5. Result: cart has milk (added on A), no bread (removed on B), plus any pre-existing items

```JSON
请求:  {"type": "cart_add", "msg_id": 1, "item": "milk", "qty": 2}
响应: {"type": "cart_add_ok", "in_reply_to": 1, "cart_size": 1}

请求:  {"type": "cart_view", "msg_id": 2}
响应: {"type": "cart_view_ok", "in_reply_to": 2, "items": [{"item": "milk", "qty": 2}, {"item": "bread", "qty": 1}], "total_items": 2}
```

## 涉及概念

- `shopping cart`
- `OR-Set application`
- `partition tolerance`
- `add-remove conflict`
- `convergence`

## 实现提示

-模式l the cart as an OR-Set of (item_id, quantity) pairs
- Add item: or_set.add((item_id, quantity))
- Remove item: or_set.remove(item_id) removes all observed entries用于that item
- Under partition, both sides can add/remove independently — cart stays available
- After partition heals, merge: add-wins semantics resolve conflicts

## 测试用例

### 1. 添加 items to cart

cart_view_ok items should include both milk和bread.

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

### 2. Remove item from cart

cart_view_ok should not include eggs after removal.

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

- [Dynamo Shopping Cart](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：Amazon Dynamo paper - shopping cart as a motivating use case用于CRDTs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
