# 实现动态映射与类型自动检测

英文标题：Implement Dynamic Mapping with Type Auto-Detection
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-4-dynamic-mapping>

课程：23. 搜索引擎
任务序号：4
短标题：动态映射
难度：进阶
子主题：文档模型与映射

## 中文导读

这道题要求你实现动态映射（Dynamic Mapping），让系统在索引新文档时自动推断字段类型。这就像给数据库加了"自动建表"的功能，方便但也有风险。理解这些风险（如映射爆炸和类型冲突），是设计健壮搜索系统的关键。

## 题目说明

动态映射（Dynamic Mapping）能在索引新文档时自动检测字段类型。这提供了写入时自动建模的便利性，但也引入了风险。

**自动检测规则**：
- 字符串 -> `text`，并附带一个 `keyword` 子字段
- 整数 -> `long`
- 小数 -> `double`
- 布尔值 -> `boolean`
- 对象 -> `object`（嵌套映射）
- 数组 -> 取第一个元素的类型

**风险**：
1. **映射爆炸（Mapping Explosion）**：如果文档中有成千上万个不同的字段名（比如用户自定义的键），映射会无限膨胀，消耗内存并降低性能。
2. **类型冲突（Type Conflict）**：字段 `"price"` 在文档一中是 `"10"`（字符串），在文档二中是 `10`（整数），后者将无法索引。

```json
Request:  {"type": "doc_index", "msg_id": 1, "index": "logs", "doc": {"message": "error occurred", "level": "ERROR", "status_code": 500, "success": false}}
Response: {"type": "doc_index_ok", "in_reply_to": 1, "_id": "abc", "dynamic_fields_added": [{"name": "message", "type": "text"}, {"name": "level", "type": "text"}, {"name": "status_code", "type": "long"}, {"name": "success", "type": "boolean"}]}
```

## 涉及概念

- dynamic mapping
- type auto-detection
- mapping explosion
- type conflict
- schema-on-read

## 实现提示

- 首次遇到一个字段时，根据它的 JSON 值自动推断类型
- 字符串值默认映射为 `text` 类型，并附带一个 `keyword` 子字段
- 整数（无小数点）默认为 `long`，有小数点的默认为 `double`
- 布尔值映射为 `boolean`，对象则创建嵌套映射
- 风险：当文档包含大量不同的字段名（成千上万个）时，会导致映射爆炸

## 测试用例

### 1. 动态映射自动将字符串识别为文本类型

`mapping_get_ok` 应显示 `"message"` 字段的类型为 `"text"`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"logs","doc":{"message":"hello"}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"logs"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 动态映射将整数识别为长整型

`mapping_get_ok` 应显示 `"count"` 字段的类型为 `"long"`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"metrics","doc":{"count":42}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"metrics"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Dynamic Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-mapping.html)：关于动态映射和类型自动检测的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
