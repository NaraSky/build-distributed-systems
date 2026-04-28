# 实现 DAG-Based Task Scheduling

英文标题：Implement DAG-Based Task Scheduling
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-2-dag-scheduling>

课程：28. 编排器：容器调度与服务网格
任务序号：2
短标题：DAG Scheduling
难度：advanced
子主题：Scheduling

## 中文导读

本题要求你完成 `实现 DAG-Based Task Scheduling`。

重点关注：`DAG`、`topological sort`、`task dependencies`、`cycle detection`、`parallel execution`。

建议先按提示逐步实现：A DAG is valid if it contains no cycles — use DFS，包含a visiting set to detect back-edges。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A DAG (Directed Acyclic Graph) scheduler orchestrates workflows where tasks have dependencies. Task B cannot start until Task A finishes, but independent tasks can run in parallel, reducing total execution time.

Implement a 节点 that creates, validates,和executes DAG workflows:

```JSON
// Create a DAG: B和C both depend on A
{ "type": "create_dag", "msg_id": 1,
  "tasks": [{"id":"A","command":"run A"},
             {"id":"B","command":"run B"},
             {"id":"C","command":"run C"}],
  "dependencies": [{"task":"B","depends_on":"A"},
                   {"task":"C","depends_on":"A"}] }
-> { "type": "dag_created", "in_reply_to": 1,
    "dag_id": "<uuid>", "valid": true, "tasks": 3 }

// A cycle A->B->C->A is rejected
-> { "type": "dag_invalid", "in_reply_to": 1,
    "error": "Cycle detected in DAG" }

// Execute: run A first, then B和C in parallel
{ "type": "execute_dag", "msg_id": 2, "dag_id": "dag-123" }
-> { "type": "dag_executed", "in_reply_to": 2,
    "execution_id": "<uuid>", "status": "completed",
    "tasks_completed": 3, "duration_seconds": 10 }
```

When a task fails, all tasks that (directly or transitively) depend on it are also marked failed和listed in `failed_tasks`.

## 涉及概念

- `DAG`
- `topological sort`
- `task dependencies`
- `cycle detection`
- `parallel execution`

## 实现提示

- A DAG is valid if it contains no cycles — use DFS，包含a visiting set to detect back-edges
- Topological sort gives safe execution order: a task runs only after all its dependencies finish
- Tasks，包含no unmet dependencies can all be launched in parallel
- If task A fails, mark every task that transitively depends on A as failed
- Use Kahn's algorithm or recursive DFS用于topological ordering

## 测试用例

### 1. 创建和validate DAG

Valid DAG，包含no cycles should be created.

输入：

```json
{"src":"client","dest":"dag","body":{"type":"create_dag","msg_id":1,"tasks":[{"id":"A","command":"run A"},{"id":"B","command":"run B"},{"id":"C","command":"run C"}],"dependencies":[{"task":"B","depends_on":"A"},{"task":"C","depends_on":"A"}]}}
```

期望输出：

```text
{"type": "dag_created", "in_reply_to": 1, "dag_id": ".*", "valid": true, "tasks": 3}
```

### 2. Execute DAG，包含parallel tasks

B和C should run in parallel after A completes.

输入：

```json
{"src":"executor","dest":"dag","body":{"type":"execute_dag","msg_id":1,"dag_id":"dag-123"}}
```

期望输出：

```text
{"type": "dag_executed", "in_reply_to": 1, "execution_id": ".*", "status": "completed", "tasks_completed": 3, "duration_seconds": 10}
```

## 参考资料

- [Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting)：Algorithm用于ordering tasks，包含dependencies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
