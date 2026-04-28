# 实现 Dependency-Aware Job Scheduling

英文标题：Implement Dependency-Aware Job Scheduling
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-4-dependency-scheduling>

课程：24. 调度器：任务调度
任务序号：4
短标题：Dependency Scheduling
难度：advanced
子主题：Centralized Job Scheduling

## 中文导读

本题要求你完成 `实现 Dependency-Aware Job Scheduling`。

重点关注：`topological sort`、`critical path`、`circular dependency`、`failure propagation`、`parallel rounds`。

建议先按提示逐步实现：Build execution plan: each round contains jobs whose all deps completed in prior rounds。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Some jobs can only start after others finish. Dependency-aware scheduling builds an execution plan that respects these constraints while maximising parallelism: jobs in the same round have no shared dependencies和can run simultaneously.

Implement a 节点 that plans和executes dependency-constrained workflows:

```JSON
// a has no deps; b和c depend on a; d depends on b和c
{ "type": "submit_workflow", "msg_id": 1,
  "jobs": [{"id":"a","deps":[]},{"id":"b","deps":["a"]},
            {"id":"c","deps":["a"]},{"id":"d","deps":["b","c"]}] }
-> { "type": "workflow_submitted", "in_reply_to": 1,
    "execution_plan": {"round_1":["a"],"round_2":["b","c"],"round_3":["d"]} }

// Circular dependency detected
-> { "type": "workflow_rejected",
    "error": "Circular dependency detected: a->b->c->a" }

// Critical path: a(100ms)->b(200ms)=300ms vs a(100ms)->c(50ms)=150ms
{ "type": "submit_workflow", "msg_id": 3,
  "jobs": [{"id":"a","duration_ms":100,"deps":[]},
            {"id":"b","duration_ms":200,"deps":["a"]},
            {"id":"c","duration_ms":50,"deps":["a"]}] }
-> { "type": "workflow_submitted", "in_reply_to": 3,
    "critical_path": ["a","b"], "critical_path_length_ms": 300 }
```

When a job fails, every job that (directly or transitively) depends on it must be cancelled.

## 涉及概念

- `topological sort`
- `critical path`
- `circular dependency`
- `failure propagation`
- `parallel rounds`

## 实现提示

- Build execution plan: each round contains jobs whose all deps completed in prior rounds
- Detect circular deps，包含DFS — a back-edge during traversal means a cycle
- Critical path: the chain of duration_ms values，包含the maximum total from source to sink
- On job 故障, cancel all jobs that directly or transitively depend on it
- Round 1 = jobs，包含no deps; Round 2 = jobs whose only deps are in Round 1;和so on

## 测试用例

### 1. Topological sort scheduling

a first, then b/c in parallel, then d.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_workflow","msg_id":1,"jobs":[{"id":"a","deps":[]},{"id":"b","deps":["a"]},{"id":"c","deps":["a"]},{"id":"d","deps":["b","c"]}]}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "workflow_submitted", "in_reply_to": 1, "execution_plan": {"round_1": ["a"], "round_2": ["b", "c"], "round_3": ["d"]}}}
```

### 2. Circular dependency detection

Cycle a->b->c->a should be detected和workflow rejected.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_workflow","msg_id":1,"jobs":[{"id":"a","deps":["b"]},{"id":"b","deps":["c"]},{"id":"c","deps":["a"]}]}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "workflow_rejected", "in_reply_to": 1, "error": "Circular dependency detected: a->b->c->a"}}
```

## 参考资料

- [Critical Path Method](https://en.wikipedia.org/wiki/Critical_path_method)：Finding the longest path through a dependency graph

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
