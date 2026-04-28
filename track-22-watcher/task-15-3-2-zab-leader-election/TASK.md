# Implement ZAB Leader Election with FastLeaderElection

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-2-zab-leader-election>

Track: 22. The Watcher
Task order: 12
Short title: ZAB Election
Difficulty: advanced
Subtrack: Consistency and the ZAB Protocol

## Problem

ZAB leader election selects the server with the most up-to-date transaction log (highest `zxid`) as the new leader. This minimizes data synchronization after election.

**FastLeaderElection algorithm**:
1. Each server starts by voting for itself: `(myId, myZxid)`
2. Servers exchange votes. If a received vote has a higher zxid (or higher server ID as tiebreaker), update your vote to match.
3. Continue until a quorum (majority) of servers all vote for the same candidate.
4. The elected leader enters the **synchronization phase**: sends missing proposals to followers.
5. After synchronization, the leader begins serving requests.

**Epoch**: each new leader increments the epoch (upper 32 bits of zxid). This fences stale leaders.

```json
Request:  {"type": "zab_election", "msg_id": 1}
Response: {"type": "zab_election_ok", "in_reply_to": 1, "leader": "n2", "leader_zxid": "0x200000005", "epoch": 2, "rounds": 3, "votes_received": {"n1": "n2", "n2": "n2", "n3": "n2"}}
```

## Concepts

- ZAB leader election
- FastLeaderElection
- zxid comparison
- epoch
- voting rounds

## Hints

- The server with the highest zxid (most up-to-date log) wins the election
- FastLeaderElection: each server proposes itself, then updates its vote to the server with the highest zxid
- Voting continues in rounds until a quorum agrees on the same candidate
- After election, the leader synchronizes followers (sends missing proposals)
- The epoch increments on each new leader to fence stale leaders

## Test Cases

### 1. Election produces a leader

zab_election_ok should include leader, leader_zxid, epoch, and votes_received.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_election","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Quorum votes for same leader

A majority of votes_received values should match the leader.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_election","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZAB Leader Election](https://zookeeper.apache.org/doc/current/zookeeperInternals.html#sc_leaderElection): ZooKeeper documentation on FastLeaderElection algorithm

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
