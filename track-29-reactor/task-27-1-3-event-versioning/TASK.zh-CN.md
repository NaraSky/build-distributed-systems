# 实现事件版本控制与迁移

英文标题：Implement Event Versioning and Migration
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-3-event-versioning>

课程：29. 反应器：事件溯源与 CQRS
任务序号：3
短标题：事件版本控制
难度：高级
子主题：Event Sourcing

## 中文导读

本题要求你实现事件的版本控制和迁移功能。随着业务发展，事件的数据结构不可避免地会发生变化，比如新增字段、重命名字段等。但事件是不可变的，不能回去修改旧数据，因此需要一种"向上转换"机制，在读取旧事件时自动将其升级到最新格式。这是事件溯源在生产环境中必须解决的问题。

## 题目说明

随着需求的演进，事件的数据结构（Schema）会发生变化：可能新增了一个字段、重命名了一个字段，或者把一个字段拆分成了两个。由于旧事件是不可变的，你不能直接修改它们。解决办法是使用**向上转换（Upcasting）**：在读取旧版本事件时，将其转换为当前版本的格式。

你需要实现一个通过向上转换来处理事件版本迁移的节点：

```json
// 将单个事件从 v1 升级到 v2
// v1 的 UserCreated 包含: id, name
// v2 的 UserCreated 新增: email（默认值为空字符串）
{ "type": "upcast", "msg_id": 1,
  "event": {"event_type": "UserCreated", "version": 1,
            "event_data": {"id": 1, "name": "John"}},
  "target_version": 2 }
-> { "type": "upcasted", "in_reply_to": 1,
    "event": {"event_type": "UserCreated", "version": 2,
              "event_data": {"id": 1, "name": "John", "email": ""}} }

// 批量迁移事件到目标版本
{ "type": "migrate_batch", "msg_id": 2,
  "events": [
    {"event_type": "UserCreated", "version": 1, "event_data": {"id": 1}}
  ],
  "target_version": 2 }
-> { "type": "migrated", "in_reply_to": 2,
    "count": 1, "target_version": 2 }
```

你的向上转换器必须支持多步迁移（例如 v1 -> v2 -> v3），通过链式调用单步升级来实现。每一步升级都会添加或设置该版本引入的新字段的默认值。

## 概念说明

向上转换可以类比为手机系统升级：你的旧版手机系统可能没有某个功能的设置项，升级到新版本时，系统会自动为这些新功能填入默认设置。事件版本控制的思路完全一样：旧事件缺少的字段，在读取时自动补上默认值。

## 涉及概念

- `event versioning`
- `schema evolution`
- `upcasting`
- `backward compatibility`
- `migration`

## 实现提示

- 向上转换在读取时将旧版本事件就地转换为目标版本
- 从 v1 升级到 v2 时，为缺失的字段填入合理的默认值（空字符串、0 等）
- 批量迁移遍历事件数组，逐个执行向上转换
- 批量迁移响应中的计数值是已处理的事件总数
- 已经处于目标版本的事件应原样返回，不做修改

## 测试用例

### 1. 向上转换事件到新版本

从 v1 升级到 v2 时，应为缺失的 email 字段添加默认空字符串。

输入：

```json
{"src":"migrator","dest":"eventstore","body":{"type":"upcast","msg_id":1,"event":{"event_type":"UserCreated","version":1,"event_data":{"id":1,"name":"John"}},"target_version":2}}
```

期望输出：

```text
{"type": "upcasted", "in_reply_to": 1, "event": {"event_type": "UserCreated", "version": 2, "event_data": {"id": 1, "name": "John", "email": ""}}}
```

### 2. 批量迁移事件

应迁移所有事件并返回处理数量。

输入：

```json
{"src":"migrator","dest":"eventstore","body":{"type":"migrate_batch","msg_id":1,"events":[{"event_type":"UserCreated","version":1,"event_data":{"id":1}}],"target_version":2}}
```

期望输出：

```text
{"type": "migrated", "in_reply_to": 1, "count": 1, "target_version": 2}
```

## 参考资料

- [Event Versioning Patterns](https://leanpub.com/esversioning/read)：Greg Young 关于事件溯源系统中事件版本控制的指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
