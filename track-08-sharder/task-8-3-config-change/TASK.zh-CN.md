#处理Configuration Changes

英文标题：Handle Configuration Changes
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-3-config-change>

课程：8. 分片器：水平扩展与数据迁移
任务序号：3
短标题：Config Change
难度：advanced
子主题：Range Sharding

## 中文导读

本题要求你完成 `Handle Configuration Changes`。

重点关注：`configuration`、`coordination`、`atomic transition`。

建议先按提示逐步实现：Poll controller用于new configs。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Handle 分片 configuration changes:

1. Replica groups poll controller用于configuration updates
2. Detect when 分片 assignment changes
3. Start migration: fetch shards assigned to this group
4. Complete migration before processing 客户端 requests
5. Acknowledge migration to source groups

Groups must coordinate to ensure exactly-once transfer.

## 概念说明

### Configuration Versioning

Configurations are versioned. Groups must apply configurations in order. Skip a version和you might miss a 分片 assignment, leading to data loss.

### Migration Coordination

When shards move, both source和destination must coordinate. Source stops serving the 分片, sends data, destination takes over. Use config version to track progress.

## 涉及概念

- `configuration`
- `coordination`
- `atomic transition`

## 实现提示

- Poll controller用于new configs
- Process configs in order
- Coordinate between replicas

## 测试用例

### 1. Detect config change

Group detects version change (1→2)和applies new config.

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
