# 实现 a Text Analysis Pipeline

英文标题：Implement a Text Analysis Pipeline
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-3-text-analysis>

课程：23. 搜索器：分布式搜索
任务序号：3
短标题：Text Analysis
难度：intermediate
子主题：Document模式l和Mapping

## 中文导读

本题要求你完成 `实现 a Text Analysis Pipeline`。

重点关注：`text analysis`、`tokenizer`、`lowercase filter`、`stemmer`、`stop words`。

建议先按提示逐步实现：Tokenizer: split text on whitespace和punctuation into individual tokens。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Text analysis converts raw text into a sequence of tokens用于indexing. The analysis pipeline determines how text is searched.

**Pipeline stages**:
1. **Tokenizer**: split "分布式系统: A Primer" into ["Distributed", "Systems", "A", "Primer"]
2. **Lowercase filter**: ["distributed", "systems", "a", "primer"]
3. **Stop word filter**: remove "a" -> ["distributed", "systems", "primer"]
4. **Stemmer (Porter algorithm)**: "distributed" -> "distribut", "systems" -> "system" -> ["distribut", "system", "primer"]

The same pipeline is applied at both 索引 time (to build the inverted 索引)和query time (to normalize the search query). This ensures that a search用于"Distribution" matches a document containing "Distributed".

```JSON
请求:  {"type": "analyze", "msg_id": 1, "text": "The Quick Brown Fox Jumps", "analyzer": "standard"}
响应: {"type": "analyze_ok", "in_reply_to": 1, "tokens": [{"token": "quick", "position": 1}, {"token": "brown", "position": 2}, {"token": "fox", "position": 3}, {"token": "jump", "position": 4}]}
```

## 涉及概念

- `text analysis`
- `tokenizer`
- `lowercase filter`
- `stemmer`
- `stop words`

## 实现提示

- Tokenizer: split text on whitespace和punctuation into individual tokens
- Lowercase filter: convert all tokens to lowercase用于case-insensitive search
- Stop word filter: remove common words (the, a, is, and, etc.) that add noise
- Stemmer (Porter): reduce words to their root form (running -> run, distributed -> distribut)
- Chain these into a pipeline: tokenize -> lowercase -> stop words -> stem

## 测试用例

### 1. Standard analyzer tokenizes和lowercases

analyze_ok tokens should include "hello"和"world" (lowercased).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"analyze","msg_id":2,"text":"Hello World","analyzer":"standard"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Stop words are removed

Tokens should not include "the", "is", "on" (stop words).

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

- [Elasticsearch Analysis](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)：Elasticsearch documentation on text analysis和analyzers

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
