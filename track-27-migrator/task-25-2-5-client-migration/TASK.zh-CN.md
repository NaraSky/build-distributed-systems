# 实现客户端迁移策略

英文标题：Implement Client Migration Strategy
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-5-client-migration>

课程：27. 迁移器：数据与协议演进
任务序号：10
短标题：Client Migration
难度：高级
子主题：Protocol and API Evolution

## 中文导读

这道题要求你实现一个管理客户端跨 API 版本迁移的节点。将客户端从 v1 迁移到 v2 应该是渐进且安全的过程。金丝雀部署（Canary Deployment）先将少量流量导向新版本试水，迁移进度追踪帮你判断何时可以安全下线旧版本。这是大规模系统平滑升级的核心实践。

## 题目说明

将客户端从 API v1 迁移到 v2 应该是渐进且安全的。金丝雀部署从一小部分流量开始试水；A/B 测试根据用户标识确定性地路由特定用户；迁移进度追踪显示何时可以安全地完全下线 v1。

请实现一个管理客户端跨 API 版本迁移的节点：

```json
// 金丝雀比例 10%：大部分流量留在 v1
{ "type": "get_users", "msg_id": 1, "user_id": "user123" }
{ canary_percentage: 10 }
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v1", "canary": false }

// 50/50 流量分割
{ "type": "get_users", "msg_id": 2 }
{ traffic_split: {"v1": 50, "v2": 50} }
-> { "type": "users_response", "in_reply_to": 2,
    "version": "<v1 or v2>" }

// 追踪有多少客户端已完成迁移
{ "type": "get_migration_stats", "msg_id": 3 }
-> { "type": "migration_stats", "in_reply_to": 3,
    "total_clients": 1000,
    "version_percentages": {"v1": 20, "v2": 80},
    "migration_complete": false }

// 分步灰度发布，每步之间进行健康检查
{ "type": "gradual_rollout", "msg_id": 4,
  "steps": [{"percentage":10,"duration_minutes":60},
              {"percentage":50,"duration_minutes":240}] }
-> { "type": "rollout_complete", "in_reply_to": 4,
    "final_percentage": 50, "health_checks_passed": true }
```

## 涉及概念

- `canary deployment`
- `traffic splitting`
- `migration tracking`
- `gradual rollout`
- `health checks`

## 实现提示

- 金丝雀部署：将 10% 的流量路由到 v2（通过 `hash(user_id) % 100 < 10` 判断），其余走 v1
- 流量分割：每个请求生成一个随机数，按百分比区间路由
- 迁移统计：按版本统计一段时间内的请求数量，当 v1 的使用量降为 0 时标记迁移完成
- 分步灰度发布：每一步在检查健康指标后增加 v2 的流量比例
- `health_checks_passed: true` 表示灰度过程中未检测到错误率上升

## 测试用例

### 1. 金丝雀部署路由

在 10% 金丝雀比例下，大多数用户（包括 user123）应留在 v1。

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"user_id":"user123"},"canary_percentage":10}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": "v1", "canary": false}
```

### 2. 流量分割

应按 50/50 分割流量，返回 v1 或 v2。

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1},"traffic_split":{"v1":50,"v2":50}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": ".*"}
```

## 参考资料

- [Canary Release](https://martinfowler.com/bliki/CanaryRelease.html)：通过渐进式流量切换安全地发布 API 变更
- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)：Martin Fowler 关于蓝绿部署的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
