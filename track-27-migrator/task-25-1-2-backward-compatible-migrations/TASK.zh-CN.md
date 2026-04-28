# 实现向后兼容的模式迁移

英文标题：Implement Backward-Compatible Schema Migrations
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-2-backward-compatible-migrations>

课程：27. 迁移器：数据与协议演进
任务序号：2
短标题：Backward-Compatible Migrations
难度：高级
子主题：Schema Migrations

## 中文导读

这道题要求你实现一个支持向后兼容的数据库模式变更节点。想象你要给数据库的列改名，如果直接改，正在运行的旧版应用就会因为找不到旧列名而崩溃。扩展-收缩模式（Expand-Contract Pattern）通过分三步走来解决这个问题，确保新旧应用能同时正常工作。这是零停机部署中非常关键的技术。

## 题目说明

简单的"重命名列"迁移会导致仍在使用旧列名的应用实例崩溃。**扩展-收缩模式（Expand-Contract Pattern）** 可以避免这个问题：先添加新列（新旧两列同时存在），然后回填数据，最后在所有应用实例都更新完毕后再移除旧列。

请实现一个管理向后兼容模式变更的节点，变更分三个阶段进行：

```json
// 第一阶段 - 扩展：添加新列（可为空，旧列保留）
{ "type": "migrate", "msg_id": 1,
  "phase": "expand", "table": "users", "add_column": "full_name" }
-> { "type": "migration_applied", "in_reply_to": 1,
    "version": 1, "name": "add_full_name_column",
    "schema": "users (name, full_name NULL)",
    "backward_compatible": true }

// 第二阶段 - 数据迁移：将 name 的值复制到 full_name
{ "type": "migrate", "msg_id": 2,
  "phase": "migrate_data", "from": "name", "to": "full_name" }
-> { "type": "data_migrated", "in_reply_to": 2,
    "version": 2, "rows_migrated": 1000 }

// 第三阶段 - 收缩：移除旧列（仅在所有应用实例更新后执行）
{ "type": "migrate", "msg_id": 3,
  "phase": "contract", "table": "users", "remove_column": "name" }
-> { "type": "migration_applied", "in_reply_to": 3,
    "version": 3, "name": "remove_name_column",
    "schema": "users (full_name)" }
```

## 涉及概念

- `expand-contract pattern`
- `backward compatibility`
- `rolling deployment`
- `column rename`
- `zero downtime`

## 实现提示

- 扩展阶段：将新列以可为空的方式添加到旧列旁边，使两列同时存在
- 数据迁移阶段：将旧列的值复制或转换到新列
- 收缩阶段：仅在所有应用实例都已切换到新列后，才移除旧列
- 在零停机要求下，绝不能在单次迁移中直接重命名或删除列
- 滚动部署：逐个更新应用实例，每更新一个都要做健康检查

## 测试用例

### 1. 扩展阶段（添加新列）

应添加可为空的 full_name 列，同时保留 name 列，并标记为向后兼容。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1,"phase":"expand","table":"users","add_column":"full_name"}}
```

期望输出：

```text
{"type": "migration_applied", "in_reply_to": 1, "version": 1, "name": "add_full_name_column", "schema": "users (name, full_name NULL)", "backward_compatible": true}
```

### 2. 数据迁移（回填数据）

应将 name 的值复制到 full_name，并报告已迁移的行数。

输入：

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1,"phase":"migrate_data","from":"name","to":"full_name"}}
```

期望输出：

```text
{"type": "data_migrated", "in_reply_to": 1, "version": 2, "rows_migrated": 1000}
```

## 参考资料

- [Expand-Contract Pattern](https://martinfowler.com/bliki/ParallelChange.html)：Martin Fowler 提出的并行变更模式，用于实现零停机迁移

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
