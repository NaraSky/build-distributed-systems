# 1. The Messenger

中文名：信使：消息通信基础

## 按子主题分组

### Hello, Distributed World

- 1. [`task-1-1-json-parser`](task-1-1-json-parser/TASK.zh-CN.md) - 实现 基础 JSON 消息 解析器
- 2. [`task-1-2-init-handler`](task-1-2-init-handler/TASK.zh-CN.md) -处理初始化 消息和存储集群元数据
- 3. [`task-1-3-echo-service`](task-1-3-echo-service/TASK.zh-CN.md) - 实现 回声 服务，包含正确的 确认响应
- 4. [`task-1-4-envelope-validation`](task-1-4-envelope-validation/TASK.zh-CN.md) - 添加 消息 信封 校验
- 5. [`task-1-5-async-handler`](task-1-5-async-handler/TASK.zh-CN.md) - 创建 异步 事件循环用于Concurrent 消息处理

### RPC和the Request-Response模式l

- 6. [`task-1-2-1-sync-rpc`](task-1-2-1-sync-rpc/TASK.zh-CN.md) - 实现 同步 RPC，包含超时
- 7. [`task-1-2-2-timeout-retry`](task-1-2-2-timeout-retry/TASK.zh-CN.md) - 实现 超时和重试循环用于RPC
- 8. [`task-1-2-3-async-rpc`](task-1-2-3-async-rpc/TASK.zh-CN.md) - 实现 异步 RPC使用Callbacks
- 9. [`task-1-2-4-callback-reaper`](task-1-2-4-callback-reaper/TASK.zh-CN.md) - 实现 回调 清理器用于Leaked RPCs
- 10. [`task-1-2-5-exponential-backoff`](task-1-2-5-exponential-backoff/TASK.zh-CN.md) - 实现 指数退避用于Retries

### The Protocol Beneath

- 11. [`task-1-3-1-typed-schema`](task-1-3-1-typed-schema/TASK.zh-CN.md) -模式l 消息格式，包含类型化模式
- 12. [`task-1-3-2-envelope-logger`](task-1-3-2-envelope-logger/TASK.zh-CN.md) - 添加 消息 信封 日志器，包含Timestamps
- 13. [`task-1-3-3-deduplication`](task-1-3-3-deduplication/TASK.zh-CN.md) - 实现 消息 去重，包含LRU 缓存
- 14. [`task-1-3-4-throughput-bench`](task-1-3-4-throughput-bench/TASK.zh-CN.md) - 基准测试节点吞吐量和延迟
- 15. [`task-1-3-5-chaos-mode`](task-1-3-5-chaos-mode/TASK.zh-CN.md) - 添加 混沌模式，包含Random 消息丢弃
