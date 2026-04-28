# 实现端到端加密

英文标题：Implement End-to-End Encryption (E2EE)
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-5-end-to-end-encryption>

课程：26. 安全器
任务序号：10
短标题：端到端加密
难度：高级
子主题：静态和传输中的加密

## 中文导读

这道题要求你实现端到端加密的会话建立和消息收发。端到端加密确保只有通信双方能阅读消息内容，服务器和网络都无法窥探。你需要了解 X3DH 协议如何在双方之间建立共享密钥，以及双棘轮算法如何为每条消息派生独立的加密密钥，从而实现前向安全性。这是现代安全通信的核心技术。

## 题目说明

端到端加密（E2EE）确保只有通信双方能阅读消息——服务器看不到，网络也看不到。X3DH 协议让双方在不直接传输密钥的情况下，各自计算出同一个共享密钥。双棘轮算法（Double Ratchet）随后为每一条消息派生一个全新的密钥，提供完美前向安全性。

可以这样理解：端到端加密就像两个人在嘈杂的咖啡厅里用只有他们才懂的密语交谈——即使咖啡厅老板（服务器）在旁边偷听，也完全听不懂。X3DH 密钥协商让两人能在不碰面的情况下约定好密语规则，就像两个人各自混合颜料但最终得到相同的颜色。双棘轮算法确保每条消息都用不同的密钥加密，即使某条消息的密钥被破解，其他消息仍然安全——这就是完美前向安全性（Perfect Forward Secrecy）。

你需要实现一个节点来处理端到端加密的会话建立和消息收发：

```json
// Alice 使用 Bob 公开发布的公钥来建立会话
{ "type": "initiate_conversation", "msg_id": 1,
  "recipient": "bob",
  "bob_public_key": {"identity_key": "IK", "signed_pre_key": "SPK"} }
-> { "type": "conversation_initiated", "in_reply_to": 1,
    "session_id": "<uuid>",
    "root_key": "<derived shared secret>" }

// 使用双棘轮加密一条消息
{ "type": "send_message", "msg_id": 2,
  "recipient": "bob", "plaintext": "Secret message" }
-> { "type": "message_encrypted", "in_reply_to": 2,
    "encrypted_message": {"ciphertext": "<base64>", "auth_tag": "<hex>"} }

// Bob 解密并验证消息的真实性
{ "type": "receive_message", "msg_id": 3,
  "sender": "alice",
  "encrypted_message": {"ciphertext": "CIPHERTEXT", "auth_tag": "AUTHTAG"} }
-> { "type": "message_decrypted", "in_reply_to": 3,
    "plaintext": "Secret message" }
```

## 涉及概念

- E2EE
- X3DH key agreement
- double ratchet
- perfect forward secrecy
- session keys

## 实现提示

- X3DH：Alice 使用 Bob 的公钥派生出共享根密钥，服务器无法获知该密钥
- session_id 由 X3DH 交换过程派生，每个会话唯一
- 双棘轮：每条消息使用一个由前一个密钥派生出的全新密钥
- 完美前向安全性：使用过的会话密钥会被删除；即使今天的密钥泄露，也无法解密过去的消息
- 端到端加密确保服务器永远看不到明文，只有通信双方能解密

## 测试用例

### 1. 发起端到端加密会话

X3DH 密钥协商应当建立会话并产生共享根密钥。

输入：

```json
{"src":"alice","dest":"e2ee","body":{"type":"initiate_conversation","msg_id":1,"recipient":"bob","bob_public_key":{"identity_key":"IK","signed_pre_key":"SPK"}}}
```

期望输出：

```text
{"type": "conversation_initiated", "in_reply_to": 1, "session_id": ".*", "root_key": ".*"}
```

### 2. 使用端到端加密发送消息

应当使用双棘轮派生的密钥加密消息。

输入：

```json
{"src":"alice","dest":"e2ee","body":{"type":"send_message","msg_id":1,"recipient":"bob","plaintext":"Secret message"}}
```

期望输出：

```text
{"type": "message_encrypted", "in_reply_to": 1, "encrypted_message": {"ciphertext": ".*", "auth_tag": ".*"}}
```

## 参考资料

- [Signal Protocol](https://signal.org/docs/)：X3DH 和双棘轮协议，Signal、WhatsApp 和 iMessage 端到端加密的基础
- [Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/)：双棘轮算法规范

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
