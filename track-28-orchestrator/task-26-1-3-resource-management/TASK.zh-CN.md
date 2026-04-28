# 实现 Resource Management用于Jobs

英文标题：Implement Resource Management用于Jobs
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-3-resource-management>

课程：28. 编排器：容器调度与服务网格
任务序号：3
短标题：Resource Management
难度：intermediate
子主题：Scheduling

## 中文导读

本题要求你完成 `实现 Resource Management用于Jobs`。

重点关注：`resource allocation`、`resource pool`、`job queuing`、`concurrency limit`、`fairness`。

建议先按提示逐步实现：Track a pool of available resources; subtract on allocate, restore on release。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Jobs compete用于finite resources like CPU, memory,和GPU. Resource management tracks what is available, grants allocations when possible,和queues jobs that would exceed capacity.

Implement a 节点 that manages a shared resource pool:

```JSON
// Allocate resources (succeeds if enough available)
{ "type": "allocate", "msg_id": 1,
  "requirements": [{"type": "cpu", "amount": 2},
                   {"type": "memory", "amount": 4}] }
-> { "type": "allocated", "in_reply_to": 1,
    "allocation_id": "<uuid>",
    "resources": {"cpu": 2, "memory": 4} }

// Not enough GPU -> 队列 the job
{ "type": "allocate", "msg_id": 2,
  "requirements": [{"type": "gpu", "amount": 4}] }
-> { "type": "queued", "in_reply_to": 2,
    "reason": "Insufficient resources",
    "available": {"gpu": 2}, "required": 4 }

// Release resources when job finishes
{ "type": "release", "msg_id": 3,
  "allocation_id": "alloc-123", "job_status": "completed" }
-> { "type": "released", "in_reply_to": 3,
    "allocation_id": "alloc-123",
    "resources_freed": {"cpu": 2, "memory": 4} }

// Submit 3 jobs，包含a concurrency cap of 2
{ "type": "submit_job", "msg_id": 4,
  "category": "heavy", "concurrency_limit": 2, "jobs": 3 }
-> { "type": "jobs_submitted", "in_reply_to": 4,
    "queued": 1, "running": 2, "waiting": 1 }
```

## 涉及概念

- `resource allocation`
- `resource pool`
- `job queuing`
- `concurrency limit`
- `fairness`

## 实现提示

- Track a pool of available resources; subtract on allocate, restore on release
- If requested amount exceeds available, return queued，包含available和required amounts
- concurrency_limit caps how many jobs of a category run simultaneously; 队列 the rest
- release returns which resources were freed使用the allocation_id as the key
- After a release, check if any queued jobs can now be allocated

## 测试用例

### 1. Allocate resources用于job

Should allocate requested CPU和memory.

输入：

```json
{"src":"scheduler","dest":"resources","body":{"type":"allocate","msg_id":1,"requirements":[{"type":"cpu","amount":2},{"type":"memory","amount":4}]}}
```

期望输出：

```text
{"type": "allocated", "in_reply_to": 1, "allocation_id": ".*", "resources": {"cpu": 2, "memory": 4}}
```

### 2. 队列 job when resources unavailable

Insufficient GPU should 队列 the job.

输入：

```json
{"src":"scheduler","dest":"resources","body":{"type":"allocate","msg_id":1,"requirements":[{"type":"gpu","amount":4}]}}
```

期望输出：

```text
{"type": "queued", "in_reply_to": 1, "reason": "Insufficient resources", "available": {"gpu": 2}, "required": 4}
```

## 参考资料

- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)：Resource requests和limits in production orchestration

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
