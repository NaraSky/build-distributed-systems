# 实现对称加密

英文标题：Implement Symmetric Encryption
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-1-symmetric-encryption>

课程：26. 安全器
任务序号：6
短标题：对称加密
难度：高级
子主题：静态和传输中的加密

## 中文导读

这道题要求你实现基于 AES-256-GCM 的对称加密和解密。对称加密是保护数据机密性的基础手段，使用同一个密钥进行加密和解密。AES-256-GCM 是当今的主流标准，它同时提供保密性和完整性保护，能检测数据是否被篡改。理解对称加密是学习更高级加密方案的前提。

## 题目说明

对称加密（Symmetric Encryption）使用同一个密钥来加密和解密数据。AES-256-GCM 是现代加密标准：它既提供保密性（别人看不懂），又提供完整性（能发现篡改）。认证标签（Auth Tag）就像密文上的防拆封条——如果数据被动过手脚，解密时就会发现。

可以把对称加密想象成一个保险箱：你用一把钥匙锁上（加密），也用同一把钥匙打开（解密）。初始化向量（IV）就像每次锁保险箱时加入的一个随机数，即使存放的东西一样，外观也不同，这样攻击者就无法通过比较密文来推断内容。

你需要实现一个节点，使用 AES-256-GCM 加密和解密数据：

```json
// 加密明文 -> 得到 IV、密文和认证标签
{ "type": "encrypt", "msg_id": 1,
  "plaintext": "Secret message" }
-> { "type": "encrypted", "in_reply_to": 1,
    "iv": "<random 12-byte hex>",
    "encryptedData": "<ciphertext hex>",
    "authTag": "<16-byte hex>" }

// 解密还原为明文
{ "type": "decrypt", "msg_id": 2,
  "iv": "abc123", "encryptedData": "xyz789", "authTag": "def456" }
-> { "type": "decrypted", "in_reply_to": 2,
    "plaintext": "Secret message" }

// 密文被篡改 -> 认证失败
{ "type": "decrypt", "msg_id": 3,
  "iv": "abc123", "encryptedData": "TAMPERED", "authTag": "def456" }
-> { "type": "decryption_failed", "in_reply_to": 3,
    "error": "Authentication failed - data has been tampered with" }
```

对同一段明文加密两次，必须产生不同的密文，因为每次加密都会使用新生成的随机初始化向量。

## 涉及概念

- AES-256-GCM
- symmetric encryption
- IV
- authentication tag
- tamper detection

## 实现提示

- AES-256-GCM 使用 256 位密钥、随机 12 字节 IV，并产生 16 字节认证标签
- 每次加密都必须生成新的随机 IV，绝对不要对同一个密钥重复使用 IV
- 认证标签能帮你检测密文是否被篡改
- 如果 IV、密文或认证标签有误，解密会以认证错误失败
- 对同一段明文加密两次应产生不同的密文（因为使用了不同的 IV）

## 测试用例

### 1. 使用 AES-256-GCM 加密数据

应当加密数据并返回 IV、密文和认证标签。

输入：

```json
{"src":"client","dest":"encryption","body":{"type":"encrypt","msg_id":1,"plaintext":"Secret message"}}
```

期望输出：

```text
{"type": "encrypted", "in_reply_to": 1, "iv": ".*", "encryptedData": ".*", "authTag": ".*"}
```

### 2. 解密有效数据

有效的 IV、密文和认证标签应当解密还原为原始明文。

输入：

```json
{"src":"client","dest":"encryption","body":{"type":"decrypt","msg_id":1,"iv":"abc123","encryptedData":"xyz789","authTag":"def456"}}
```

期望输出：

```text
{"type": "decrypted", "in_reply_to": 1, "plaintext": "Secret message"}
```

## 参考资料

- [AES-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode)：AES-GCM 认证加密，同时提供保密性和完整性
- [NIST AES Specification](https://csrc.nist.gov/publications/detail/fips/197/final)：NIST 高级加密标准规范（FIPS 197）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
