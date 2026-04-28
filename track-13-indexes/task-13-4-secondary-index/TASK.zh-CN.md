# 添加二级索引

英文标题：Add Secondary Indexes
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-4-secondary-index>

课程：13. 索引
任务序号：4
短标题：二级索引
难度：进阶

## 中文导读

这道题要求你实现二级索引（Secondary Index）。主键索引只能按主键查找数据，但在实际应用中，我们经常需要按其他属性查询，例如按邮箱查找用户、按状态查找订单。二级索引为这些非主键属性提供了高效的查找路径，是数据库系统中不可或缺的功能。

## 题目说明

为非主键属性实现二级索引：

1. 主索引：主键 -> 数据
2. 二级索引：属性值 -> 主键列表
3. 按属性查询时：先查二级索引获取主键列表，再通过主索引获取实际数据
4. 在所有写入和删除操作时，同步更新二级索引

二级索引使得可以按任意属性（而不仅仅是主键）进行高效查询。

## 概念说明

### 二级索引

主索引按主键组织数据。但如果你需要按邮箱查找用户，或者按状态查找订单呢？二级索引为这些非主键查询提供了替代的访问路径。打个比方：主索引就像按学号排列的花名册，二级索引就像按姓氏排列的索引页——两种方式都能找到同一个人。

### 实现方式

有三种常见的实现方式：
1. 独立的索引文件，将属性值映射到主键列表
2. 覆盖索引，包含完整记录，避免回查主索引
3. 倒排索引，用于全文搜索

## 涉及概念

- `secondary index`
- `non-key lookup`
- `inverted index`

## 实现提示

- 二级索引将属性值映射到主键列表
- 数据发生变化时同步更新二级索引
- 处理一对多的映射关系

## 测试用例

### 1. 二级索引查找

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"db_insert","msg_id":2,"id":1,"name":"Alice","status":"active"}}
{"src":"c2","dest":"n1","body":{"type":"db_insert","msg_id":3,"id":2,"name":"Bob","status":"active"}}
{"src":"c3","dest":"n1","body":{"type":"db_query","msg_id":4,"field":"status","value":"active"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"db_insert_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"db_insert_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c3","body":{"type":"db_query_ok","in_reply_to":4,"msg_id":3,"results":[1,2]}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
