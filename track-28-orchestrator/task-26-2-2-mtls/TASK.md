# Implement mTLS Authentication in Service Mesh

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-2-mtls>

Track: 28. The Orchestrator
Task order: 7
Short title: mTLS
Difficulty: advanced
Subtrack: Service Mesh

## Problem

In a service mesh, every service-to-service call must be authenticated. mTLS (mutual TLS) achieves this by requiring **both** the client and the server to present a certificate. If either certificate is invalid or untrusted, the connection is rejected — even inside the cluster.

Implement a node that handles mTLS certificate operations:

```json
// Mutual TLS handshake between two services
{ "type": "handshake", "msg_id": 1,
  "client": "service-a", "server": "service-b" }
-> { "type": "handshake_complete", "in_reply_to": 1,
    "success": true, "cipher_suite": "TLS_AES_256_GCM_SHA384" }

// CA issues a certificate for a service
{ "type": "issue_certificate", "msg_id": 2,
  "service": "service-a" }
-> { "type": "certificate_issued", "in_reply_to": 2,
    "service": "service-a",
    "certificate": "-----BEGIN CERTIFICATE-----...",
    "expiry": "<iso-timestamp>" }

// Verify a SPIFFE identity
{ "type": "verify_identity", "msg_id": 3,
  "spiffe_id": "spiffe://example.com/ns-1/service-a",
  "trust_domain": "example.com" }
-> { "type": "identity_valid", "in_reply_to": 3,
    "valid": true, "service": "service-a", "namespace": "ns-1" }

// Reject an invalid certificate
{ "type": "handshake", "msg_id": 4,
  "client": "attacker", "cert": "invalid-cert" }
-> { "type": "handshake_failed", "in_reply_to": 4,
    "reason": "Invalid certificate", "success": false }
```

## Concepts

- mTLS
- mutual TLS
- certificate authority
- SPIFFE
- service identity
- zero-trust

## Hints

- mTLS: both client and server present certificates — not just the server as in regular TLS
- The CA issues a certificate for each service identified by a SPIFFE ID
- SPIFFE format: spiffe://<trust-domain>/ns-<namespace>/<service-name>
- A handshake fails if either party presents an invalid or untrusted certificate
- Verify: check that the SPIFFE ID matches the expected service and trust domain

## Test Cases

### 1. Perform mTLS handshake

Valid mutual TLS handshake should succeed.

Input:

```json
{"src":"sidecar-a","dest":"sidecar-b","body":{"type":"handshake","msg_id":1,"client":"service-a","server":"service-b"}}
```

Expected output:

```text
{"type": "handshake_complete", "in_reply_to": 1, "success": true, "cipher_suite": "TLS_AES_256_GCM_SHA384"}
```

### 2. Issue certificate for service

CA should issue a certificate with an expiry timestamp.

Input:

```json
{"src":"service","dest":"ca","body":{"type":"issue_certificate","msg_id":1,"service":"service-a"}}
```

Expected output:

```text
{"type": "certificate_issued", "in_reply_to": 1, "service": "service-a", "certificate": "-----BEGIN CERTIFICATE-----...", "expiry": ".*"}
```

## Resources

- [SPIFFE and SPIRE](https://spiffe.io/): Secure Production Identity Framework for Everyone
- [Istio mTLS](https://istio.io/latest/docs/concepts/security/#mutual-tls-authentication): Istio mTLS authentication guide

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
