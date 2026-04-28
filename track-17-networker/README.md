# 17. The Networker

中文名：网络器：TCP 与协议基础

## 按子主题分组

### TCP From Scratch

- 1. [`task-5-1-1-tcp-echo`](task-5-1-1-tcp-echo/TASK.zh-CN.md) - 构建 a TCP 回声 Server from Raw Syscalls
- 2. [`task-5-1-2-connection-pool`](task-5-1-2-connection-pool/TASK.zh-CN.md) - 添加 a Connection Pool，包含Configurable Backlog
- 3. [`task-5-1-3-graceful-shutdown`](task-5-1-3-graceful-shutdown/TASK.zh-CN.md) - 实现 Graceful Shutdown，包含In-Flight Drain
- 4. [`task-5-1-4-keepalive`](task-5-1-4-keepalive/TASK.zh-CN.md) - 实现 Application-Level TCP Keep-Alive
- 5. [`task-5-1-5-throughput-bench`](task-5-1-5-throughput-bench/TASK.zh-CN.md) - 基准测试 Server 吞吐量和延迟

### 消息 Framing和Serialization

- 6. [`task-5-2-1-length-prefix`](task-5-2-1-length-prefix/TASK.zh-CN.md) - 实现 Length-Prefixed 消息 Framing
- 7. [`task-5-2-2-line-delimited`](task-5-2-2-line-delimited/TASK.zh-CN.md) - 实现 Line-Delimited Framing (Redis RESP Style)
- 8. [`task-5-2-3-binary-serialization`](task-5-2-3-binary-serialization/TASK.zh-CN.md) - 实现 a Binary Serialization格式
- 9. [`task-5-2-4-compression`](task-5-2-4-compression/TASK.zh-CN.md) - 添加 消息 Compression，包含CPU-Bandwidth Tradeoff Analysis
- 10. [`task-5-2-5-protocol-versioning`](task-5-2-5-protocol-versioning/TASK.zh-CN.md) - 实现 Protocol Versioning，包含Backward Compatibility

### gRPC和Protocol Buffers

- 11. [`task-5-3-1-protobuf-schema`](task-5-3-1-protobuf-schema/TASK.zh-CN.md) - Define和Encode Protocol Buffer Messages
- 12. [`task-5-3-2-grpc-unary`](task-5-3-2-grpc-unary/TASK.zh-CN.md) - 实现 a gRPC Unary RPC 服务
- 13. [`task-5-3-3-grpc-streaming`](task-5-3-3-grpc-streaming/TASK.zh-CN.md) - 实现 gRPC Server和Bidirectional Streaming
- 14. [`task-5-3-4-grpc-interceptors`](task-5-3-4-grpc-interceptors/TASK.zh-CN.md) - 构建 gRPC Interceptors用于Logging, Auth,和Rate Limiting
- 15. [`task-5-3-5-grpc-vs-rest`](task-5-3-5-grpc-vs-rest/TASK.zh-CN.md) - Compare gRPC vs REST: 延迟, Size,和DX
