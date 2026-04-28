# Implement Dynamic Scheduling with Locality Awareness

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-5-dynamic-scheduling>

Track: 24. The Scheduler
Task order: 10
Short title: Locality Scheduling
Difficulty: advanced
Subtrack: Distributed Work Allocation

## Problem

Moving a job to where its data lives is cheaper than shipping large data over the network. Locality-aware scheduling scores workers based on data proximity, then selects the best-scoring, least-loaded worker.

Implement a node that makes locality-aware scheduling decisions:

```json
// node-1 hosts the data but is 90% loaded; node-2 is in same rack, 30% loaded
{ "type": "submit_job", "msg_id": 1,
  "job": {"id":"job1","inputs":["data.csv"]},
  "topology": {"rack1":["node-1","node-2"]},
  "data_location": "node-1",
  "node-1_utilization": 0.9,
  "node-2_utilization": 0.3 }
-> { "type": "job_assigned", "in_reply_to": 1,
    "worker": "node-2",
    "reason": "Same rack as data (rack1) and less loaded than node-1" }

// Data moves to node-5 -> future jobs follow it
{ "type": "update_data_location", "msg_id": 1,
  "file": "data.csv", "old_location": "node-1", "new_location": "node-5" }
{ "type": "submit_job", "msg_id": 2,
  "job": {"id":"job1","inputs":["data.csv"]} }
-> { "type": "job_assigned", "in_reply_to": 2,
    "worker": "node-5", "reason": "Data moved to node-5" }
```

## Concepts

- data locality
- rack awareness
- worker scoring
- dynamic data placement
- load vs locality tradeoff

## Hints

- Score workers: +2 if it hosts all input files, +1 if in the same rack, 0 otherwise
- Among equal locality scores, prefer the worker with lower current utilization
- Rack-aware: same-rack worker preferred over cross-rack even if the exact data node is overloaded
- update_data_location changes the data map; subsequent jobs use the new location
- locality_aware balances speed and fairness: faster than load-balancing, more even than locality-only

## Test Cases

### 1. Locality-aware scheduling

Should prefer the worker hosting the most input data.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"workers":["node-1","node-2","node-3"],"data_map":{"file1.txt":["node-1"],"file2.txt":["node-2"]}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"job1","inputs":["file1.txt","file2.txt"]}}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Rack-aware scheduling

node-2 (same rack, lower utilization) should be preferred over overloaded node-1.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"job1","inputs":["data.csv"]},"topology":{"rack1":["node-1","node-2"],"rack2":["node-3","node-4"]},"data_location":"node-1","node-1_utilization":0.9,"node-2_utilization":0.3}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_assigned", "in_reply_to": 1, "worker": "node-2", "reason": "Same rack as data (rack1) and less loaded than node-1"}}
```

## Resources

- [Data Locality in Hadoop](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html): How Hadoop uses data locality for scheduling decisions

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
