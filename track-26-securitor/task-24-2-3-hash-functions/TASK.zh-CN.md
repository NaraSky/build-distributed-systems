# 实现密码学哈希函数

英文标题：Implement Cryptographic Hash Functions
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-3-hash-functions>

课程：26. 安全器
任务序号：8
短标题：哈希函数
难度：进阶
子主题：静态和传输中的加密

## 中文导读

这道题要求你实现密码学哈希函数的两个典型应用：数据完整性校验和密码安全存储。SHA-256 速度快，适合验证数据有没有被篡改；但正因为太快，不适合存储密码。Bcrypt 故意设计得很慢，让暴力破解密码变得不切实际。理解何时使用哪种哈希函数，是安全开发的基本功。

## 题目说明

密码学哈希函数将任意长度的输入映射为固定长度的摘要，而且这个过程不可逆——你无法从摘要还原出原始数据。SHA-256 速度快，非常适合做数据完整性校验，但正因为太快，不适合用来存储密码（攻击者可以极速尝试大量密码）。Bcrypt 故意设计得很慢，并且工作因子（Work Factor）可配置，这使得暴力破解密码变得不切实际。

可以把哈希函数想象成一台绞肉机：你把任意大小的数据放进去，出来的永远是固定大小的摘要，而且这个过程不可逆。SHA-256 就像一台高速绞肉机，适合快速验证"数据有没有被换过"。但存储密码时需要一台故意转得很慢的绞肉机——Bcrypt。它的工作因子让每次哈希运算都耗费可观的时间，即使攻击者拿到了哈希值，逐个尝试密码也极其缓慢。盐值（Salt）是每次哈希时混入的随机数据，确保相同的密码也会产生不同的哈希值，防止攻击者用预计算表破解。

你需要实现一个节点来处理哈希运算和密码操作：

```json
// SHA-256 哈希用于完整性校验
{ "type": "hash", "msg_id": 1,
  "data": "Hello World", "algorithm": "sha256" }
-> { "type": "hashed", "in_reply_to": 1,
    "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e" }

// 验证数据完整性
{ "type": "verify_integrity", "msg_id": 2,
  "data": "Hello World",
  "expected_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e" }
-> { "type": "integrity_verified", "in_reply_to": 2, "valid": true }

// 使用 bcrypt 哈希密码（自动包含随机盐值）
{ "type": "hash_password", "msg_id": 3,
  "password": "user_password_123", "algorithm": "bcrypt" }
-> { "type": "password_hashed", "in_reply_to": 3,
    "hash": "$2b$10$..." }

// 验证密码是否与存储的 bcrypt 哈希匹配
{ "type": "verify_password", "msg_id": 4,
  "password": "user_password_123",
  "hash": "$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy" }
-> { "type": "password_verified", "in_reply_to": 4, "valid": true }
```

## 涉及概念

- SHA-256
- bcrypt
- hash integrity
- password hashing
- salt
- work factor

## 实现提示

- SHA-256 对相同的输入始终产生相同的 64 字符十六进制输出
- verify_integrity：对数据计算哈希，然后与 expected_hash 进行比较
- 绝不使用 SHA-256 来存储密码，应当使用 bcrypt、scrypt 或 Argon2
- bcrypt 会自动在哈希字符串中包含随机盐值和工作因子
- verify_password：使用 `bcrypt.compare()` 进行验证，不要手动计算哈希后比较

## 测试用例

### 1. 计算 SHA-256 哈希

"Hello World" 的 SHA-256 哈希值应当是下面显示的特定十六进制字符串。

输入：

```json
{"src":"client","dest":"hash","body":{"type":"hash","msg_id":1,"data":"Hello World","algorithm":"sha256"}}
```

期望输出：

```text
{"type": "hashed", "in_reply_to": 1, "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}
```

### 2. 验证数据完整性

数据的哈希与期望值匹配，应当返回 valid=true。

输入：

```json
{"src":"client","dest":"hash","body":{"type":"verify_integrity","msg_id":1,"data":"Hello World","expected_hash":"a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}}
```

期望输出：

```text
{"type": "integrity_verified", "in_reply_to": 1, "valid": true}
```

## 参考资料

- [Password Hashing](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)：OWASP 密码存储速查表，涵盖 bcrypt、scrypt、Argon2
- [Password Hashing Competition](https://www.password-hashing.net/)：密码哈希竞赛（Argon2）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
