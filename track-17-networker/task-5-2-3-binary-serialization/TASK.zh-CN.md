# 实现二进制序列化格式

英文标题：Implement a Binary Serialization Format
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-3-binary-serialization>

课程：17. 网络器：TCP 与协议基础
任务序号：8
短标题：二进制序列化
难度：高级
子主题：消息分帧与序列化

## 中文导读

这道题让你动手实现一个类似 MessagePack 的二进制序列化格式。日常开发中我们习惯用 JSON 来传输数据，但 JSON 是文本格式，体积大、解析慢。二进制序列化把数据"压缩"成紧凑的字节序列，省去了字段名、引号等冗余字符，传输效率大大提高。通过亲手实现编码和解码，你将深刻理解二进制协议的设计思路，以及它相比 JSON 在体积和性能上的优势。

## 题目说明

实现一个二进制序列化格式（类似 MessagePack）。支持四种类型：整数、字符串、数组和映射表。并将其与 JSON 在体积和性能上进行对比。

类型标签：
- `0x01`：整数（4 字节大端序）
- `0x02`：字符串（2 字节长度 + UTF-8 字节）
- `0x03`：数组（2 字节元素数量 + N 个编码后的值）
- `0x04`：映射表（2 字节键值对数量 + N 个键值对）

实现以下消息处理器：

```json
Request:  {"type": "bin_encode", "msg_id": 1, "value": {"name": "Alice", "age": 30}}
Response: {"type": "bin_encode_ok", "in_reply_to": 1, "encoded_hex": "...", "size_bytes": 20, "json_size_bytes": 27, "savings_pct": 25.9}

Request:  {"type": "bin_decode", "msg_id": 2, "encoded_hex": "..."}
Response: {"type": "bin_decode_ok", "in_reply_to": 2, "value": {"name": "Alice", "age": 30}}

Request:  {"type": "bin_benchmark", "msg_id": 3, "payload_sizes": [100, 1000, 10000]}
Response: {"type": "bin_benchmark_ok", "in_reply_to": 3, "results": [
    {"size": 100, "json_bytes": 100, "binary_bytes": 72, "ratio": 0.72}
]}
```

## 涉及概念

- `binary serialization`
- `MessagePack`
- `type tags`
- `compact encoding`

## 实现提示

- 在每个值前面放一个类型标签字节：0x01 表示整数，0x02 表示字符串，0x03 表示数组，0x04 表示映射表
- 整数使用固定的 4 字节大端序编码
- 字符串前面加 2 字节的长度，后跟 UTF-8 编码的字节
- 数组前面加 2 字节的元素数量，后跟相应数量的编码后的值
- 将二进制编码后的大小与同一数据的 JSON 大小进行对比

## 测试用例

### 1. 编码一个简单整数

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bin_encode","msg_id":2,"value":42}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bin_encode_ok", "in_reply_to": 2, "encoded_hex": "010000002a", "size_bytes": 5, "msg_id": 1}}
```

### 2. 编码与解码往返验证

验证说明：编码字符串 "hello" 应生成对应的十六进制表示；对该十六进制解码后应还原为 "hello"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bin_encode","msg_id":2,"value":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"bin_decode","msg_id":3,"encoded_hex":"02000568656c6c6f"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [MessagePack Specification](https://msgpack.org/)：MessagePack 高效二进制序列化格式的规范文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
