# 实现数据本地性感知的动态调度

英文标题：Implement Dynamic Scheduling with Locality Awareness
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-5-dynamic-scheduling>

课程：24. 任务调度器
任务序号：10
短标题：本地性调度
难度：高级
子主题：分布式任务分配

## 中文导读

这道题要求你实现数据本地性感知的调度。核心思想是"把计算搬到数据旁边"，而不是把大量数据通过网络搬到计算节点上，因为移动数据的代价远大于移动计算逻辑。调度器需要综合考虑数据位置、机架拓扑和节点负载，选出最优的执行节点。

## 题目说明

把任务调度到数据所在的节点执行，远比通过网络传输大量数据划算。本地性感知调度（Locality-Aware Scheduling）根据数据的远近给工作节点打分，然后选择得分最高、负载最低的节点来执行任务。

你需要实现一个能做出本地性感知调度决策的节点：

```json
// node-1 持有数据但负载 90%；node-2 在同一机架，负载 30%
{ "type": "submit_job", "msg_id": 1,
  "job": {"id":"job1","inputs":["data.csv"]},
  "topology": {"rack1":["node-1","node-2"]},
  "data_location": "node-1",
  "node-1_utilization": 0.9,
  "node-2_utilization": 0.3 }
-> { "type": "job_assigned", "in_reply_to": 1,
    "worker": "node-2",
    "reason": "Same rack as data (rack1) and less loaded than node-1" }

// 数据迁移到 node-5 -> 后续任务跟着走
{ "type": "update_data_location", "msg_id": 1,
  "file": "data.csv", "old_location": "node-1", "new_location": "node-5" }
{ "type": "submit_job", "msg_id": 2,
  "job": {"id":"job1","inputs":["data.csv"]} }
-> { "type": "job_assigned", "in_reply_to": 2,
    "worker": "node-5", "reason": "Data moved to node-5" }
```

评分规则如下：如果节点持有任务所需的全部输入文件，得 2 分；如果节点与数据在同一个机架（Rack），得 1 分；否则得 0 分。得分相同时，优先选择当前负载更低的节点。这种方式在速度和公平性之间取得了平衡：比纯负载均衡更快（数据不用搬），比纯本地性优先更均匀（不会让某个节点过载）。

## 涉及概念

- data locality
- rack awareness
- worker scoring
- dynamic data placement
- load vs locality tradeoff

## 实现提示

- 工作节点评分：持有所有输入文件得 +2 分，与数据在同一机架得 +1 分，否则得 0 分
- 本地性得分相同时，优先选择当前负载更低的节点
- 机架感知：即使数据节点负载过高，同机架的节点也优于跨机架的节点
- `update_data_location` 更新数据位置映射，后续任务使用新的位置信息
- 本地性感知调度在速度和公平性之间取得平衡：比纯负载均衡更快，比纯本地性优先更均匀

## 测试用例

### 1. 本地性感知调度

应优先选择持有最多输入数据的工作节点。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"workers":["node-1","node-2","node-3"],"data_map":{"file1.txt":["node-1"],"file2.txt":["node-2"]}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"job1","inputs":["file1.txt","file2.txt"]}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 机架感知调度

node-2（同一机架、负载更低）应优先于负载过高的 node-1。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"job1","inputs":["data.csv"]},"topology":{"rack1":["node-1","node-2"],"rack2":["node-3","node-4"]},"data_location":"node-1","node-1_utilization":0.9,"node-2_utilization":0.3}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_assigned", "in_reply_to": 1, "worker": "node-2", "reason": "Same rack as data (rack1) and less loaded than node-1"}}
```

## 参考资料

- [Data Locality in Hadoop](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)：Hadoop 如何利用数据本地性进行调度决策

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
