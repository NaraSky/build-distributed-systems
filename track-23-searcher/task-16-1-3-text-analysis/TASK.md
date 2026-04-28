# Implement a Text Analysis Pipeline

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-3-text-analysis>

Track: 23. The Searcher
Task order: 3
Short title: Text Analysis
Difficulty: intermediate
Subtrack: Document Model and Mapping

## Problem

Text analysis converts raw text into a sequence of tokens for indexing. The analysis pipeline determines how text is searched.

**Pipeline stages**:
1. **Tokenizer**: split "Distributed Systems: A Primer" into ["Distributed", "Systems", "A", "Primer"]
2. **Lowercase filter**: ["distributed", "systems", "a", "primer"]
3. **Stop word filter**: remove "a" -> ["distributed", "systems", "primer"]
4. **Stemmer (Porter algorithm)**: "distributed" -> "distribut", "systems" -> "system" -> ["distribut", "system", "primer"]

The same pipeline is applied at both index time (to build the inverted index) and query time (to normalize the search query). This ensures that a search for "Distribution" matches a document containing "Distributed".

```json
Request:  {"type": "analyze", "msg_id": 1, "text": "The Quick Brown Fox Jumps", "analyzer": "standard"}
Response: {"type": "analyze_ok", "in_reply_to": 1, "tokens": [{"token": "quick", "position": 1}, {"token": "brown", "position": 2}, {"token": "fox", "position": 3}, {"token": "jump", "position": 4}]}
```

## Concepts

- text analysis
- tokenizer
- lowercase filter
- stemmer
- stop words

## Hints

- Tokenizer: split text on whitespace and punctuation into individual tokens
- Lowercase filter: convert all tokens to lowercase for case-insensitive search
- Stop word filter: remove common words (the, a, is, and, etc.) that add noise
- Stemmer (Porter): reduce words to their root form (running -> run, distributed -> distribut)
- Chain these into a pipeline: tokenize -> lowercase -> stop words -> stem

## Test Cases

### 1. Standard analyzer tokenizes and lowercases

analyze_ok tokens should include "hello" and "world" (lowercased).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"analyze","msg_id":2,"text":"Hello World","analyzer":"standard"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Stop words are removed

Tokens should not include "the", "is", "on" (stop words).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"analyze","msg_id":2,"text":"The cat is on the mat","analyzer":"standard"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Analysis](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html): Elasticsearch documentation on text analysis and analyzers

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
