# 实现基于有向无环图的任务调度

英文标题：Implement DAG-Based Task Scheduling
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-2-dag-scheduling>

课程：28. 编排器：容器调度与服务网格
任务序号：2
短标题：DAG Scheduling
难度：高级
子主题：Scheduling

## 中文导读

这道题要求你实现一个基于有向无环图（DAG）的任务调度器。在复杂的工作流中，任务之间往往存在依赖关系，比如"任务 B 必须等任务 A 完成后才能开始"。DAG 调度器能正确处理这些依赖：先执行没有前置依赖的任务，互不依赖的任务可以并行执行，从而缩短整体执行时间。这是数据管道和 CI/CD 流水线等场景的核心技术。

## 题目说明

DAG（Directed Acyclic Graph，有向无环图）调度器编排具有依赖关系的工作流。任务 B 必须等任务 A 完成后才能开始，但互相独立的任务可以并行运行，从而缩短总执行时间。

请实现一个创建、验证和执行 DAG 工作流的节点：

```json
// 创建一个 DAG：B 和 C 都依赖于 A
{ "type": "create_dag", "msg_id": 1,
  "tasks": [{"id":"A","command":"run A"},
             {"id":"B","command":"run B"},
             {"id":"C","command":"run C"}],
  "dependencies": [{"task":"B","depends_on":"A"},
                   {"task":"C","depends_on":"A"}] }
-> { "type": "dag_created", "in_reply_to": 1,
    "dag_id": "<uuid>", "valid": true, "tasks": 3 }

// 存在环（A->B->C->A）的 DAG 会被拒绝
-> { "type": "dag_invalid", "in_reply_to": 1,
    "error": "Cycle detected in DAG" }

// 执行：先运行 A，然后 B 和 C 并行执行
{ "type": "execute_dag", "msg_id": 2, "dag_id": "dag-123" }
-> { "type": "dag_executed", "in_reply_to": 2,
    "execution_id": "<uuid>", "status": "completed",
    "tasks_completed": 3, "duration_seconds": 10 }
```

当某个任务失败时，所有直接或间接依赖它的任务也会被标记为失败，并列在 `failed_tasks` 中。

## 涉及概念

- `DAG`
- `topological sort`
- `task dependencies`
- `cycle detection`
- `parallel execution`

## 实现提示

- 一个有效的 DAG 不能包含环，可以使用深度优先搜索（DFS）配合"正在访问"集合来检测回边
- 拓扑排序（Topological Sort）给出安全的执行顺序：一个任务只在所有依赖项完成后才运行
- 没有未满足依赖的任务可以同时并行启动
- 如果任务 A 失败，所有传递性依赖于 A 的任务都要标记为失败
- 可以使用 Kahn 算法或递归 DFS 来实现拓扑排序

## 测试用例

### 1. 创建并验证 DAG

没有环的有效 DAG 应成功创建。

输入：

```json
{"src":"client","dest":"dag","body":{"type":"create_dag","msg_id":1,"tasks":[{"id":"A","command":"run A"},{"id":"B","command":"run B"},{"id":"C","command":"run C"}],"dependencies":[{"task":"B","depends_on":"A"},{"task":"C","depends_on":"A"}]}}
```

期望输出：

```text
{"type": "dag_created", "in_reply_to": 1, "dag_id": ".*", "valid": true, "tasks": 3}
```

### 2. 执行包含并行任务的 DAG

A 完成后，B 和 C 应并行执行。

输入：

```json
{"src":"executor","dest":"dag","body":{"type":"execute_dag","msg_id":1,"dag_id":"dag-123"}}
```

期望输出：

```text
{"type": "dag_executed", "in_reply_to": 1, "execution_id": ".*", "status": "completed", "tasks_completed": 3, "duration_seconds": 10}
```

## 参考资料

- [Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting)：用于对有依赖关系的任务进行排序的算法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
