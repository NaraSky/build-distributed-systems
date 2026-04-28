# 构建 a TCP 回声 Server from Raw Syscalls

英文标题：Build a TCP Echo Server from Raw Syscalls
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-1-tcp-echo>

课程：17. 网络器：TCP 与协议基础
任务序号：1
短标题：TCP 回声 Server
难度：intermediate
子主题：TCP From Scratch

## 中文导读

本题要求你完成 `构建 a TCP 回声 Server from Raw Syscalls`。

重点关注：`TCP`、`socket`、`bind`、`listen`、`accept`。

建议先按提示逐步实现：Use raw socket syscalls: socket(), bind(), listen(), accept(), read(), write()。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a TCP echo 服务端使用raw syscalls. No standard library 网络 abstractions allowed. The 服务端 should:

1. Create a socket使用`socket(AF_INET, SOCK_STREAM, 0)`
2. Bind to a port使用`bind()`
3. Listen用于connections使用`listen()`
4. Accept connections使用`accept()`
5. Read data使用`read()`
6. Write data back使用`write()`

Implement a Maelstrom 节点 that simulates this:

```JSON
请求:  {"type": "tcp_echo_start", "msg_id": 1, "port": 8080}
响应: {"type": "tcp_echo_start_ok", "in_reply_to": 1, "status": "listening", "port": 8080}

请求:  {"type": "tcp_echo_send", "msg_id": 2, "data": "hello world"}
响应: {"type": "tcp_echo_send_ok", "in_reply_to": 2, "echoed": "hello world", "bytes": 11}

请求:  {"type": "tcp_echo_stats", "msg_id": 3}
响应: {"type": "tcp_echo_stats_ok", "in_reply_to": 3, "total_connections": 1, "total_bytes": 11}
```

## 涉及概念

- `TCP`
- `socket`
- `bind`
- `listen`
- `accept`
- `syscalls`

## 实现提示

- Use raw socket syscalls: socket(), bind(), listen(), accept(), read(), write()
- Do not use high-level 网络 abstractions from the standard library
- The echo 服务端 reads data from a 客户端和writes it back unchanged
- Use SOCK_STREAM用于TCP和AF_INET用于IPv4
- Close 客户端 connections properly after echoing

## 测试用例

### 1. Start 回声 server

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_echo_start","msg_id":2,"port":8080}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_echo_start_ok", "in_reply_to": 2, "status": "listening", "port": 8080, "msg_id": 1}}
```

### 2. 回声 data back correctly

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_echo_start","msg_id":2,"port":8080}}
{"src":"c1","dest":"n1","body":{"type":"tcp_echo_send","msg_id":3,"data":"hello world"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_echo_start_ok", "in_reply_to": 2, "status": "listening", "port": 8080, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_echo_send_ok", "in_reply_to": 3, "echoed": "hello world", "bytes": 11, "msg_id": 2}}
```

## 参考资料

- [Beej Guide to Network Programming](https://beej.us/guide/bgnet/)：Classic guide to Unix socket programming from raw syscalls

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
