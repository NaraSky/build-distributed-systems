# Implement Shuffle Phase with Hash Partitioning

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-3-shuffle-phase>

Track: 30. The MapReducer
Task order: 3
Short title: Shuffle Phase
Difficulty: advanced
Subtrack: MapReduce Fundamentals

## Problem

After the map phase, all values for the same key must reach the same reducer. The shuffle phase does exactly this: it **partitions** map outputs by key hash, **groups** values for each key, and optionally **combines** them locally to reduce network traffic.

Your node handles three shuffle operations:

```json
// Partition pairs across N reducers using hash(key) % N
{ "type": "partition", "msg_id": 1,
  "pairs": [["hello",1],["world",1],["hello",1]],
  "num_reducers": 2 }
→ { "type": "partitioned", "in_reply_to": 1,
    "partitions": [
      {"reducer_id": 0, "pairs": [["world",1]]},
      {"reducer_id": 1, "pairs": [["hello",2]]}
    ]}

// Group pairs by key (returns key → [values] map)
{ "type": "group", "msg_id": 2,
  "pairs": [["hello",1],["world",1],["hello",1]] }
→ { "type": "grouped", "in_reply_to": 2,
    "groups": {"hello": [1,1], "world": [1]} }

// Combine (local pre-reduce): sum values per key before sending over network
{ "type": "combine", "msg_id": 3,
  "pairs": [["hello",1],["world",1],["hello",1]] }
→ { "type": "combined", "in_reply_to": 3,
    "pairs": [["hello",2],["world",1]] }
```

For `partition`, after assigning pairs to reducer buckets, also group and sort keys alphabetically within each partition before returning.

## Concepts

- shuffle phase
- hash partitioning
- key grouping
- combiner
- reduce assignment

## Hints

- Partition key: reducer_id = hash(key) % num_reducers
- Use a simple string hash: sum of char codes, then abs() % num_reducers
- group collects all values for the same key before reduce
- combine is a local pre-reduce: sum values for the same key on the mapper side
- sort keys alphabetically within each partition

## Test Cases

### 1. Partition map outputs

Should assign pairs to reducers by hash(key) % num_reducers and aggregate within partition.

Input:

```json
{"src":"shuffler","dest":"partitioner","body":{"type":"partition","msg_id":1,"pairs":[["hello",1],["world",1],["hello",1]],"num_reducers":2}}
```

Expected output:

```text
{"type": "partitioned", "in_reply_to": 1, "partitions": [{"reducer_id": 0, "pairs": [["world", 1]]}, {"reducer_id": 1, "pairs": [["hello", 2]]}]}
```

### 2. Group by key

Should collect all values for each key.

Input:

```json
{"src":"shuffler","dest":"grouper","body":{"type":"group","msg_id":1,"pairs":[["hello",1],["world",1],["hello",1]]}}
```

Expected output:

```text
{"type": "grouped", "in_reply_to": 1, "groups": {"hello": [1, 1], "world": [1]}}
```

## Resources

- [Hadoop MapReduce Tutorial](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html): Covers shuffle and sort in depth

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
