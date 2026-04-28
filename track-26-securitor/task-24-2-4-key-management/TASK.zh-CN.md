# 实现 Secure Key Management

英文标题：Implement Secure Key Management
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-4-key-management>

课程：26. 安全器：认证、授权与加密
任务序号：9
短标题：Key Management
难度：advanced
子主题：Encryption at Rest和in Transit

## 中文导读

本题要求你完成 `实现 Secure Key Management`。

重点关注：`KMS`、`envelope encryption`、`key rotation`、`data key`、`master key`。

建议先按提示逐步实现：Generate a random AES data key; return both the plaintext version (use it once)和the encrypted version (store it)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Managing cryptographic keys is as important as the encryption itself. A KMS (Key Management System) generates data keys, wraps them，包含a master key (envelope encryption),和handles rotation so old data remains decryptable while new data uses fresh keys.

Implement a 节点 that acts as a simple KMS:

```JSON
// Generate a random AES-256 data key
{ "type": "generate_data_key", "msg_id": 1,
  "key_id": "data-key-1", "key_spec": "AES_256" }
-> { "type": "data_key_generated", "in_reply_to": 1,
    "key_id": "data-key-1",
    "plaintext_key": "<use once, then discard>",
    "encrypted_key": "<store this alongside the ciphertext>" }

// Envelope encryption: encrypt data，包含data key, encrypt data key，包含master key
{ "type": "envelope_encrypt", "msg_id": 2,
  "plaintext": "Secret data", "data_key": "DATA_KEY" }
-> { "type": "envelope_encrypted", "in_reply_to": 2,
    "encrypted_data_key": "<master-key-wrapped data key>",
    "ciphertext": "<base64>" }

// Rotate key to a new version (retain old用于decryption)
{ "type": "rotate_key", "msg_id": 3,
  "key_id": "data-key-1", "new_version": 2 }
-> { "type": "key_rotated", "in_reply_to": 3,
    "old_version": 1, "new_version": 2,
    "previous_key_stored": true }
```

## 涉及概念

- `KMS`
- `envelope encryption`
- `key rotation`
- `data key`
- `master key`
- `escrow`

## 实现提示

- Generate a random AES data key; return both the plaintext version (use it once)和the encrypted version (store it)
- Envelope encryption: encrypt data，包含the data key, encrypt the data key，包含the master key
- Key rotation: create a new version of the key; keep the old version so old data can still be decrypted
- previous_key_stored=true confirms the old key is retained after rotation
- Escrow backup requires multiple approvals和returns an encrypted backup_id

## 测试用例

### 1. Generate data key，包含KMS

Should return both plaintext和encrypted versions of the data key.

输入：

```json
{"src":"app","dest":"kms","body":{"type":"generate_data_key","msg_id":1,"key_id":"data-key-1","key_spec":"AES_256"}}
```

期望输出：

```text
{"type": "data_key_generated", "in_reply_to": 1, "key_id": "data-key-1", "plaintext_key": ".*", "encrypted_key": ".*"}
```

### 2. 信封 encryption

Should encrypt data，包含data key和wrap data key，包含master key.

输入：

```json
{"src":"app","dest":"crypto","body":{"type":"envelope_encrypt","msg_id":1,"plaintext":"Secret data","data_key":"DATA_KEY"}}
```

期望输出：

```text
{"type": "envelope_encrypted", "in_reply_to": 1, "encrypted_data_key": ".*", "ciphertext": "[A-Za-z0-9+/=]+"}
```

## 参考资料

- [AWS KMS Concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)：Key management concepts: data keys, master keys,和envelope encryption
- [NIST Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)：NIST Key Management Guidelines (SP 800-57)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
