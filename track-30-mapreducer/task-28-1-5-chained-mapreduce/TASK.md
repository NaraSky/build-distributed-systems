# Implement Chained MapReduce Pipeline

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-5-chained-mapreduce>

Track: 30. The MapReducer
Task order: 5
Short title: Chained MapReduce
Difficulty: advanced
Subtrack: MapReduce Fundamentals

## Problem

Complex data analysis often needs multiple MapReduce stages. A chained pipeline feeds the output of one job directly as input to the next, keeping each job focused on a single transformation.

Example use-case: find the top 3 most frequent words across a document set.

```
Stage 1 (word count):  ["hello world", "hello there"]
                       → {"hello":2, "world":1, "there":1}

Stage 2 (sort by freq): {"hello":2, "world":1, "there":1}
                        → [["hello",2], ["world",1], ["there",1]]

Stage 3 (top N):        [["hello",2], ["world",1], ["there",1]], N=2
                        → [["hello",2], ["world",1]]
```

Your node handles a single `pipeline` message that runs all three stages and returns each stage's output:

```json
{ "type": "pipeline", "msg_id": 1,
  "lines": ["hello world", "hello there", "world peace"],
  "top_n": 2 }
→ { "type": "pipeline_result", "in_reply_to": 1,
    "stage1": {"hello":2,"world":2,"there":1,"peace":1},
    "stage2": [["hello",2],["world",2],["there",1],["peace",1]],
    "stage3": [["hello",2],["world",2]] }
```

When frequencies are equal (hello and world both 2), sort those keys alphabetically as a tiebreaker so the output is deterministic.

## Concepts

- pipeline
- job chaining
- multi-stage processing
- intermediate data
- top-N
- secondary sort

## Hints

- Run jobs in order: output of job[i] becomes input of job[i+1]
- Job 1 is a word count (map → reduce)
- Job 2 sorts the word-count results by frequency descending
- Job 3 takes the top N entries from the sorted list
- Return intermediate results for each stage so the caller can inspect them

## Test Cases

### 1. Run full pipeline

Should run all three stages and return each stage output.

Input:

```json
{"src":"client","dest":"pipeline","body":{"type":"pipeline","msg_id":1,"lines":["hello world","hello there","world peace"],"top_n":2}}
```

Expected output:

```text
{"type": "pipeline_result", "in_reply_to": 1, "stage1": {"hello": 2, "world": 2, "there": 1, "peace": 1}, "stage2": [["hello", 2], ["world", 2], ["peace", 1], ["there", 1]], "stage3": [["hello", 2], ["world", 2]]}
```

### 2. Top 1 word

top_n=1 should return only the most frequent word.

Input:

```json
{"src":"client","dest":"pipeline","body":{"type":"pipeline","msg_id":1,"lines":["a b a","a c"],"top_n":1}}
```

Expected output:

```text
{"type": "pipeline_result", "in_reply_to": 1, "stage1": {"a": 3, "b": 1, "c": 1}, "stage2": [["a", 3], ["b", 1], ["c", 1]], "stage3": [["a", 3]]}
```

## Resources

- [Chaining MapReduce Jobs in Hadoop](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html): Multi-stage job chaining patterns

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
