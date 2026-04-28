# Implement DAG-Based Task Scheduling

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-2-dag-scheduling>

Track: 28. The Orchestrator
Task order: 2
Short title: DAG Scheduling
Difficulty: advanced
Subtrack: Scheduling

## Problem

A DAG (Directed Acyclic Graph) scheduler orchestrates workflows where tasks have dependencies. Task B cannot start until Task A finishes, but independent tasks can run in parallel, reducing total execution time.

Implement a node that creates, validates, and executes DAG workflows:

```json
// Create a DAG: B and C both depend on A
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

// Execute: run A first, then B and C in parallel
{ "type": "execute_dag", "msg_id": 2, "dag_id": "dag-123" }
-> { "type": "dag_executed", "in_reply_to": 2,
    "execution_id": "<uuid>", "status": "completed",
    "tasks_completed": 3, "duration_seconds": 10 }
```

When a task fails, all tasks that (directly or transitively) depend on it are also marked failed and listed in `failed_tasks`.

## Concepts

- DAG
- topological sort
- task dependencies
- cycle detection
- parallel execution

## Hints

- A DAG is valid if it contains no cycles — use DFS with a visiting set to detect back-edges
- Topological sort gives safe execution order: a task runs only after all its dependencies finish
- Tasks with no unmet dependencies can all be launched in parallel
- If task A fails, mark every task that transitively depends on A as failed
- Use Kahn's algorithm or recursive DFS for topological ordering

## Test Cases

### 1. Create and validate DAG

Valid DAG with no cycles should be created.

Input:

```json
{"src":"client","dest":"dag","body":{"type":"create_dag","msg_id":1,"tasks":[{"id":"A","command":"run A"},{"id":"B","command":"run B"},{"id":"C","command":"run C"}],"dependencies":[{"task":"B","depends_on":"A"},{"task":"C","depends_on":"A"}]}}
```

Expected output:

```text
{"type": "dag_created", "in_reply_to": 1, "dag_id": ".*", "valid": true, "tasks": 3}
```

### 2. Execute DAG with parallel tasks

B and C should run in parallel after A completes.

Input:

```json
{"src":"executor","dest":"dag","body":{"type":"execute_dag","msg_id":1,"dag_id":"dag-123"}}
```

Expected output:

```text
{"type": "dag_executed", "in_reply_to": 1, "execution_id": ".*", "status": "completed", "tasks_completed": 3, "duration_seconds": 10}
```

## Resources

- [Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting): Algorithm for ordering tasks with dependencies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
