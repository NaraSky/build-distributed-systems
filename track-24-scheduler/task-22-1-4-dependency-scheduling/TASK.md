# Implement Dependency-Aware Job Scheduling

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-4-dependency-scheduling>

Track: 24. The Scheduler
Task order: 4
Short title: Dependency Scheduling
Difficulty: advanced
Subtrack: Centralized Job Scheduling

## Problem

Some jobs can only start after others finish. Dependency-aware scheduling builds an execution plan that respects these constraints while maximising parallelism: jobs in the same round have no shared dependencies and can run simultaneously.

Implement a node that plans and executes dependency-constrained workflows:

```json
// a has no deps; b and c depend on a; d depends on b and c
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

## Concepts

- topological sort
- critical path
- circular dependency
- failure propagation
- parallel rounds

## Hints

- Build execution plan: each round contains jobs whose all deps completed in prior rounds
- Detect circular deps with DFS — a back-edge during traversal means a cycle
- Critical path: the chain of duration_ms values with the maximum total from source to sink
- On job failure, cancel all jobs that directly or transitively depend on it
- Round 1 = jobs with no deps; Round 2 = jobs whose only deps are in Round 1; and so on

## Test Cases

### 1. Topological sort scheduling

a first, then b/c in parallel, then d.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_workflow","msg_id":1,"jobs":[{"id":"a","deps":[]},{"id":"b","deps":["a"]},{"id":"c","deps":["a"]},{"id":"d","deps":["b","c"]}]}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "workflow_submitted", "in_reply_to": 1, "execution_plan": {"round_1": ["a"], "round_2": ["b", "c"], "round_3": ["d"]}}}
```

### 2. Circular dependency detection

Cycle a->b->c->a should be detected and workflow rejected.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_workflow","msg_id":1,"jobs":[{"id":"a","deps":["b"]},{"id":"b","deps":["c"]},{"id":"c","deps":["a"]}]}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "workflow_rejected", "in_reply_to": 1, "error": "Circular dependency detected: a->b->c->a"}}
```

## Resources

- [Critical Path Method](https://en.wikipedia.org/wiki/Critical_path_method): Finding the longest path through a dependency graph

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
