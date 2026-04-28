# Implement MapReduce

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-1-mapreduce>

Track: 10. Advanced
Task order: 1
Short title: MapReduce
Difficulty: advanced
Subtrack: Advanced Paradigms

## Problem

Implement MapReduce: Map emits (key, value) pairs, shuffle groups by key, Reduce aggregates. Build word count as example.

## Concept Notes

### MapReduce

MapReduce splits batch jobs into parallelizable map and reduce phases. Map transforms data, Reduce aggregates. Shuffle handles data movement between phases.

## Concepts

- MapReduce
- batch processing
- word count

## Hints

- Map phase: emit key-value pairs
- Shuffle: group by key
- Reduce phase: aggregate values

## Test Cases

### 1. Map emits key-value pairs

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mapreduce_map","msg_id":2,"data":["hello world","hello"],"mapper":"word_count"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"mapreduce_map_ok","in_reply_to":2,"msg_id":1,"mapped":[["hello",1],["world",1],["hello",1]]}}
```

## Resources

- [MapReduce Paper](https://research.google/pubs/pub62/): Google MapReduce paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
