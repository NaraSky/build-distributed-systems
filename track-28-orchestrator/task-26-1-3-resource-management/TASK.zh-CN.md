# 实现任务资源管理

英文标题：Implement Resource Management for Jobs
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-3-resource-management>

课程：28. 编排器：容器调度与服务网格
任务序号：3
短标题：Resource Management
难度：进阶
子主题：Scheduling

## 中文导读

这道题要求你实现一个共享资源池的管理节点。在实际系统中，CPU、内存、GPU 等资源是有限的，多个任务会争抢这些资源。资源管理器的职责是追踪可用资源、在资源充足时分配、在资源不足时将任务排队等待。这就像一个停车场管理员，有车位就放行，没车位就让你排队等候。

## 题目说明

任务之间竞争有限的资源，如 CPU、内存和 GPU。资源管理器追踪可用资源，在资源充足时进行分配，并将超出容量的任务排队等待。

请实现一个管理共享资源池的节点：

```json
// 分配资源（资源充足时成功）
{ "type": "allocate", "msg_id": 1,
  "requirements": [{"type": "cpu", "amount": 2},
                   {"type": "memory", "amount": 4}] }
-> { "type": "allocated", "in_reply_to": 1,
    "allocation_id": "<uuid>",
    "resources": {"cpu": 2, "memory": 4} }

// GPU 不足 -> 任务排队
{ "type": "allocate", "msg_id": 2,
  "requirements": [{"type": "gpu", "amount": 4}] }
-> { "type": "queued", "in_reply_to": 2,
    "reason": "Insufficient resources",
    "available": {"gpu": 2}, "required": 4 }

// 任务完成时释放资源
{ "type": "release", "msg_id": 3,
  "allocation_id": "alloc-123", "job_status": "completed" }
-> { "type": "released", "in_reply_to": 3,
    "allocation_id": "alloc-123",
    "resources_freed": {"cpu": 2, "memory": 4} }

// 提交 3 个任务，但并发上限为 2
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

- 维护一个可用资源池，分配时扣减，释放时归还
- 如果请求的资源量超过可用量，返回排队状态，并告知可用量和需求量
- 并发上限限制同一类别同时运行的任务数量，超出的任务排队等待
- 释放操作通过 `allocation_id` 查找并归还对应的资源
- 每次释放后检查是否有排队的任务现在可以获得资源

## 测试用例

### 1. 为任务分配资源

应分配请求的 CPU 和内存。

输入：

```json
{"src":"scheduler","dest":"resources","body":{"type":"allocate","msg_id":1,"requirements":[{"type":"cpu","amount":2},{"type":"memory","amount":4}]}}
```

期望输出：

```text
{"type": "allocated", "in_reply_to": 1, "allocation_id": ".*", "resources": {"cpu": 2, "memory": 4}}
```

### 2. 资源不足时排队

GPU 不足时应将任务排队。

输入：

```json
{"src":"scheduler","dest":"resources","body":{"type":"allocate","msg_id":1,"requirements":[{"type":"gpu","amount":4}]}}
```

期望输出：

```text
{"type": "queued", "in_reply_to": 1, "reason": "Insufficient resources", "available": {"gpu": 2}, "required": 4}
```

## 参考资料

- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)：生产编排系统中的资源请求和限制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
