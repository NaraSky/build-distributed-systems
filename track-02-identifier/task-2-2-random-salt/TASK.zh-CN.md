# 添加随机Salt to Prevent Collisions

英文标题：Add随机Salt to Prevent Collisions
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-random-salt>

课程：2. 标识符：分布式唯一 ID
任务序号：2
短标题：Random Salt
难度：beginner
子主题：Why 唯一 IDs Are Hard

## 中文导读

本题要求你完成 `添加随机Salt to Prevent Collisions`。

重点关注：`randomness`、`collision prevention`、`UUID`。

建议先按提示逐步实现：Add a random component to each generated ID。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Your basic ID generator might produce duplicates if called multiple times within the same millisecond. Add a random component or sequence 计数器 to ensure uniqueness even under high load.

Options用于enhanced uniqueness:

1. Add a **sequence 计数器** that resets each millisecond
2. Include **random bytes** in each ID
3. Use a structure similar to **Twitter Snowflake IDs**

Your IDs must be unique across all 节点和all time, even if generate is called millions of times per second.

## 概念说明

## The Same-Millisecond Problem

High-throughput systems can generate **thousands of IDs per millisecond**. Timestamp alone is not granular enough. You need an additional component.

### Option 1: Sequence 计数器

```text
class IDGenerator:
    last_timestamp = 0
    sequence = 0
    
    def generate(self):
        timestamp = current_time_ms()
        
        if timestamp == self.last_timestamp:
            self.sequence += 1
        else:
            self.sequence = 0
            self.last_timestamp = timestamp
        
        return f"{node_id}-{timestamp}-{sequence}"
```

### Option 2:随机Salt

```text
def generate():
    timestamp = current_time_ms()
    salt = random_bytes(4)  # 4 billion combinations
    return f"{node_id}-{timestamp}-{salt}"
```

### Snowflake IDs

Twitter invented **Snowflake IDs**用于exactly this problem. A 64-bit Snowflake ID contains:

  - **41 bits** - timestamp (69 years)

  - **10 bits** - machine ID (1024 machines)

  - **12 bits** - sequence number (4096 IDs per millisecond)

This allows *4096 unique IDs per millisecond per machine*.

## 涉及概念

- `randomness`
- `collision prevention`
- `UUID`

## 实现提示

- Add a random component to each generated ID
- Use a sequence 计数器用于IDs generated in the same millisecond
- Consider combining timestamp, node_id,和random value

## 测试用例

### 1. Generate single ID

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## 参考资料

- [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID)：Wikipedia article on Twitter Snowflake ID format

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
