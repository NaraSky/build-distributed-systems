# Implement ZAB Atomic Broadcast Protocol

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-1-zab>

Track: 22. The Watcher
Task order: 11
Short title: ZAB Broadcast
Difficulty: advanced
Subtrack: Consistency and the ZAB Protocol

## Problem

ZAB (ZooKeeper Atomic Broadcast) is the consensus protocol that keeps all ZooKeeper servers in sync. It guarantees that all servers see updates in the same order.

**ZAB 2-phase protocol**:
1. **Propose**: leader assigns a monotonically increasing `zxid` to the update and broadcasts a PROPOSAL to all followers
2. **ACK**: each follower writes the proposal to its WAL and sends an ACK to the leader
3. **Commit**: when the leader receives ACKs from a **quorum** (majority), it broadcasts COMMIT
4. **Apply**: each follower (and the leader) applies the committed update to the in-memory ZNode tree

**Ordering guarantee**: because `zxid` is monotonically increasing and proposals are applied in order, all servers see the same sequence of updates (sequential consistency).

```json
Request:  {"type": "zab_propose", "msg_id": 1, "operation": "SetData", "path": "/config", "data": "v2", "zxid": "0x100000001"}
Response: {"type": "zab_propose_ok", "in_reply_to": 1, "acks_received": 2, "quorum_size": 2, "committed": true}
```

## Concepts

- ZAB
- atomic broadcast
- 2-phase commit
- proposal
- quorum acknowledgement

## Hints

- Leader receives a write request and creates a proposal with a unique zxid
- Leader broadcasts the proposal to all followers
- Followers write the proposal to their local WAL and send ACK to the leader
- When the leader receives ACKs from a quorum (majority), it sends COMMIT
- Followers apply the committed proposal to their in-memory tree

## Test Cases

### 1. Proposal with quorum commits

zab_propose_ok should show committed: true when acks >= quorum.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":2,"operation":"SetData","path":"/cfg","data":"v1","zxid":"0x100000001"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Sequential zxids are ordered

Both proposals should commit in zxid order.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":2,"operation":"SetData","path":"/a","data":"1","zxid":"0x100000001"}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":3,"operation":"SetData","path":"/b","data":"2","zxid":"0x100000002"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZAB Protocol](https://zookeeper.apache.org/doc/current/zookeeperInternals.html#sc_atomicBroadcast): ZooKeeper documentation on Atomic Broadcast protocol

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
