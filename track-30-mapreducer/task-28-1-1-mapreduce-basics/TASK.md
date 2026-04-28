# Implement Single-Machine MapReduce

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-1-mapreduce-basics>

Track: 30. The MapReducer
Task order: 1
Short title: MapReduce Basics
Difficulty: intermediate
Subtrack: MapReduce Fundamentals

## Problem

MapReduce splits work into two simple phases: **map** transforms each input record into key-value pairs, and **reduce** aggregates all values for the same key.

Your node handles three message types:

```json
// Map a single line into word-count pairs
{ "type": "map", "msg_id": 1, "line": "hello world hello" }
→ { "type": "map_result", "in_reply_to": 1, "pairs": [["hello",1],["world",1],["hello",1]] }

// Reduce a list of values for one key
{ "type": "reduce", "msg_id": 2, "key": "hello", "values": [1,1,1] }
→ { "type": "reduce_result", "in_reply_to": 2, "result": ["hello", 3] }

// Execute a full word-count job over multiple lines
{ "type": "execute", "msg_id": 3, "lines": ["hello world", "hello mapreduce"] }
→ { "type": "job_result", "in_reply_to": 3, "results": {"hello":2,"world":1,"mapreduce":1} }
```

The execute flow: run map on every line → collect all pairs → group pairs by key → reduce each group → return the final counts.

## Concepts

- MapReduce
- map phase
- reduce phase
- word count
- key-value pairs
- shuffle

## Hints

- Map emits (word, 1) for each word in the input line
- Reduce sums all values for the same key
- execute runs map on each line, groups by key, then reduces
- Use a plain dict/map to accumulate counts during reduce
- Strip and lowercase words before emitting from map

## Test Cases

### 1. Map word to pairs

Should emit one (word, 1) pair per word token.

Input:

```json
{"src":"client","dest":"mapreduce","body":{"type":"map","msg_id":1,"line":"hello world hello"}}
```

Expected output:

```text
{"type": "map_result", "in_reply_to": 1, "pairs": [["hello", 1], ["world", 1], ["hello", 1]]}
```

### 2. Reduce word counts

Should sum all values for the given key.

Input:

```json
{"src":"client","dest":"mapreduce","body":{"type":"reduce","msg_id":1,"key":"hello","values":[1,1,1]}}
```

Expected output:

```text
{"type": "reduce_result", "in_reply_to": 1, "result": ["hello", 3]}
```

## Resources

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/): The original Google MapReduce paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
