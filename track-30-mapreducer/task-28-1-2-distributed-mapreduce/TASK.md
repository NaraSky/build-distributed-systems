# Implement Distributed MapReduce

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-2-distributed-mapreduce>

Track: 30. The MapReducer
Task order: 2
Short title: Distributed MapReduce
Difficulty: advanced
Subtrack: MapReduce Fundamentals

## Problem

Single-machine MapReduce is limited by one CPU and one memory space. Distributed MapReduce sends different data chunks to different workers so all workers map in parallel, then the master merges and reduces.

Your node plays the role of the **master**. It receives a `distribute` job request and must coordinate the workers listed in the message:

```json
// Master receives a distribute request
{ "type": "distribute", "msg_id": 1,
  "lines": ["hello world", "hello mapreduce", "world peace"],
  "workers": ["n2", "n3"] }

// Master splits lines evenly and sends to each worker
→ sends to n2: { "type": "map_chunk", "chunk": ["hello world", "hello mapreduce"] }
→ sends to n3: { "type": "map_chunk", "chunk": ["world peace"] }

// Workers reply with their map results
← n2: { "type": "chunk_result", "pairs": [["hello",1],["world",1],["hello",1],["mapreduce",1]] }
← n3: { "type": "chunk_result", "pairs": [["world",1],["peace",1]] }

// Master merges, reduces, and replies
→ { "type": "distribute_result", "in_reply_to": 1,
    "results": {"hello":2,"world":2,"mapreduce":1,"peace":1} }
```

Split the input into `len(workers)` chunks, forward each chunk, collect all pair lists, then run the same reduce logic from task 1 over the merged pairs.

## Concepts

- distributed MapReduce
- worker nodes
- job splitting
- parallel processing
- result merging

## Hints

- split divides the input array into equal-sized chunks, one per worker
- assign sends each chunk to a worker and waits for its map result
- merge combines all worker outputs before the reduce phase
- The master coordinates workers; workers only map their assigned chunk
- Use worker count to decide chunk size: ceil(total / workers)

## Test Cases

### 1. Split input into chunks

Should split lines evenly into the requested number of chunks.

Input:

```json
{"src":"client","dest":"master","body":{"type":"split","msg_id":1,"lines":["a","b","c","d"],"num_chunks":2}}
```

Expected output:

```text
{"type": "split_result", "in_reply_to": 1, "chunks": [["a", "b"], ["c", "d"]]}
```

### 2. Merge worker results

Should merge and reduce all worker pair arrays.

Input:

```json
{"src":"client","dest":"master","body":{"type":"merge","msg_id":1,"worker_results":[[["hello",1],["world",1]],[["hello",1],["peace",1]]]}}
```

Expected output:

```text
{"type": "merge_result", "in_reply_to": 1, "results": {"hello": 2, "world": 1, "peace": 1}}
```

## Resources

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/): Original Google MapReduce paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
