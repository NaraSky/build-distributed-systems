# 实现 Cryptographic Hash Functions

英文标题：Implement Cryptographic Hash Functions
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-3-hash-functions>

课程：26. 安全器：认证、授权与加密
任务序号：8
短标题：Hash Functions
难度：intermediate
子主题：Encryption at Rest和in Transit

## 中文导读

本题要求你完成 `实现 Cryptographic Hash Functions`。

重点关注：`SHA-256`、`bcrypt`、`hash integrity`、`password hashing`、`salt`。

建议先按提示逐步实现：SHA-256 always produces the same 64-character hex output用于the same input。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Cryptographic hash functions map any input to a fixed-size digest. SHA-256 is fast和great用于integrity checks, but too fast用于passwords. Bcrypt is deliberately slow，包含a configurable work factor, making brute-force password cracking impractical.

Implement a 节点 that handles hashing和password operations:

```JSON
// SHA-256 hash用于integrity verification
{ "type": "hash", "msg_id": 1,
  "data": "Hello World", "algorithm": "sha256" }
-> { "type": "hashed", "in_reply_to": 1,
    "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e" }

// Verify data integrity
{ "type": "verify_integrity", "msg_id": 2,
  "data": "Hello World",
  "expected_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e" }
-> { "type": "integrity_verified", "in_reply_to": 2, "valid": true }

// Hash a password，包含bcrypt (includes random salt)
{ "type": "hash_password", "msg_id": 3,
  "password": "user_password_123", "algorithm": "bcrypt" }
-> { "type": "password_hashed", "in_reply_to": 3,
    "hash": "$2b$10$..." }

// Verify password against stored bcrypt hash
{ "type": "verify_password", "msg_id": 4,
  "password": "user_password_123",
  "hash": "$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy" }
-> { "type": "password_verified", "in_reply_to": 4, "valid": true }
```

## 涉及概念

- `SHA-256`
- `bcrypt`
- `hash integrity`
- `password hashing`
- `salt`
- `work factor`

## 实现提示

- SHA-256 always produces the same 64-character hex output用于the same input
- verify_integrity: hash the data和compare to expected_hash
- Never use SHA-256用于passwords — use bcrypt, scrypt, or Argon2
- bcrypt includes a random salt和work factor automatically in the hash string
- verify_password: use bcrypt.compare() — do not hash manually和compare

## 测试用例

### 1. Calculate SHA-256 hash

SHA-256 of "Hello World" is the specific hex string shown.

输入：

```json
{"src":"client","dest":"hash","body":{"type":"hash","msg_id":1,"data":"Hello World","algorithm":"sha256"}}
```

期望输出：

```text
{"type": "hashed", "in_reply_to": 1, "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}
```

### 2. Verify data integrity

Hash of data matches expected_hash -> valid=true.

输入：

```json
{"src":"client","dest":"hash","body":{"type":"verify_integrity","msg_id":1,"data":"Hello World","expected_hash":"a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}}
```

期望输出：

```text
{"type": "integrity_verified", "in_reply_to": 1, "valid": true}
```

## 参考资料

- [Password Hashing](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)：OWASP password 存储 cheat sheet: bcrypt, scrypt, Argon2
- [Password Hashing Competition](https://www.password-hashing.net/)：Password Hashing Competition (Argon2)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
