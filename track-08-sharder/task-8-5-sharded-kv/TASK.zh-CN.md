# 构建完整的分片键值存储

英文标题：Build Complete Sharded Key-Value Store
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-5-sharded-kv>

课程：8. 分片器：水平扩展与数据迁移
任务序号：5
短标题：分片键值存储
难度：高级
子主题：Range Sharding

## 中文导读

本题要求你将前面所有组件整合起来，构建一个完整的分片键值存储系统。客户端需要根据配置信息将请求路由到正确的副本组，并在配置变更时自动重试。这是对整个分片系统的端到端集成，是本系列的综合大练习。

## 题目说明

构建一个完整的分片键值存储系统：

1. 客户端根据键确定它属于哪个分片
2. 客户端将请求路由到拥有该分片的副本组
3. 如果发到了错误的副本组，获取新配置并重试
4. 处理并发的配置变更
5. 在每个分片内部保证线性一致性

这道题将前面所有的组件组合成一个可运行的完整系统。

## 概念说明

### 整合所有组件

一个分片键值存储系统包含三部分：（1）分片控制器管理配置信息；（2）多个副本组，每个组负责若干分片；（3）客户端根据配置信息将请求路由到正确的副本组。

### 客户端重试

当副本组收到一个不属于自己的分片的请求时，会返回错误。客户端需要刷新配置信息并重试。在重新配置期间，这种重试可能会发生多次。

## 涉及概念

- `sharded storage`
- `routing`
- `end-to-end`

## 实现提示

- 将请求路由到正确的分片
- 处理"错误副本组"的错误响应
- 配置变更时进行重试

## 测试用例

### 1. 路由到正确的分片

代理根据分片分配关系，将请求路由到正确的副本组。

输入：

```json
{"src":"client","dest":"proxy","body":{"type":"init","msg_id":1,"node_id":"proxy","node_ids":["proxy"]}}
{"src":"controller","dest":"proxy","body":{"type":"config","msg_id":2,"version":1,"shards":{"0":"g1","1":"g1","2":"g1","3":"g1","4":"g2","5":"g2"}}}
{"src":"c1","dest":"proxy","body":{"type":"get","msg_id":3,"key":"mykey"}}
```

期望输出：

```text
{"src":"proxy","dest":"client","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"proxy","dest":"controller","body":{"type":"config_ok","in_reply_to":2,"msg_id":1}}
{"src":"proxy","dest":"c1","body":{"type":"get_ok","in_reply_to":3,"msg_id":2,"key":"mykey"}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
