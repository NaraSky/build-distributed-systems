# 处理配置变更

英文标题：Handle Configuration Changes
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-3-config-change>

课程：8. 分片器：水平扩展与数据迁移
任务序号：3
短标题：配置变更
难度：高级
子主题：Range Sharding

## 中文导读

本题要求你处理分片配置的变更流程。当分片控制器更新了分配方案后，各副本组需要感知到变化并执行数据迁移。这是分布式系统中一个很有挑战性的问题，因为必须保证数据在迁移过程中不丢失、不重复。

## 题目说明

处理分片配置的变更：

1. 副本组定期向控制器轮询配置更新
2. 检测分片分配是否发生了变化
3. 开始迁移：获取新分配给本组的分片数据
4. 在迁移完成之前，不处理客户端请求
5. 向源副本组确认迁移完成

各副本组之间必须协调配合，确保数据的精确一次传输。

## 概念说明

### 配置版本控制

配置信息带有版本号。各副本组必须按顺序逐版本应用配置。如果跳过某个版本，可能会遗漏分片分配的变更，导致数据丢失。

### 迁移协调

当分片发生迁移时，源副本组和目标副本组必须相互协调。源端停止服务该分片、发送数据，目标端接收数据后开始提供服务。通过配置版本号来跟踪迁移进度。

## 涉及概念

- `configuration`
- `coordination`
- `atomic transition`

## 实现提示

- 定期向控制器轮询新配置
- 按照版本顺序处理配置变更
- 在副本之间进行协调

## 测试用例

### 1. 检测配置变更

副本组检测到版本从 1 变为 2，并应用新配置。

输入：

```json
{"src":"c0","dest":"g1","body":{"type":"init","msg_id":1,"node_id":"g1","node_ids":["g1","g2"]}}
{"src":"c0","dest":"g1","body":{"type":"set_config","msg_id":2,"version":1,"shards":[0,1,2]}}
{"src":"controller","dest":"g1","body":{"type":"config_update","msg_id":3,"version":2,"shards":[0,1]}}
```

期望输出：

```text
{"src":"g1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"g1","dest":"c0","body":{"type":"set_config_ok","in_reply_to":2,"msg_id":1}}
{"src":"g1","dest":"controller","body":{"type":"config_update_ok","in_reply_to":3,"msg_id":2,"applied":true}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
