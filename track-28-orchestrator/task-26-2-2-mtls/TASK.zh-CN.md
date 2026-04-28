# 实现服务网格中的双向 TLS 认证

英文标题：Implement mTLS Authentication in Service Mesh
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-2-mtls>

课程：28. 编排器：容器调度与服务网格
任务序号：7
短标题：mTLS
难度：高级
子主题：Service Mesh

## 中文导读

这道题要求你实现一个处理双向 TLS（mTLS）证书操作的节点。在服务网格中，每次服务间调用都必须经过身份认证。普通的 TLS 只要求服务端出示证书，而 mTLS 要求客户端和服务端**双方**都出示证书，任何一方的证书无效都会拒绝连接。即使在集群内部，也不信任任何未经认证的调用，这就是零信任（Zero-Trust）安全模型的核心。

## 题目说明

在服务网格中，每次服务间调用都必须经过身份认证。双向 TLS（mTLS，Mutual TLS）通过要求**客户端和服务端双方**都出示证书来实现这一点。如果任何一方的证书无效或不受信任，连接就会被拒绝，即使是在集群内部也是如此。

请实现一个处理 mTLS 证书操作的节点：

```json
// 两个服务之间的双向 TLS 握手
{ "type": "handshake", "msg_id": 1,
  "client": "service-a", "server": "service-b" }
-> { "type": "handshake_complete", "in_reply_to": 1,
    "success": true, "cipher_suite": "TLS_AES_256_GCM_SHA384" }

// 证书颁发机构为服务签发证书
{ "type": "issue_certificate", "msg_id": 2,
  "service": "service-a" }
-> { "type": "certificate_issued", "in_reply_to": 2,
    "service": "service-a",
    "certificate": "-----BEGIN CERTIFICATE-----...",
    "expiry": "<iso-timestamp>" }

// 验证 SPIFFE 身份标识
{ "type": "verify_identity", "msg_id": 3,
  "spiffe_id": "spiffe://example.com/ns-1/service-a",
  "trust_domain": "example.com" }
-> { "type": "identity_valid", "in_reply_to": 3,
    "valid": true, "service": "service-a", "namespace": "ns-1" }

// 拒绝无效证书
{ "type": "handshake", "msg_id": 4,
  "client": "attacker", "cert": "invalid-cert" }
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

- mTLS 要求客户端和服务端双方都出示证书，而不像普通 TLS 只有服务端出示
- 证书颁发机构（CA）为每个服务签发证书，服务通过 SPIFFE ID 来标识
- SPIFFE ID 格式：`spiffe://<信任域>/ns-<命名空间>/<服务名>`
- 如果任何一方出示的证书无效或不受信任，握手就会失败
- 验证时检查 SPIFFE ID 是否与预期的服务名和信任域匹配

## 测试用例

### 1. 执行 mTLS 握手

有效的双向 TLS 握手应成功完成。

输入：

```json
{"src":"sidecar-a","dest":"sidecar-b","body":{"type":"handshake","msg_id":1,"client":"service-a","server":"service-b"}}
```

期望输出：

```text
{"type": "handshake_complete", "in_reply_to": 1, "success": true, "cipher_suite": "TLS_AES_256_GCM_SHA384"}
```

### 2. 为服务签发证书

证书颁发机构应签发带有过期时间的证书。

输入：

```json
{"src":"service","dest":"ca","body":{"type":"issue_certificate","msg_id":1,"service":"service-a"}}
```

期望输出：

```text
{"type": "certificate_issued", "in_reply_to": 1, "service": "service-a", "certificate": "-----BEGIN CERTIFICATE-----...", "expiry": ".*"}
```

## 参考资料

- [SPIFFE and SPIRE](https://spiffe.io/)：面向所有人的安全生产身份标识框架
- [Istio mTLS](https://istio.io/latest/docs/concepts/security/#mutual-tls-authentication)：Istio 双向 TLS 认证指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
