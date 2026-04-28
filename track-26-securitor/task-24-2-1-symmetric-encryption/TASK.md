# Implement Symmetric Encryption

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-1-symmetric-encryption>

Track: 26. The Securitor
Task order: 6
Short title: Symmetric Encryption
Difficulty: advanced
Subtrack: Encryption at Rest and in Transit

## Problem

Symmetric encryption uses the same key to encrypt and decrypt. AES-256-GCM is the modern standard: it is both a cipher (confidentiality) and a MAC (integrity). The auth tag proves the ciphertext has not been modified since it was encrypted.

Implement a node that encrypts and decrypts data using AES-256-GCM:

```json
// Encrypt plaintext -> get IV, ciphertext, and auth tag
{ "type": "encrypt", "msg_id": 1,
  "plaintext": "Secret message" }
-> { "type": "encrypted", "in_reply_to": 1,
    "iv": "<random 12-byte hex>",
    "encryptedData": "<ciphertext hex>",
    "authTag": "<16-byte hex>" }

// Decrypt back to plaintext
{ "type": "decrypt", "msg_id": 2,
  "iv": "abc123", "encryptedData": "xyz789", "authTag": "def456" }
-> { "type": "decrypted", "in_reply_to": 2,
    "plaintext": "Secret message" }

// Tampered ciphertext -> authentication failure
{ "type": "decrypt", "msg_id": 3,
  "iv": "abc123", "encryptedData": "TAMPERED", "authTag": "def456" }
-> { "type": "decryption_failed", "in_reply_to": 3,
    "error": "Authentication failed - data has been tampered with" }
```

Encrypting the same plaintext twice must produce different ciphertexts because each encryption uses a freshly generated random IV.

## Concepts

- AES-256-GCM
- symmetric encryption
- IV
- authentication tag
- tamper detection

## Hints

- AES-256-GCM uses a 256-bit key, a random 12-byte IV, and produces a 16-byte auth tag
- Generate a fresh random IV for every encryption — never reuse IVs with the same key
- The auth tag lets you detect if the ciphertext was tampered with
- Decryption fails with an authentication error if IV, ciphertext, or auth tag is wrong
- Encrypting the same plaintext twice should produce different ciphertexts (different IVs)

## Test Cases

### 1. Encrypt data with AES-256-GCM

Should encrypt and return IV, ciphertext, and auth tag.

Input:

```json
{"src":"client","dest":"encryption","body":{"type":"encrypt","msg_id":1,"plaintext":"Secret message"}}
```

Expected output:

```text
{"type": "encrypted", "in_reply_to": 1, "iv": ".*", "encryptedData": ".*", "authTag": ".*"}
```

### 2. Decrypt valid data

Valid IV/ciphertext/authTag should decrypt to the original plaintext.

Input:

```json
{"src":"client","dest":"encryption","body":{"type":"decrypt","msg_id":1,"iv":"abc123","encryptedData":"xyz789","authTag":"def456"}}
```

Expected output:

```text
{"type": "decrypted", "in_reply_to": 1, "plaintext": "Secret message"}
```

## Resources

- [AES-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode): AES-GCM: authenticated encryption providing both confidentiality and integrity
- [NIST AES Specification](https://csrc.nist.gov/publications/detail/fips/197/final): NIST Advanced Encryption Standard (FIPS 197)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
