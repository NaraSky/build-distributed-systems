# 添加 消息 Compression，包含CPU-Bandwidth Tradeoff Analysis

英文标题：Add Message Compression，包含CPU-Bandwidth Tradeoff Analysis
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-4-compression>

课程：17. 网络器：TCP 与协议基础
任务序号：9
短标题：Compression Tradeoff
难度：intermediate
子主题：消息 Framing和Serialization

## 中文导读

本题要求你完成 `添加 消息 Compression，包含CPU-Bandwidth Tradeoff Analysis`。

重点关注：`compression`、`LZ4`、`Snappy`、`CPU vs bandwidth`、`tradeoff analysis`。

建议先按提示逐步实现：Compress the payload after serialization, before framing。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Add compression to your 消息 framing. Benchmark the CPU vs bandwidth tradeoff at different payload sizes to determine when compression helps versus hurts.

Add a compression flag to the frame header. The receiver checks the flag和decompresses if needed.

Implement handlers:

```JSON
请求:  {"type": "compress", "msg_id": 1, "data": "hello hello hello hello", "algorithm": "lz4"}
响应: {"type": "compress_ok", "in_reply_to": 1, "original_size": 23, "compressed_size": 14, "ratio": 0.61}

请求:  {"type": "compress_benchmark", "msg_id": 2, "payload_sizes_bytes": [64, 1024, 10240, 102400]}
响应: {"type": "compress_benchmark_ok", "in_reply_to": 2, "results": [
    {"size": 64, "compressed_size": 72, "ratio": 1.13, "verdict": "skip_compression"},
    {"size": 1024, "compressed_size": 420, "ratio": 0.41, "verdict": "compress"},
    {"size": 10240, "compressed_size": 2100, "ratio": 0.21, "verdict": "compress"},
    {"size": 102400, "compressed_size": 15000, "ratio": 0.15, "verdict": "compress"}
]}
```

## 涉及概念

- `compression`
- `LZ4`
- `Snappy`
- `CPU vs bandwidth`
- `tradeoff analysis`

## 实现提示

- Compress the payload after serialization, before framing
- Small payloads (< 100 bytes) often get larger after compression due to header overhead
- Use a compression flag in the frame header: 0x00=raw, 0x01=compressed
- Benchmark at different payload sizes to find the crossover point
- CPU cost of compression may exceed the bandwidth savings用于small 消息

## 测试用例

### 1. Compress repetitive data

compress_ok should show compressed_size < original_size和ratio < 1.0用于highly repetitive data.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compress","msg_id":2,"data":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","algorithm":"lz4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compress和decompress roundtrip

decompress_ok should return the original data unchanged.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compress","msg_id":2,"data":"test data用于roundtrip","algorithm":"lz4"}}
{"src":"c1","dest":"n1","body":{"type":"decompress","msg_id":3,"algorithm":"lz4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [LZ4 Compression Algorithm](https://lz4.github.io/lz4/)：LZ4: extremely fast compression algorithm optimized用于speed

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
