# 处理客户端请求路由

英文标题：Handle Client Request Routing
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-2-client-routing>

课程：7. 存储：线性一致键值存储
任务序号：2
短标题：Client Routing
难度：进阶
子主题：线性一致键值存储

## 中文导读

这道题要求你实现客户端请求的路由机制：当客户端把请求发到了非领导者节点时，系统需要把请求正确地引导到领导者。这是分布式键值存储中非常实际的问题，因为客户端并不总是知道谁是当前的领导者。

## 题目说明

实现客户端请求到领导者的路由逻辑：

1. 客户端可以向集群中的任意节点发送请求
2. 如果当前节点就是领导者，直接处理请求
3. 如果当前节点不是领导者，返回重定向响应，并附带领导者的地址提示
4. 客户端根据重定向信息，重新向领导者发送请求

还需要处理领导者未知的情况（比如正在进行选举时）。

## 概念说明

### 客户端路由

在 Raft 中，只有领导者能处理写请求。因此客户端必须找到领导者。常见的做法有三种：将客户端重定向到领导者、通过当前节点代理转发请求到领导者、或者让客户端库自己记住领导者是谁。

### 领导者发现

节点通过接收 AppendEntries 消息来得知谁是领导者。当需要重定向客户端时，把当前已知的领导者信息告诉客户端。但需要注意，如果请求处理过程中领导者发生了变更，客户端可能需要重试。

## 涉及概念

- `leader routing`
- `redirect`
- `client sessions`

## 实现提示

- 只有领导者能处理写操作
- 非领导者节点需要将客户端重定向到领导者
- 需要记录当前领导者的标识

## 测试用例

### 1. 领导者直接处理请求

验证领导者收到读请求后能直接在本地处理，无需重定向。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"become_leader","msg_id":2,"term":1}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"become_leader_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":null}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
