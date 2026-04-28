#处理Client Request Routing

英文标题：Handle Client Request Routing
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-2-client-routing>

课程：7. 存储：线性一致 KV Store
任务序号：2
短标题：Client Routing
难度：intermediate
子主题：Linearizable 键值 存储

## 中文导读

本题要求你完成 `Handle Client Request Routing`。

重点关注：`leader routing`、`redirect`、`client sessions`。

建议先按提示逐步实现：Only Leader can process writes。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Route 客户端 requests to the Leader:

1. 客户端 sends 请求 to any 节点
2. If 节点 is Leader, process 请求
3. If not Leader, return redirect，包含Leader hint
4. 客户端 follows redirect

Handle the case when Leader is unknown (election in progress).

## 概念说明

### Client Routing

Only the Raft Leader can process writes. Clients must find the Leader. Options: redirect to Leader, 代理 through Leader, or use 客户端 library that tracks Leader.

### Leader Discovery

节点 learn the Leader from AppendEntries. When redirecting, include the current known Leader. Clients may need to 重试 if Leader changes during the 请求.

## 涉及概念

- `leader routing`
- `redirect`
- `client sessions`

## 实现提示

- Only Leader can process writes
- Redirect clients to Leader
- Track Leader ID

## 测试用例

### 1. Leader processes request

Leader processes read 请求 locally without redirecting

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
