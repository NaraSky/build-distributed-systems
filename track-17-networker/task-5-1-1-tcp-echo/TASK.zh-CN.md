# 用原始系统调用构建 TCP 回声服务器

网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-1-tcp-echo>

课程：17. 网络器：TCP 与协议基础
任务序号：1
短标题：TCP 回声服务器
难度：进阶
子主题：从零实现 TCP

## 中文导读

我们平时用的各种网络库，底下都是系统调用在干活。这道题让你跳过那些封装好的高层接口，直接用最底层的系统调用来搭建一个 TCP 回声服务器。所谓"回声"就是客户端发什么过来，服务器就原样发回去。

通过这道题，你将完整走一遍 TCP 连接的生命周期：创建套接字、绑定端口、监听、接受连接、读取数据、写回数据。这些是所有网络编程的基础，理解了它们，你再看任何网络框架都不会觉得是黑盒了。

## 题目说明

请使用原始系统调用（Syscall）构建一个 TCP 回声服务器。不允许使用标准库中的高层网络抽象，必须直接调用底层接口。服务器需要完成以下步骤：

1. 使用 `socket(AF_INET, SOCK_STREAM, 0)` 创建一个套接字（Socket）。`AF_INET` 表示使用 IPv4 地址，`SOCK_STREAM` 表示使用 TCP 协议。
2. 使用 `bind()` 将套接字绑定到指定端口
3. 使用 `listen()` 开始监听连接请求
4. 使用 `accept()` 接受客户端的连接
5. 使用 `read()` 从客户端读取数据
6. 使用 `write()` 将数据原样写回客户端

实现一个 Maelstrom 节点来模拟上述过程：

```json
Request:  {"type": "tcp_echo_start", "msg_id": 1, "port": 8080}
Response: {"type": "tcp_echo_start_ok", "in_reply_to": 1, "status": "listening", "port": 8080}

Request:  {"type": "tcp_echo_send", "msg_id": 2, "data": "hello world"}
Response: {"type": "tcp_echo_send_ok", "in_reply_to": 2, "echoed": "hello world", "bytes": 11}

Request:  {"type": "tcp_echo_stats", "msg_id": 3}
Response: {"type": "tcp_echo_stats_ok", "in_reply_to": 3, "total_connections": 1, "total_bytes": 11}
```

## 涉及概念

- `TCP`
- `socket`
- `bind`
- `listen`
- `accept`
- `syscalls`

## 实现提示

- 使用原始套接字系统调用：socket()、bind()、listen()、accept()、read()、write()
- 不要使用标准库提供的 ServerSocket 等高层封装
- 回声服务器的逻辑非常简单：读到什么就原封不动地写回去
- 使用 `SOCK_STREAM` 表示 TCP 协议，使用 `AF_INET` 表示 IPv4 地址族
- 回声完成后，记得正确关闭客户端连接，避免资源泄漏

## 测试用例

### 1. 启动回声服务器

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

### 2. 正确回声数据

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

- [Beej Guide to Network Programming](https://beej.us/guide/bgnet/)：经典的 Unix 套接字编程指南，从最底层的系统调用开始讲解网络编程

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
