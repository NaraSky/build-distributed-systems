# 实现 Symmetric Encryption

英文标题：Implement Symmetric Encryption
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-1-symmetric-encryption>

课程：26. 安全器：认证、授权与加密
任务序号：6
短标题：Symmetric Encryption
难度：advanced
子主题：Encryption at Rest和in Transit

## 中文导读

本题要求你完成 `实现 Symmetric Encryption`。

重点关注：`AES-256-GCM`、`symmetric encryption`、`IV`、`authentication tag`、`tamper detection`。

建议先按提示逐步实现：AES-256-GCM uses a 256-bit key, a random 12-byte IV,和produces a 16-byte auth tag。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Symmetric encryption uses the same key to encrypt和decrypt. AES-256-GCM is the modern standard: it is both a cipher (confidentiality)和a MAC (integrity). The auth tag proves the ciphertext has not been modified since it was encrypted.

Implement a 节点 that encrypts和decrypts data使用AES-256-GCM:

```JSON
// Encrypt plaintext -> get IV, ciphertext,和auth tag
{ "type": "encrypt", "msg_id": 1,
  "plaintext": "Secret 消息" }
-> { "type": "encrypted", "in_reply_to": 1,
    "iv": "<random 12-byte hex>",
    "encryptedData": "<ciphertext hex>",
    "authTag": "<16-byte hex>" }

// Decrypt back to plaintext
{ "type": "decrypt", "msg_id": 2,
  "iv": "abc123", "encryptedData": "xyz789", "authTag": "def456" }
-> { "type": "decrypted", "in_reply_to": 2,
    "plaintext": "Secret 消息" }

// Tampered ciphertext -> authentication 故障
{ "type": "decrypt", "msg_id": 3,
  "iv": "abc123", "encryptedData": "TAMPERED", "authTag": "def456" }
-> { "type": "decryption_failed", "in_reply_to": 3,
    "error": "Authentication failed - data has been tampered with" }
```

Encrypting the same plaintext twice must produce different ciphertexts because each encryption uses a freshly generated random IV.

## 涉及概念

- `AES-256-GCM`
- `symmetric encryption`
- `IV`
- `authentication tag`
- `tamper detection`

## 实现提示

- AES-256-GCM uses a 256-bit key, a random 12-byte IV,和produces a 16-byte auth tag
- Generate a fresh random IV用于every encryption — never reuse IVs，包含the same key
- The auth tag lets you detect if the ciphertext was tampered with
- Decryption fails，包含an authentication error if IV, ciphertext, or auth tag is wrong
- Encrypting the same plaintext twice should produce different ciphertexts (different IVs)

## 测试用例

### 1. Encrypt data，包含AES-256-GCM

Should encrypt和return IV, ciphertext,和auth tag.

输入：

```json
{"src":"client","dest":"encryption","body":{"type":"encrypt","msg_id":1,"plaintext":"Secret message"}}
```

期望输出：

```text
{"type": "encrypted", "in_reply_to": 1, "iv": ".*", "encryptedData": ".*", "authTag": ".*"}
```

### 2. Decrypt valid data

Valid IV/ciphertext/authTag should decrypt to the original plaintext.

输入：

```json
{"src":"client","dest":"encryption","body":{"type":"decrypt","msg_id":1,"iv":"abc123","encryptedData":"xyz789","authTag":"def456"}}
```

期望输出：

```text
{"type": "decrypted", "in_reply_to": 1, "plaintext": "Secret message"}
```

## 参考资料

- [AES-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode)：AES-GCM: authenticated encryption providing both confidentiality和integrity
- [NIST AES Specification](https://csrc.nist.gov/publications/detail/fips/197/final)：NIST Advanced Encryption Standard (FIPS 197)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
