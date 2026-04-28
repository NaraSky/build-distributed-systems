# Implement Cryptographic Hash Functions

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-3-hash-functions>

Track: 26. The Securitor
Task order: 8
Short title: Hash Functions
Difficulty: intermediate
Subtrack: Encryption at Rest and in Transit

## Problem

Cryptographic hash functions map any input to a fixed-size digest. SHA-256 is fast and great for integrity checks, but too fast for passwords. Bcrypt is deliberately slow with a configurable work factor, making brute-force password cracking impractical.

Implement a node that handles hashing and password operations:

```json
// SHA-256 hash for integrity verification
{ "type": "hash", "msg_id": 1,
  "data": "Hello World", "algorithm": "sha256" }
-> { "type": "hashed", "in_reply_to": 1,
    "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e" }

// Verify data integrity
{ "type": "verify_integrity", "msg_id": 2,
  "data": "Hello World",
  "expected_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e" }
-> { "type": "integrity_verified", "in_reply_to": 2, "valid": true }

// Hash a password with bcrypt (includes random salt)
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

## Concepts

- SHA-256
- bcrypt
- hash integrity
- password hashing
- salt
- work factor

## Hints

- SHA-256 always produces the same 64-character hex output for the same input
- verify_integrity: hash the data and compare to expected_hash
- Never use SHA-256 for passwords — use bcrypt, scrypt, or Argon2
- bcrypt includes a random salt and work factor automatically in the hash string
- verify_password: use bcrypt.compare() — do not hash manually and compare

## Test Cases

### 1. Calculate SHA-256 hash

SHA-256 of "Hello World" is the specific hex string shown.

Input:

```json
{"src":"client","dest":"hash","body":{"type":"hash","msg_id":1,"data":"Hello World","algorithm":"sha256"}}
```

Expected output:

```text
{"type": "hashed", "in_reply_to": 1, "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}
```

### 2. Verify data integrity

Hash of data matches expected_hash -> valid=true.

Input:

```json
{"src":"client","dest":"hash","body":{"type":"verify_integrity","msg_id":1,"data":"Hello World","expected_hash":"a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}}
```

Expected output:

```text
{"type": "integrity_verified", "in_reply_to": 1, "valid": true}
```

## Resources

- [Password Hashing](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): OWASP password storage cheat sheet: bcrypt, scrypt, Argon2
- [Password Hashing Competition](https://www.password-hashing.net/): Password Hashing Competition (Argon2)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
