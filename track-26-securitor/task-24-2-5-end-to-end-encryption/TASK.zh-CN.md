# 实现 End-to-End Encryption (E2EE)

英文标题：Implement End-to-End Encryption (E2EE)
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-5-end-to-end-encryption>

课程：26. 安全器：认证、授权与加密
任务序号：10
短标题：E2EE
难度：advanced
子主题：Encryption at Rest和in Transit

## 中文导读

本题要求你完成 `实现 End-to-End Encryption (E2EE)`。

重点关注：`E2EE`、`X3DH key agreement`、`double ratchet`、`perfect forward secrecy`、`session keys`。

建议先按提示逐步实现：X3DH: Alice uses Bob public keys to derive a shared root key without the 服务端 learning it。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

End-to-end encryption ensures only the communicating parties can read 消息 — not the 服务端, not the 网络. The X3DH protocol establishes a shared secret without either party transmitting it. The double ratchet algorithm then derives a fresh key用于every single 消息, providing perfect forward secrecy.

Implement a 节点 that handles E2EE session establishment和messaging:

```JSON
// Alice uses Bob's published public keys to establish a session
{ "type": "initiate_conversation", "msg_id": 1,
  "recipient": "bob",
  "bob_public_key": {"identity_key": "IK", "signed_pre_key": "SPK"} }
-> { "type": "conversation_initiated", "in_reply_to": 1,
    "session_id": "<uuid>",
    "root_key": "<derived shared secret>" }

// Encrypt a 消息使用the double ratchet
{ "type": "send_message", "msg_id": 2,
  "recipient": "bob", "plaintext": "Secret 消息" }
-> { "type": "message_encrypted", "in_reply_to": 2,
    "encrypted_message": {"ciphertext": "<base64>", "auth_tag": "<hex>"} }

// Bob decrypts和verifies authenticity
{ "type": "receive_message", "msg_id": 3,
  "sender": "alice",
  "encrypted_message": {"ciphertext": "CIPHERTEXT", "auth_tag": "AUTHTAG"} }
-> { "type": "message_decrypted", "in_reply_to": 3,
    "plaintext": "Secret 消息" }
```

## 涉及概念

- `E2EE`
- `X3DH key agreement`
- `double ratchet`
- `perfect forward secrecy`
- `session keys`

## 实现提示

- X3DH: Alice uses Bob public keys to derive a shared root key without the 服务端 learning it
- session_id is derived from the X3DH exchange和is unique per conversation
- Double ratchet: each 消息 uses a fresh key derived from the previous one
- Perfect forward secrecy: past session keys are deleted after use; compromising today's key reveals nothing about past 消息
- E2EE ensures the 服务端 never sees plaintext — only Alice和Bob can decrypt

## 测试用例

### 1. Initiate E2EE conversation

X3DH key agreement should establish a session，包含a shared root key.

输入：

```json
{"src":"alice","dest":"e2ee","body":{"type":"initiate_conversation","msg_id":1,"recipient":"bob","bob_public_key":{"identity_key":"IK","signed_pre_key":"SPK"}}}
```

期望输出：

```text
{"type": "conversation_initiated", "in_reply_to": 1, "session_id": ".*", "root_key": ".*"}
```

### 2. Encrypt 消息，包含E2EE

Should encrypt 消息使用double ratchet derived key.

输入：

```json
{"src":"alice","dest":"e2ee","body":{"type":"send_message","msg_id":1,"recipient":"bob","plaintext":"Secret message"}}
```

期望输出：

```text
{"type": "message_encrypted", "in_reply_to": 1, "encrypted_message": {"ciphertext": ".*", "auth_tag": ".*"}}
```

## 参考资料

- [Signal Protocol](https://signal.org/docs/)：X3DH和double ratchet: the basis of Signal, WhatsApp,和iMessage E2EE
- [Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/)：Double Ratchet Algorithm specification

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
