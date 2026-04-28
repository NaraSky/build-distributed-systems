# 实现依赖感知的任务调度

英文标题：Implement Dependency-Aware Job Scheduling
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-4-dependency-scheduling>

课程：24. 任务调度器
任务序号：4
短标题：依赖调度
难度：高级
子主题：集中式任务调度

## 中文导读

这道题要求你实现依赖感知调度（Dependency Scheduling），即在任务之间存在先后依赖关系时，构建一个合理的执行计划。没有依赖关系的任务可以并行执行，有依赖关系的必须按序执行。这就像做菜时，"切菜"和"烧水"可以同时做，但"炒菜"必须等切完菜之后。

## 题目说明

有些任务必须等其他任务完成后才能开始。依赖感知调度会构建一个执行计划，在遵守依赖约束的同时最大化并行度：同一轮中的任务互不依赖，可以同时运行。

实现一个能规划和执行带依赖约束的工作流的节点：

```json
// a 没有依赖；b 和 c 依赖 a；d 依赖 b 和 c
{ "type": "submit_workflow", "msg_id": 1,
  "jobs": [{"id":"a","deps":[]},{"id":"b","deps":["a"]},
            {"id":"c","deps":["a"]},{"id":"d","deps":["b","c"]}] }
-> { "type": "workflow_submitted", "in_reply_to": 1,
    "execution_plan": {"round_1":["a"],"round_2":["b","c"],"round_3":["d"]} }

// 检测到循环依赖
-> { "type": "workflow_rejected",
    "error": "Circular dependency detected: a->b->c->a" }

// 关键路径：a(100ms)->b(200ms)=300ms vs a(100ms)->c(50ms)=150ms
{ "type": "submit_workflow", "msg_id": 3,
  "jobs": [{"id":"a","duration_ms":100,"deps":[]},
            {"id":"b","duration_ms":200,"deps":["a"]},
            {"id":"c","duration_ms":50,"deps":["a"]}] }
-> { "type": "workflow_submitted", "in_reply_to": 3,
    "critical_path": ["a","b"], "critical_path_length_ms": 300 }
```

当某个任务失败时，所有直接或间接依赖它的任务都必须被取消。

## 涉及概念

- topological sort
- critical path
- circular dependency
- failure propagation
- parallel rounds

## 实现提示

- 构建执行计划：每一轮包含所有依赖已在前序轮次中完成的任务
- 使用深度优先搜索检测循环依赖：遍历中遇到回边说明存在环
- 关键路径：从源头到终点的最长耗时路径，由各任务的 `duration_ms` 累加得出
- 任务失败时，取消所有直接或间接依赖该任务的后续任务
- 第一轮 = 没有依赖的任务；第二轮 = 所有依赖仅在第一轮中的任务；以此类推

## 测试用例

### 1. 拓扑排序调度

先执行 a，然后 b 和 c 并行，最后执行 d。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_workflow","msg_id":1,"jobs":[{"id":"a","deps":[]},{"id":"b","deps":["a"]},{"id":"c","deps":["a"]},{"id":"d","deps":["b","c"]}]}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "workflow_submitted", "in_reply_to": 1, "execution_plan": {"round_1": ["a"], "round_2": ["b", "c"], "round_3": ["d"]}}}
```

### 2. 检测循环依赖

环路 a->b->c->a 应被检测到，工作流应被拒绝。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_workflow","msg_id":1,"jobs":[{"id":"a","deps":["b"]},{"id":"b","deps":["c"]},{"id":"c","deps":["a"]}]}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "workflow_rejected", "in_reply_to": 1, "error": "Circular dependency detected: a->b->c->a"}}
```

## 参考资料

- [Critical Path Method](https://en.wikipedia.org/wiki/Critical_path_method)：在依赖图中寻找最长路径的方法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
