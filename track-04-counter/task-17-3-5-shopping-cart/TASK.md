# Build a Distributed Shopping Cart with CRDTs

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-5-shopping-cart>

Track: 4. The Counter
Task order: 15
Short title: CRDT Shopping Cart
Difficulty: advanced
Subtrack: More CRDTs

## Problem

A distributed shopping cart demonstrates CRDTs solving a real-world problem. Using an OR-Set, items can be added and removed from the cart across partitioned nodes, and the cart always converges after healing.

**Cart operations**:
- `add_item(item_id, qty)`: add an item with a quantity (uses OR-Set add with unique tag)
- `remove_item(item_id)`: remove all observed entries for the item
- `view_cart()`: return all items in the cart with quantities

**Partition scenario**:
1. Nodes A and B are partitioned
2. User on A adds "milk" to cart
3. User on B removes "bread" from cart
4. Partition heals, nodes merge
5. Result: cart has milk (added on A), no bread (removed on B), plus any pre-existing items

```json
Request:  {"type": "cart_add", "msg_id": 1, "item": "milk", "qty": 2}
Response: {"type": "cart_add_ok", "in_reply_to": 1, "cart_size": 1}

Request:  {"type": "cart_view", "msg_id": 2}
Response: {"type": "cart_view_ok", "in_reply_to": 2, "items": [{"item": "milk", "qty": 2}, {"item": "bread", "qty": 1}], "total_items": 2}
```

## Concepts

- shopping cart
- OR-Set application
- partition tolerance
- add-remove conflict
- convergence

## Hints

- Model the cart as an OR-Set of (item_id, quantity) pairs
- Add item: or_set.add((item_id, quantity))
- Remove item: or_set.remove(item_id) removes all observed entries for that item
- Under partition, both sides can add/remove independently — cart stays available
- After partition heals, merge: add-wins semantics resolve conflicts

## Test Cases

### 1. Add items to cart

cart_view_ok items should include both milk and bread.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"cart_add","msg_id":2,"item":"milk","qty":2}}
{"src":"c1","dest":"n1","body":{"type":"cart_add","msg_id":3,"item":"bread","qty":1}}
{"src":"c1","dest":"n1","body":{"type":"cart_view","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Remove item from cart

cart_view_ok should not include eggs after removal.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"cart_add","msg_id":2,"item":"eggs","qty":12}}
{"src":"c1","dest":"n1","body":{"type":"cart_remove","msg_id":3,"item":"eggs"}}
{"src":"c1","dest":"n1","body":{"type":"cart_view","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Dynamo Shopping Cart](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): Amazon Dynamo paper - shopping cart as a motivating use case for CRDTs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
