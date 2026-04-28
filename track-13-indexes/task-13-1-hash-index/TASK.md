# Implement Hash Index

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-1-hash-index>

Track: 13. Indexes
Task order: 1
Short title: Hash Index
Difficulty: intermediate

## Problem

Build a hash index that maps keys to data file offsets:

1. Hash each key to a bucket
2. Store key and file offset in the bucket
3. Lookup returns the offset for a key
4. Handle collisions with chaining or probing

Hash indexes provide O(1) point lookups but cannot support range queries.

## Concept Notes

### Why Indexing?

Without indexes, finding a record requires scanning all data - O(n) cost. Indexes provide shortcuts from keys to locations, reducing lookup to O(1) for hash or O(log n) for tree indexes.

### Hash Index

Hash indexes map key -> file offset. They are extremely fast for exact matches. Bitcask, a log-structured store, uses hash indexes. The tradeoff: index must fit in memory, and no range queries.

## Concepts

- indexing
- hash table
- O(1) lookup

## Hints

- Map keys to data locations
- Handle hash collisions
- Support insert, lookup, delete

## Test Cases

### 1. Insert and lookup

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"index_put","msg_id":2,"key":"foo","value":100}}
{"src":"c2","dest":"n1","body":{"type":"index_get","msg_id":3,"key":"foo"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"index_put_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"index_get_ok","in_reply_to":3,"msg_id":2,"value":100}}
```

## Resources

- [DDIA Chapter 3](https://dataintensive.net/): Storage and Retrieval chapter on log-structured storage

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
