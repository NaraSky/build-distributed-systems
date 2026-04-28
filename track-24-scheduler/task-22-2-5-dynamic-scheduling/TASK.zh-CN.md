# 实现 Dynamic Scheduling，包含Locality Awareness

英文标题：Implement Dynamic Scheduling，包含Locality Awareness
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-5-dynamic-scheduling>

课程：24. 调度器：任务调度
任务序号：10
短标题：Locality Scheduling
难度：advanced
子主题：Distributed Work Allocation

## 中文导读

本题要求你完成 `实现 Dynamic Scheduling，包含Locality Awareness`。

重点关注：`data locality`、`rack awareness`、`worker scoring`、`dynamic data placement`、`load vs locality tradeoff`。

建议先按提示逐步实现：Score workers: +2 if it hosts all input files, +1 if in the same rack, 0 otherwise。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Moving a job to where its data lives is cheaper than shipping large data over the 网络. Locality-aware scheduling scores workers based on data proximity, then selects the best-scoring, least-loaded worker.

Implement a 节点 that makes locality-aware scheduling decisions:

```JSON
// 节点-1 hosts the data but is 90% loaded; 节点-2 is in same rack, 30% loaded
{ "type": "submit_job", "msg_id": 1,
  "job": {"id":"job1","inputs":["data.csv"]},
  "topology": {"rack1":["节点-1","节点-2"]},
  "data_location": "节点-1",
  "节点-1_utilization": 0.9,
  "节点-2_utilization": 0.3 }
-> { "type": "job_assigned", "in_reply_to": 1,
    "worker": "节点-2",
    "reason": "Same rack as data (rack1)和less loaded than 节点-1" }

// Data moves to 节点-5 -> future jobs follow it
{ "type": "update_data_location", "msg_id": 1,
  "file": "data.csv", "old_location": "节点-1", "new_location": "节点-5" }
{ "type": "submit_job", "msg_id": 2,
  "job": {"id":"job1","inputs":["data.csv"]} }
-> { "type": "job_assigned", "in_reply_to": 2,
    "worker": "节点-5", "reason": "Data moved to 节点-5" }
```

## 涉及概念

- `data locality`
- `rack awareness`
- `worker scoring`
- `dynamic data placement`
- `load vs locality tradeoff`

## 实现提示

- Score workers: +2 if it hosts all input files, +1 if in the same rack, 0 otherwise
- Among equal locality scores, prefer the worker，包含lower current utilization
- Rack-aware: same-rack worker preferred over cross-rack even if the exact data 节点 is overloaded
- update_data_location changes the data map; subsequent jobs use the new location
- locality_aware balances speed和fairness: faster than load-balancing, more even than locality-only

## 测试用例

### 1. Locality-aware scheduling

Should prefer the worker hosting the most input data.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"workers":["node-1","node-2","node-3"],"data_map":{"file1.txt":["node-1"],"file2.txt":["node-2"]}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"job1","inputs":["file1.txt","file2.txt"]}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Rack-aware scheduling

节点-2 (same rack, lower utilization) should be preferred over overloaded 节点-1.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"job1","inputs":["data.csv"]},"topology":{"rack1":["node-1","node-2"],"rack2":["node-3","node-4"]},"data_location":"node-1","node-1_utilization":0.9,"node-2_utilization":0.3}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_assigned", "in_reply_to": 1, "worker": "node-2", "reason": "Same rack as data (rack1)和less loaded than node-1"}}
```

## 参考资料

- [Data Locality in Hadoop](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)：How Hadoop uses data locality用于scheduling decisions

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
