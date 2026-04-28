# Handle Init Message and Store Cluster Metadata

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-init-handler>

Track: 1. The Messenger
Task order: 2
Short title: Init Handler
Difficulty: beginner
Subtrack: Hello, Distributed World

## Problem

Before processing any workload, Maelstrom sends an init message to each node. This message tells your node its identity and the full cluster membership.

The init message looks like:

```json
{
  "type": "init",
  "msg_id": 1,
  "node_id": "n1",
  "node_ids": ["n1", "n2", "n3"]
}
```

Your task is to handle the init message by storing the node_id (your identity) and node_ids (all cluster members). Then respond with an init_ok message:

```json
{
  "type": "init_ok",
  "in_reply_to": 1
}
```

The in_reply_to field must match the msg_id from the init request.

## Concept Notes

## Node Initialization

Every distributed system needs a **bootstrap phase** where nodes learn about themselves and their peers. The init message serves this purpose in Maelstrom.

### Understanding Identity

The `node_id` field gives your node its **unique identity**. This is critical because:

  - All messages you send must use this as the `src` field

  - Other nodes will address messages to you using this ID

  - Your identity distinguishes you from other nodes in the cluster

### Cluster Topology

The `node_ids` array tells you about **all nodes in the cluster**. This information becomes essential for:

  - **Broadcast algorithms** - knowing who to send messages to

  - **Consensus protocols** - calculating quorums

  - **Leader election** - participating in voting

### Request-Response Pattern

The `in_reply_to` field establishes a **correlation** between requests and responses. This pattern is fundamental in distributed systems where you need to match responses to outstanding requests.

```text
Request:  { "type": "init", "msg_id": 1, ... }
Response: { "type": "init_ok", "in_reply_to": 1 }
```

This correlation allows the sender to:

  - Track which requests have been answered

  - Implement timeouts for unresponsive nodes

  - Handle out-of-order message delivery

## Concepts

- initialization
- node identity
- cluster topology

## Hints

- The init message contains node_id and node_ids fields
- Store these values for use in subsequent message handling
- Reply with init_ok message type

## Test Cases

### 1. Respond to init

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Maelstrom Initialization](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md#initialization): Details on the init message and expected response

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
