# Add Message Compression with CPU-Bandwidth Tradeoff Analysis

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-4-compression>

Track: 17. The Networker
Task order: 9
Short title: Compression Tradeoff
Difficulty: intermediate
Subtrack: Message Framing and Serialization

## Problem

Add compression to your message framing. Benchmark the CPU vs bandwidth tradeoff at different payload sizes to determine when compression helps versus hurts.

Add a compression flag to the frame header. The receiver checks the flag and decompresses if needed.

Implement handlers:

```json
Request:  {"type": "compress", "msg_id": 1, "data": "hello hello hello hello", "algorithm": "lz4"}
Response: {"type": "compress_ok", "in_reply_to": 1, "original_size": 23, "compressed_size": 14, "ratio": 0.61}

Request:  {"type": "compress_benchmark", "msg_id": 2, "payload_sizes_bytes": [64, 1024, 10240, 102400]}
Response: {"type": "compress_benchmark_ok", "in_reply_to": 2, "results": [
    {"size": 64, "compressed_size": 72, "ratio": 1.13, "verdict": "skip_compression"},
    {"size": 1024, "compressed_size": 420, "ratio": 0.41, "verdict": "compress"},
    {"size": 10240, "compressed_size": 2100, "ratio": 0.21, "verdict": "compress"},
    {"size": 102400, "compressed_size": 15000, "ratio": 0.15, "verdict": "compress"}
]}
```

## Concepts

- compression
- LZ4
- Snappy
- CPU vs bandwidth
- tradeoff analysis

## Hints

- Compress the payload after serialization, before framing
- Small payloads (< 100 bytes) often get larger after compression due to header overhead
- Use a compression flag in the frame header: 0x00=raw, 0x01=compressed
- Benchmark at different payload sizes to find the crossover point
- CPU cost of compression may exceed the bandwidth savings for small messages

## Test Cases

### 1. Compress repetitive data

compress_ok should show compressed_size < original_size and ratio < 1.0 for highly repetitive data.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compress","msg_id":2,"data":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","algorithm":"lz4"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compress and decompress roundtrip

decompress_ok should return the original data unchanged.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compress","msg_id":2,"data":"test data for roundtrip","algorithm":"lz4"}}
{"src":"c1","dest":"n1","body":{"type":"decompress","msg_id":3,"algorithm":"lz4"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [LZ4 Compression Algorithm](https://lz4.github.io/lz4/): LZ4: extremely fast compression algorithm optimized for speed

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
