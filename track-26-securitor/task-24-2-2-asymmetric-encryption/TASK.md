# Implement Asymmetric Encryption (RSA)

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-2-asymmetric-encryption>

Track: 26. The Securitor
Task order: 7
Short title: Asymmetric Encryption
Difficulty: advanced
Subtrack: Encryption at Rest and in Transit

## Problem

Asymmetric encryption uses a mathematically linked key pair: anything encrypted with the public key can only be decrypted with the private key. This solves the key distribution problem — you can share the public key freely. The private key also enables digital signatures to prove authenticity.

Implement a node that handles RSA key pair operations:

```json
// Generate an RSA-4096 key pair (return only the public key)
{ "type": "generate_key_pair", "msg_id": 1, "key_size": 4096 }
-> { "type": "key_pair_generated", "in_reply_to": 1,
    "public_key": "-----BEGIN PUBLIC KEY-----..." }

// Encrypt with public key (only private key can decrypt)
{ "type": "encrypt", "msg_id": 2,
  "plaintext": "Secret message", "public_key": "PUBLIC_KEY" }
-> { "type": "encrypted", "in_reply_to": 2,
    "ciphertext": "<base64-encoded ciphertext>" }

// Decrypt with private key
{ "type": "decrypt", "msg_id": 3,
  "ciphertext": "CIPHERTEXT", "private_key": "PRIVATE_KEY" }
-> { "type": "decrypted", "in_reply_to": 3,
    "plaintext": "Secret message" }

// Verify a digital signature
{ "type": "verify", "msg_id": 4,
  "data": "Important document",
  "signature": "SIGNATURE", "public_key": "PUBLIC_KEY" }
-> { "type": "signature_valid", "in_reply_to": 4, "valid": true }
```

## Concepts

- RSA
- public key
- private key
- digital signature
- key pair generation

## Hints

- Public key encrypts data that only the private key can decrypt
- Private key signs data; public key verifies the signature
- generate_key_pair returns only the public key — never expose the private key in a response
- RSA is much slower than AES; in practice use RSA to encrypt a symmetric key (hybrid encryption)
- Digital signature: sign(hash(data), private_key) -> signature; verify(hash(data), signature, public_key)

## Test Cases

### 1. Generate RSA key pair

Should generate key pair and return only the public key.

Input:

```json
{"src":"user","dest":"crypto","body":{"type":"generate_key_pair","msg_id":1,"key_size":4096}}
```

Expected output:

```text
{"type": "key_pair_generated", "in_reply_to": 1, "public_key": ".*"}
```

### 2. Encrypt with public key

Should encrypt plaintext with RSA public key.

Input:

```json
{"src":"alice","dest":"crypto","body":{"type":"encrypt","msg_id":1,"plaintext":"Secret message","public_key":"PUBLIC_KEY"}}
```

Expected output:

```text
{"type": "encrypted", "in_reply_to": 1, "ciphertext": ".*"}
```

## Resources

- [RSA Cryptosystem](https://en.wikipedia.org/wiki/RSA_(cryptosystem)): RSA: public-key encryption and digital signatures
- [PKCS #1: RSA Cryptography](https://tools.ietf.org/html/rfc8017): RSA Cryptography Specifications (RFC 8017)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
