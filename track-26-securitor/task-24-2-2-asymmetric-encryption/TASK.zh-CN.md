# 实现非对称加密

英文标题：Implement Asymmetric Encryption (RSA)
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-2-asymmetric-encryption>

课程：26. 安全器
任务序号：7
短标题：非对称加密
难度：高级
子主题：静态和传输中的加密

## 中文导读

这道题要求你实现基于 RSA 的非对称加密操作，包括密钥对生成、加密、解密和数字签名验证。非对称加密的核心特点是使用一对数学关联的密钥：公钥加密、私钥解密，从而解决了密钥分发难题。数字签名则让接收方能验证数据确实来自声称的发送者。

## 题目说明

非对称加密（Asymmetric Encryption）使用一对数学上关联的密钥：用公钥加密的数据只能用私钥解密。这解决了对称加密面临的一个根本问题——如何安全地把密钥传给对方。有了非对称加密，你可以自由公开自己的公钥，任何人都可以用它来加密发给你的信息，但只有你手中的私钥能解开。

可以把非对称加密想象成一个特殊的邮箱：任何人都可以把信投进去（用公钥加密），但只有邮箱主人有钥匙打开它（用私钥解密）。数字签名（Digital Signature）则相反：你用私钥给文件"盖章"，任何人都可以用你的公钥验证这个章是真的，但无法伪造。在实际应用中，RSA 比对称加密慢得多，因此通常用 RSA 来加密一个对称密钥，再用对称密钥加密实际数据，这就是混合加密。

你需要实现一个节点来处理 RSA 密钥对操作：

```json
// 生成 RSA-4096 密钥对（仅返回公钥）
{ "type": "generate_key_pair", "msg_id": 1, "key_size": 4096 }
-> { "type": "key_pair_generated", "in_reply_to": 1,
    "public_key": "-----BEGIN PUBLIC KEY-----..." }

// 用公钥加密（只有私钥能解密）
{ "type": "encrypt", "msg_id": 2,
  "plaintext": "Secret message", "public_key": "PUBLIC_KEY" }
-> { "type": "encrypted", "in_reply_to": 2,
    "ciphertext": "<base64-encoded ciphertext>" }

// 用私钥解密
{ "type": "decrypt", "msg_id": 3,
  "ciphertext": "CIPHERTEXT", "private_key": "PRIVATE_KEY" }
-> { "type": "decrypted", "in_reply_to": 3,
    "plaintext": "Secret message" }

// 验证数字签名
{ "type": "verify", "msg_id": 4,
  "data": "Important document",
  "signature": "SIGNATURE", "public_key": "PUBLIC_KEY" }
-> { "type": "signature_valid", "in_reply_to": 4, "valid": true }
```

## 涉及概念

- RSA
- public key
- private key
- digital signature
- key pair generation

## 实现提示

- 公钥加密数据，只有对应的私钥能解密
- 私钥签署数据，公钥验证签名
- generate_key_pair 仅返回公钥，绝不在响应中暴露私钥
- RSA 比 AES 慢得多；实际应用中通常用 RSA 加密对称密钥（混合加密）
- 数字签名流程：`sign(hash(data), private_key)` 生成签名；`verify(hash(data), signature, public_key)` 验证签名

## 测试用例

### 1. 生成 RSA 密钥对

应当生成密钥对并仅返回公钥。

输入：

```json
{"src":"user","dest":"crypto","body":{"type":"generate_key_pair","msg_id":1,"key_size":4096}}
```

期望输出：

```text
{"type": "key_pair_generated", "in_reply_to": 1, "public_key": ".*"}
```

### 2. 用公钥加密

应当使用 RSA 公钥加密明文。

输入：

```json
{"src":"alice","dest":"crypto","body":{"type":"encrypt","msg_id":1,"plaintext":"Secret message","public_key":"PUBLIC_KEY"}}
```

期望输出：

```text
{"type": "encrypted", "in_reply_to": 1, "ciphertext": ".*"}
```

## 参考资料

- [RSA Cryptosystem](https://en.wikipedia.org/wiki/RSA_(cryptosystem))：RSA 公钥加密和数字签名介绍
- [PKCS #1: RSA Cryptography](https://tools.ietf.org/html/rfc8017)：RSA 密码学规范（RFC 8017）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
