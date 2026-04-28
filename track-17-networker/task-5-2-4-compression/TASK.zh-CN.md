# 添加消息压缩并分析 CPU 与带宽的权衡

英文标题：Add Message Compression with CPU-Bandwidth Tradeoff Analysis
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-4-compression>

课程：17. 网络器：TCP 与协议基础
任务序号：9
短标题：压缩权衡分析
难度：进阶
子主题：消息分帧与序列化

## 中文导读

这道题让你在消息分帧的基础上加入压缩功能，并通过基准测试来分析"压缩到底划不划算"。压缩可以减少传输的数据量，但需要消耗额外的 CPU 资源。对于小数据包，压缩后的结果甚至可能比原始数据更大（因为压缩算法本身有固定开销）。通过在不同数据大小下进行测试，你将找到压缩的"盈亏平衡点"，学会在实际项目中做出合理的取舍。

## 题目说明

在你的消息分帧机制中加入压缩功能。通过在不同数据大小下进行基准测试，分析 CPU 开销与带宽节省之间的权衡，找出什么时候压缩有利、什么时候反而有害。

在帧头中添加一个压缩标志位，接收方检查该标志位并在需要时进行解压。

实现以下消息处理器：

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

## 涉及概念

- `compression`
- `LZ4`
- `Snappy`
- `CPU vs bandwidth`
- `tradeoff analysis`

## 实现提示

- 在序列化之后、分帧之前进行压缩
- 小数据包（不到 100 字节）压缩后往往会变大，因为压缩算法本身有头部开销
- 在帧头中使用压缩标志位：0x00 表示未压缩，0x01 表示已压缩
- 在不同的数据大小下进行基准测试，找出压缩开始"划算"的临界点
- 对于小消息来说，压缩的 CPU 开销可能超过节省的带宽

## 测试用例

### 1. 压缩重复数据

验证说明：对于高度重复的数据，compress_ok 应显示 compressed_size 小于 original_size，且 ratio 小于 1.0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compress","msg_id":2,"data":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","algorithm":"lz4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 压缩与解压往返验证

验证说明：decompress_ok 应返回与原始数据完全一致的内容。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compress","msg_id":2,"data":"test data for roundtrip","algorithm":"lz4"}}
{"src":"c1","dest":"n1","body":{"type":"decompress","msg_id":3,"algorithm":"lz4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [LZ4 Compression Algorithm](https://lz4.github.io/lz4/)：LZ4 极速压缩算法，以速度为优化目标

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
