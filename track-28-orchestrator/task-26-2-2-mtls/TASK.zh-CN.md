# 实现 mTLS Authentication in 服务 Mesh

英文标题：Implement mTLS Authentication in Service Mesh
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-2-mtls>

课程：28. 编排器：容器调度与服务网格
任务序号：7
短标题：mTLS
难度：advanced
子主题：服务 Mesh

## 中文导读

本题要求你完成 `实现 mTLS Authentication in 服务 Mesh`。

重点关注：`mTLS`、`mutual TLS`、`certificate authority`、`SPIFFE`、`service identity`。

建议先按提示逐步实现：mTLS: both 客户端和服务端 present certificates — not just the 服务端 as in regular TLS。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In a service mesh, every service-to-service call must be authenticated. mTLS (mutual TLS) achieves this by requiring **both** the 客户端和the 服务端 to present a certificate. If either certificate is invalid or untrusted, the connection is rejected — even inside the 集群.

Implement a 节点 that handles mTLS certificate operations:

```JSON
// Mutual TLS handshake between two services
{ "type": "handshake", "msg_id": 1,
  "客户端": "service-a", "服务端": "service-b" }
-> { "type": "handshake_complete", "in_reply_to": 1,
    "success": true, "cipher_suite": "TLS_AES_256_GCM_SHA384" }

// CA issues a certificate用于a service
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
  "客户端": "attacker", "cert": "invalid-cert" }
-> { "type": "handshake_failed", "in_reply_to": 4,
    "reason": "Invalid certificate", "success": false }
```

## 涉及概念

- `mTLS`
- `mutual TLS`
- `certificate authority`
- `SPIFFE`
- `service identity`
- `zero-trust`

## 实现提示

- mTLS: both 客户端和服务端 present certificates — not just the 服务端 as in regular TLS
- The CA issues a certificate用于each service identified by a SPIFFE ID
- SPIFFE format: spiffe://<trust-domain>/ns-<namespace>/<service-name>
- A handshake fails if either party presents an invalid or untrusted certificate
- Verify: check that the SPIFFE ID matches the expected service和trust domain

## 测试用例

### 1. Perform mTLS handshake

Valid mutual TLS handshake should succeed.

输入：

```json
{"src":"sidecar-a","dest":"sidecar-b","body":{"type":"handshake","msg_id":1,"client":"service-a","server":"service-b"}}
```

期望输出：

```text
{"type": "handshake_complete", "in_reply_to": 1, "success": true, "cipher_suite": "TLS_AES_256_GCM_SHA384"}
```

### 2. Issue certificate用于服务

CA should issue a certificate，包含an expiry timestamp.

输入：

```json
{"src":"service","dest":"ca","body":{"type":"issue_certificate","msg_id":1,"service":"service-a"}}
```

期望输出：

```text
{"type": "certificate_issued", "in_reply_to": 1, "service": "service-a", "certificate": "-----BEGIN CERTIFICATE-----...", "expiry": ".*"}
```

## 参考资料

- [SPIFFE和SPIRE](https://spiffe.io/)：Secure Production Identity Framework用于Everyone
- [Istio mTLS](https://istio.io/latest/docs/concepts/security/#mutual-tls-authentication)：Istio mTLS authentication guide

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
