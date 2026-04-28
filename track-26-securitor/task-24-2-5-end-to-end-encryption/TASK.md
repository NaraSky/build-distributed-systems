# Implement End-to-End Encryption (E2EE)

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-5-end-to-end-encryption>

Track: 26. The Securitor
Task order: 10
Short title: E2EE
Difficulty: advanced
Subtrack: Encryption at Rest and in Transit

## Problem

End-to-end encryption ensures only the communicating parties can read messages — not the server, not the network. The X3DH protocol establishes a shared secret without either party transmitting it. The double ratchet algorithm then derives a fresh key for every single message, providing perfect forward secrecy.

Implement a node that handles E2EE session establishment and messaging:

```json
// Alice uses Bob's published public keys to establish a session
{ "type": "initiate_conversation", "msg_id": 1,
  "recipient": "bob",
  "bob_public_key": {"identity_key": "IK", "signed_pre_key": "SPK"} }
-> { "type": "conversation_initiated", "in_reply_to": 1,
    "session_id": "<uuid>",
    "root_key": "<derived shared secret>" }

// Encrypt a message using the double ratchet
{ "type": "send_message", "msg_id": 2,
  "recipient": "bob", "plaintext": "Secret message" }
-> { "type": "message_encrypted", "in_reply_to": 2,
    "encrypted_message": {"ciphertext": "<base64>", "auth_tag": "<hex>"} }

// Bob decrypts and verifies authenticity
{ "type": "receive_message", "msg_id": 3,
  "sender": "alice",
  "encrypted_message": {"ciphertext": "CIPHERTEXT", "auth_tag": "AUTHTAG"} }
-> { "type": "message_decrypted", "in_reply_to": 3,
    "plaintext": "Secret message" }
```

## Concepts

- E2EE
- X3DH key agreement
- double ratchet
- perfect forward secrecy
- session keys

## Hints

- X3DH: Alice uses Bob public keys to derive a shared root key without the server learning it
- session_id is derived from the X3DH exchange and is unique per conversation
- Double ratchet: each message uses a fresh key derived from the previous one
- Perfect forward secrecy: past session keys are deleted after use; compromising today's key reveals nothing about past messages
- E2EE ensures the server never sees plaintext — only Alice and Bob can decrypt

## Test Cases

### 1. Initiate E2EE conversation

X3DH key agreement should establish a session with a shared root key.

Input:

```json
{"src":"alice","dest":"e2ee","body":{"type":"initiate_conversation","msg_id":1,"recipient":"bob","bob_public_key":{"identity_key":"IK","signed_pre_key":"SPK"}}}
```

Expected output:

```text
{"type": "conversation_initiated", "in_reply_to": 1, "session_id": ".*", "root_key": ".*"}
```

### 2. Encrypt message with E2EE

Should encrypt message using double ratchet derived key.

Input:

```json
{"src":"alice","dest":"e2ee","body":{"type":"send_message","msg_id":1,"recipient":"bob","plaintext":"Secret message"}}
```

Expected output:

```text
{"type": "message_encrypted", "in_reply_to": 1, "encrypted_message": {"ciphertext": ".*", "auth_tag": ".*"}}
```

## Resources

- [Signal Protocol](https://signal.org/docs/): X3DH and double ratchet: the basis of Signal, WhatsApp, and iMessage E2EE
- [Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/): Double Ratchet Algorithm specification

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
