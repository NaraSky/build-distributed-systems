# 实现多层 LSM 树

英文标题：Implement a Multi-Level LSM Tree
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-3-multi-level>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：8
短标题：Multi-Level LSM
难度：高级
子主题：LSM 树（Log-Structured Merge Tree）

## 中文导读

本题要求你实现多层级的 LSM 树结构。随着数据增长，将所有 SSTable 放在一个扁平列表中会变得难以管理。多层 LSM 树将 SSTable 组织到不同层级中，每层有不同的特性和大小限制。理解这种分层结构，是掌握 LevelDB、RocksDB 等存储引擎架构的关键。

## 题目说明

当数据不断增长时，将所有 SSTable 放在一个扁平列表中会变得难以管理。多层 LSM 树将 SSTable 组织到不同层级（L0、L1、L2 等），并精心维护各层的不变量。

层级结构如下：
- **L0（特殊层）**：直接接收从 MemTable 刷写来的数据。各 SSTable 的键范围可能重叠。读取时必须检查 L0 中的所有文件。
- **L1、L2 等（有序层）**：同一层内的 SSTable 键范围互不重叠。读取时每层最多只需检查一个 SSTable。
- **大小比例**：每层约为上一层的 10 倍大小。L0：40MB，L1：400MB，L2：4GB，L3：40GB。

多层读取路径：
1. 查 MemTable（最新数据）
2. 查 L0（所有文件，从最新到最旧）
3. 查 L1（通过键范围进行二分查找，最多 1 个文件）
4. 查 L2、L3 等，直到找到或查完所有层

```json
Request:  {"type": "lsm_level_info", "msg_id": 1}
Response: {"type": "lsm_level_info_ok", "in_reply_to": 1, "levels": [
    {"level": 0, "sstables": 4, "total_bytes": 16777216, "sorted": false, "max_bytes": 41943040},
    {"level": 1, "sstables": 5, "total_bytes": 52428800, "sorted": true, "max_bytes": 419430400},
    {"level": 2, "sstables": 10, "total_bytes": 524288000, "sorted": true, "max_bytes": 4194304000}
]}

Request:  {"type": "lsm_read", "msg_id": 2, "key": "user:42"}
Response: {"type": "lsm_read_ok", "in_reply_to": 2, "value": "Alice", "found_at": "L1", "levels_checked": 2}
```

## 涉及概念

- `multi-level LSM`
- `L0`
- `L1`
- `sorted runs`
- `level policy`
- `size ratio`

## 实现提示

- L0 包含未排序的 SSTable（最近刷写的数据）。读取时必须检查 L0 中的所有文件
- L1 及以上层级按键范围排序，同一层内的 SSTable 键范围互不重叠
- 每层大约是上一层的 10 倍大小（大小比例 = 10）
- 读取顺序为：MemTable -> L0（所有文件）-> L1 -> L2 -> ...，直到找到目标键
- 层级选择策略根据大小限制决定对哪一层进行压缩

## 测试用例

### 1. 层级信息展示多层结构

返回的 lsm_level_info_ok 中应显示多个层级。L0 的 sorted 应为 false，L1 及以上层级的 sorted 应为 true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_level_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 读取按层级顺序搜索

返回的 lsm_read_ok 中应包含 found_at（找到的层级）和 levels_checked（检查的层数）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_read","msg_id":2,"key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [LevelDB Implementation Notes](https://github.com/google/leveldb/blob/main/doc/impl.md)：Google LevelDB 的实现细节，详细说明了多层 LSM 结构

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
