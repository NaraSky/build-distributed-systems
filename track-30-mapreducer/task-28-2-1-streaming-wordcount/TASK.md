# Implement Streaming Word Count

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-1-streaming-wordcount>

Track: 30. The MapReducer
Task order: 6
Short title: Streaming Word Count
Difficulty: intermediate
Subtrack: Stream Processing

## Problem

Batch MapReduce waits for all data before producing output. Stream processing handles an **infinite flow** of events: state is updated as each event arrives, and results can be queried at any time.

Your node maintains a running word count across all received messages:

```json
// Process a batch of words — update running counts
{ "type": "process", "msg_id": 1, "words": ["hello", "world", "hello"] }
→ { "type": "processed", "in_reply_to": 1, "counts": {"hello": 2, "world": 1} }

// Return the top N words by count
{ "type": "topn", "msg_id": 2, "n": 2,
  "counts": {"hello": 5, "world": 3, "stream": 1} }
→ { "type": "topn", "in_reply_to": 2,
    "top_words": [["hello", 5], ["world", 3]] }

// Increment a single word and return its new count
{ "type": "update", "msg_id": 3, "word": "hello", "current_count": 5 }
→ { "type": "updated", "in_reply_to": 3, "word": "hello", "new_count": 6 }

// Emit top N from current in-memory state (periodic output)
{ "type": "output", "msg_id": 4, "interval_ms": 1000, "counts": {"hello": 10} }
→ { "type": "periodic_output", "in_reply_to": 4,
    "top_words": [["hello", 10]] }
```

Unlike batch processing, the node never resets counts between messages — every `process` call adds to the global running totals.

## Concepts

- stream processing
- stateful processing
- running aggregates
- top-N
- incremental updates

## Hints

- Keep a running word count dict in memory, update on every process message
- topn: sort the dict by count descending, return the first N entries
- update increments a single word by 1 and returns the new count
- output emits the top N words from current state without resetting it
- Lowercase and strip words before counting

## Test Cases

### 1. Process word stream

Should update running word counts and return current totals.

Input:

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"words":["hello","world","hello"]}}
```

Expected output:

```text
{"type": "processed", "in_reply_to": 1, "counts": {"hello": 2, "world": 1}}
```

### 2. Output top N words

Should return top N words sorted by count descending.

Input:

```json
{"src":"stream","dest":"processor","body":{"type":"topn","msg_id":1,"n":2,"counts":{"hello":5,"world":3,"stream":1}}}
```

Expected output:

```text
{"type": "topn", "in_reply_to": 1, "top_words": [["hello", 5], ["world", 3]]}
```

## Resources

- [Streaming 101 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101): Streaming 101 by Tyler Akidau

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
