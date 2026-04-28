# 实现文本分析流水线

英文标题：Implement a Text Analysis Pipeline
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-3-text-analysis>

课程：23. 搜索引擎
任务序号：3
短标题：文本分析
难度：进阶
子主题：文档模型与映射

## 中文导读

这道题要求你构建一个文本分析流水线（Text Analysis Pipeline），将原始文本转换为可供索引使用的词元序列。文本分析决定了搜索时能匹配到什么内容，是搜索引擎实现"搜得到"的核心环节。

## 题目说明

文本分析（Text Analysis）将原始文本转换为一系列词元（Token），以便建立索引。分析流水线决定了文本被搜索的方式。

**流水线各阶段**：
1. **分词器（Tokenizer）**：将 `"Distributed Systems: A Primer"` 拆分为 `["Distributed", "Systems", "A", "Primer"]`
2. **小写过滤器（Lowercase Filter）**：`["distributed", "systems", "a", "primer"]`
3. **停用词过滤器（Stop Word Filter）**：移除 `"a"` -> `["distributed", "systems", "primer"]`
4. **词干提取器（Stemmer，Porter 算法）**：`"distributed"` -> `"distribut"`，`"systems"` -> `"system"` -> `["distribut", "system", "primer"]`

在索引和查询时都会执行同一套流水线。索引时用它构建倒排索引（Inverted Index），查询时用它规范化搜索词。这样就能确保搜索 `"Distribution"` 时可以匹配到包含 `"Distributed"` 的文档。

```json
Request:  {"type": "analyze", "msg_id": 1, "text": "The Quick Brown Fox Jumps", "analyzer": "standard"}
Response: {"type": "analyze_ok", "in_reply_to": 1, "tokens": [{"token": "quick", "position": 1}, {"token": "brown", "position": 2}, {"token": "fox", "position": 3}, {"token": "jump", "position": 4}]}
```

## 涉及概念

- text analysis
- tokenizer
- lowercase filter
- stemmer
- stop words

## 实现提示

- 分词器：按空格和标点符号将文本拆分为独立的词元
- 小写过滤器：将所有词元转换为小写，实现大小写不敏感搜索
- 停用词过滤器：移除常见的无意义词汇（如 the、a、is、and 等），减少干扰
- 词干提取器（Porter 算法）：将单词还原为词根形式（如 running -> run，distributed -> distribut）
- 将这些步骤串联成流水线：分词 -> 转小写 -> 去停用词 -> 提取词干

## 测试用例

### 1. 标准分析器执行分词和转小写

`analyze_ok` 返回的词元应包含 `"hello"` 和 `"world"`（已转为小写）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"analyze","msg_id":2,"text":"Hello World","analyzer":"standard"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 停用词被正确移除

词元中不应包含 `"the"`、`"is"`、`"on"` 等停用词。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"analyze","msg_id":2,"text":"The cat is on the mat","analyzer":"standard"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Analysis](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)：关于文本分析和分析器的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
