# 实现 Asymmetric Encryption (RSA)

英文标题：Implement Asymmetric Encryption (RSA)
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-2-asymmetric-encryption>

课程：26. 安全器：认证、授权与加密
任务序号：7
短标题：Asymmetric Encryption
难度：advanced
子主题：Encryption at Rest和in Transit

## 中文导读

本题要求你完成 `实现 Asymmetric Encryption (RSA)`。

重点关注：`RSA`、`public key`、`private key`、`digital signature`、`key pair generation`。

建议先按提示逐步实现：Public key encrypts data that only the private key can decrypt。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Asymmetric encryption uses a mathematically linked key pair: anything encrypted，包含the public key can only be decrypted，包含the private key. This solves the key distribution problem — you can share the public key freely. The private key also enables digital signatures to prove authenticity.

Implement a 节点 that handles RSA key pair operations:

```JSON
// Generate an RSA-4096 key pair (return only the public key)
{ "type": "generate_key_pair", "msg_id": 1, "key_size": 4096 }
-> { "type": "key_pair_generated", "in_reply_to": 1,
    "public_key": "-----BEGIN PUBLIC KEY-----..." }

// Encrypt，包含public key (only private key can decrypt)
{ "type": "encrypt", "msg_id": 2,
  "plaintext": "Secret 消息", "public_key": "PUBLIC_KEY" }
-> { "type": "encrypted", "in_reply_to": 2,
    "ciphertext": "<base64-encoded ciphertext>" }

// Decrypt，包含private key
{ "type": "decrypt", "msg_id": 3,
  "ciphertext": "CIPHERTEXT", "private_key": "PRIVATE_KEY" }
-> { "type": "decrypted", "in_reply_to": 3,
    "plaintext": "Secret 消息" }

// Verify a digital signature
{ "type": "verify", "msg_id": 4,
  "data": "Important document",
  "signature": "SIGNATURE", "public_key": "PUBLIC_KEY" }
-> { "type": "signature_valid", "in_reply_to": 4, "valid": true }
```

## 涉及概念

- `RSA`
- `public key`
- `private key`
- `digital signature`
- `key pair generation`

## 实现提示

- Public key encrypts data that only the private key can decrypt
- Private key signs data; public key verifies the signature
- generate_key_pair returns only the public key — never expose the private key in a 响应
- RSA is much slower than AES; in practice use RSA to encrypt a symmetric key (hybrid encryption)
- Digital signature: sign(hash(data), private_key) -> signature; verify(hash(data), signature, public_key)

## 测试用例

### 1. Generate RSA key pair

Should generate key pair和return only the public key.

输入：

```json
{"src":"user","dest":"crypto","body":{"type":"generate_key_pair","msg_id":1,"key_size":4096}}
```

期望输出：

```text
{"type": "key_pair_generated", "in_reply_to": 1, "public_key": ".*"}
```

### 2. Encrypt，包含public key

Should encrypt plaintext，包含RSA public key.

输入：

```json
{"src":"alice","dest":"crypto","body":{"type":"encrypt","msg_id":1,"plaintext":"Secret message","public_key":"PUBLIC_KEY"}}
```

期望输出：

```text
{"type": "encrypted", "in_reply_to": 1, "ciphertext": ".*"}
```

## 参考资料

- [RSA Cryptosystem](https://en.wikipedia.org/wiki/RSA_(cryptosystem))：RSA: public-key encryption和digital signatures
- [PKCS #1: RSA Cryptography](https://tools.ietf.org/html/rfc8017)：RSA Cryptography Specifications (RFC 8017)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
