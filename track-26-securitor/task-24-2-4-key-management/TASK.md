# Implement Secure Key Management

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-4-key-management>

Track: 26. The Securitor
Task order: 9
Short title: Key Management
Difficulty: advanced
Subtrack: Encryption at Rest and in Transit

## Problem

Managing cryptographic keys is as important as the encryption itself. A KMS (Key Management System) generates data keys, wraps them with a master key (envelope encryption), and handles rotation so old data remains decryptable while new data uses fresh keys.

Implement a node that acts as a simple KMS:

```json
// Generate a random AES-256 data key
{ "type": "generate_data_key", "msg_id": 1,
  "key_id": "data-key-1", "key_spec": "AES_256" }
-> { "type": "data_key_generated", "in_reply_to": 1,
    "key_id": "data-key-1",
    "plaintext_key": "<use once, then discard>",
    "encrypted_key": "<store this alongside the ciphertext>" }

// Envelope encryption: encrypt data with data key, encrypt data key with master key
{ "type": "envelope_encrypt", "msg_id": 2,
  "plaintext": "Secret data", "data_key": "DATA_KEY" }
-> { "type": "envelope_encrypted", "in_reply_to": 2,
    "encrypted_data_key": "<master-key-wrapped data key>",
    "ciphertext": "<base64>" }

// Rotate key to a new version (retain old for decryption)
{ "type": "rotate_key", "msg_id": 3,
  "key_id": "data-key-1", "new_version": 2 }
-> { "type": "key_rotated", "in_reply_to": 3,
    "old_version": 1, "new_version": 2,
    "previous_key_stored": true }
```

## Concepts

- KMS
- envelope encryption
- key rotation
- data key
- master key
- escrow

## Hints

- Generate a random AES data key; return both the plaintext version (use it once) and the encrypted version (store it)
- Envelope encryption: encrypt data with the data key, encrypt the data key with the master key
- Key rotation: create a new version of the key; keep the old version so old data can still be decrypted
- previous_key_stored=true confirms the old key is retained after rotation
- Escrow backup requires multiple approvals and returns an encrypted backup_id

## Test Cases

### 1. Generate data key with KMS

Should return both plaintext and encrypted versions of the data key.

Input:

```json
{"src":"app","dest":"kms","body":{"type":"generate_data_key","msg_id":1,"key_id":"data-key-1","key_spec":"AES_256"}}
```

Expected output:

```text
{"type": "data_key_generated", "in_reply_to": 1, "key_id": "data-key-1", "plaintext_key": ".*", "encrypted_key": ".*"}
```

### 2. Envelope encryption

Should encrypt data with data key and wrap data key with master key.

Input:

```json
{"src":"app","dest":"crypto","body":{"type":"envelope_encrypt","msg_id":1,"plaintext":"Secret data","data_key":"DATA_KEY"}}
```

Expected output:

```text
{"type": "envelope_encrypted", "in_reply_to": 1, "encrypted_data_key": ".*", "ciphertext": "[A-Za-z0-9+/=]+"}
```

## Resources

- [AWS KMS Concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html): Key management concepts: data keys, master keys, and envelope encryption
- [NIST Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final): NIST Key Management Guidelines (SP 800-57)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
