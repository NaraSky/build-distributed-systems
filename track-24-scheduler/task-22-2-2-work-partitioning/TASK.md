# Implement MapReduce-Style Work Partitioning

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-2-work-partitioning>

Track: 24. The Scheduler
Task order: 7
Short title: Work Partitioning
Difficulty: advanced
Subtrack: Distributed Work Allocation

## Problem

Large datasets are split into partitions so multiple workers can process them simultaneously. The partitioning strategy controls how evenly work is distributed, which directly affects total job time.

Implement a node that partitions work and handles stragglers:

```json
// Split 1TB input evenly across 4 workers
{ "type": "submit_mapreduce", "msg_id": 1,
  "input": "s3://data/*.txt", "map": "wordcount", "num_partitions": 4 }
-> { "type": "job_submitted", "in_reply_to": 1,
    "job_id": "mr1",
    "partition_sizes": [256, 256, 256, 256], "workers": [1,2,3,4] }

// Hash beats range on skewed keys
{ "type": "benchmark_partitioning", "msg_id": 2,
  "strategies": ["range","hash"], "data": "keys_with_skew" }
-> results: range skew_factor=5.0, hash skew_factor=1.2

// Slow partition -> speculative execution on backup worker
{ "type": "submit_mapreduce", ...,
  "straggler_partition": 2, "straggler_slowdown": 5 }
-> { "type": "straggler_detected",
    "partition": 2, "action": "speculative_execution", "backup_worker": 5 }
```

## Concepts

- hash partitioning
- range partitioning
- data skew
- straggler mitigation
- speculative execution

## Hints

- Hash partitioning: partition_id = hash(job_id) % num_partitions — distributes evenly even for skewed keys
- Skew factor = max_partition_size / avg_partition_size — closer to 1.0 means more balanced
- Range partitioning produces unequal partitions when key distribution is skewed
- A straggler is a partition whose runtime exceeds 2x the median of completed partitions
- Speculative execution: launch a backup copy on another worker and take whichever finishes first

## Test Cases

### 1. Partition input data

Input should be split into 4 equal partitions.

Input:

```json
{"src":"client","dest":"mr_cluster","body":{"type":"submit_mapreduce","msg_id":1,"input":"s3://data/*.txt","map":"wordcount","num_partitions":4}}
```

Expected output:

```text
{"src": "mr_cluster", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 1, "job_id": "mr1", "partition_sizes": [256, 256, 256, 256], "workers": [1,2,3,4]}}
```

### 2. Hash partitioning distribution

Hash should have much lower skew_factor than range on skewed data.

Input:

```json
{"src":"client","dest":"mr_cluster","body":{"type":"benchmark_partitioning","msg_id":1,"strategies":["range","hash"],"data":"keys_with_skew","num_partitions":4}}
```

Expected output:

```text
{"src": "mr_cluster", "dest": "client", "body": {"type": "benchmark_complete", "in_reply_to": 1, "results": {"range": {"skew_factor": 5.0}, "hash": {"skew_factor": 1.2}}}}
```

## Resources

- [MapReduce Paper](https://research.google/pubs/pub62/): Original Google MapReduce paper covering partitioning and straggler mitigation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
