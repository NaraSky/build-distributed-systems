# 实现安全密钥管理

英文标题：Implement Secure Key Management
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-4-key-management>

课程：26. 安全器
任务序号：9
短标题：密钥管理
难度：高级
子主题：静态和传输中的加密

## 中文导读

这道题要求你实现一个简单的密钥管理系统（KMS）。密钥管理和加密本身同等重要——再强的加密算法，如果密钥管理不当也形同虚设。你需要实现数据密钥生成、信封加密和密钥轮换这三个核心能力，这些是企业级数据安全架构的基石。

## 题目说明

密码学密钥的管理和加密本身同等重要。密钥管理系统（KMS）负责生成数据密钥，用主密钥对数据密钥进行包装（即信封加密），并处理密钥轮换，确保旧数据仍然可以解密，同时新数据使用新的密钥。

信封加密（Envelope Encryption）就像在信封里再套一个信封：你把秘密数据装进内信封并用数据密钥封好，然后把数据密钥装进外信封并用主密钥封好。这样即使数据密钥泄露，攻击者还需要主密钥才能拆开外信封。密钥轮换则像定期更换门锁：新装的锁用于以后进出，但旧钥匙要保留，因为仓库里还有用旧锁锁着的箱子需要打开。

你需要实现一个节点，充当简单的密钥管理系统：

```json
// 生成一个随机的 AES-256 数据密钥
{ "type": "generate_data_key", "msg_id": 1,
  "key_id": "data-key-1", "key_spec": "AES_256" }
-> { "type": "data_key_generated", "in_reply_to": 1,
    "key_id": "data-key-1",
    "plaintext_key": "<use once, then discard>",
    "encrypted_key": "<store this alongside the ciphertext>" }

// 信封加密：用数据密钥加密数据，用主密钥加密数据密钥
{ "type": "envelope_encrypt", "msg_id": 2,
  "plaintext": "Secret data", "data_key": "DATA_KEY" }
-> { "type": "envelope_encrypted", "in_reply_to": 2,
    "encrypted_data_key": "<master-key-wrapped data key>",
    "ciphertext": "<base64>" }

// 轮换密钥到新版本（保留旧版本用于解密）
{ "type": "rotate_key", "msg_id": 3,
  "key_id": "data-key-1", "new_version": 2 }
-> { "type": "key_rotated", "in_reply_to": 3,
    "old_version": 1, "new_version": 2,
    "previous_key_stored": true }
```

## 涉及概念

- KMS
- envelope encryption
- key rotation
- data key
- master key
- escrow

## 实现提示

- 生成一个随机的 AES 数据密钥；同时返回明文版本（使用一次后丢弃）和加密版本（与密文一起存储）
- 信封加密：用数据密钥加密数据，用主密钥加密数据密钥
- 密钥轮换：创建密钥的新版本；保留旧版本以便旧数据仍可解密
- `previous_key_stored=true` 表示确认旧密钥在轮换后被保留
- 密钥托管（Escrow）备份需要多人审批，并返回一个加密的 backup_id

## 测试用例

### 1. 通过密钥管理系统生成数据密钥

应当同时返回数据密钥的明文版本和加密版本。

输入：

```json
{"src":"app","dest":"kms","body":{"type":"generate_data_key","msg_id":1,"key_id":"data-key-1","key_spec":"AES_256"}}
```

期望输出：

```text
{"type": "data_key_generated", "in_reply_to": 1, "key_id": "data-key-1", "plaintext_key": ".*", "encrypted_key": ".*"}
```

### 2. 信封加密

应当用数据密钥加密数据，并用主密钥包装数据密钥。

输入：

```json
{"src":"app","dest":"crypto","body":{"type":"envelope_encrypt","msg_id":1,"plaintext":"Secret data","data_key":"DATA_KEY"}}
```

期望输出：

```text
{"type": "envelope_encrypted", "in_reply_to": 1, "encrypted_data_key": ".*", "ciphertext": "[A-Za-z0-9+/=]+"}
```

## 参考资料

- [AWS KMS Concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)：密钥管理核心概念，包括数据密钥、主密钥和信封加密
- [NIST Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)：NIST 密钥管理指南（SP 800-57）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
