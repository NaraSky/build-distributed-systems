# 添加随机盐值防止 ID 冲突

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-random-salt>

课程：2. 标识符：分布式唯一 ID
任务序号：2
短标题：随机盐值
难度：入门
子主题：为什么唯一 ID 这么难

## 中文导读

上一道题中，同一毫秒内连续调用可能产生重复 ID。这道题要求你在 ID 中加入随机成分或序列计数器，从而在高并发下也能保证唯一性。这是理解"雪花算法（Snowflake）"等工业级方案的基础。

## 题目说明

在上一个基础实现中，如果同一毫秒内多次调用生成函数，可能会产生重复的 ID。你需要添加一个随机成分或序列计数器，确保即使在高负载下也不会出现重复。

增强唯一性的几种方案：

1. 添加一个**序列计数器**，每毫秒重置一次
2. 在每个 ID 中加入**随机字节**
3. 采用类似 **Twitter 雪花 ID（Snowflake ID）** 的结构

你生成的 ID 必须在所有节点、所有时间上都保持唯一，即使每秒被调用数百万次也不能重复。

## 概念说明

### 同一毫秒问题

高吞吐量系统每毫秒可能需要生成**数千个 ID**。仅靠时间戳的精度远远不够，你需要额外的区分手段。

### 方案一：序列计数器

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

就像在同一秒发出的多封信件，可以用"信件 1、信件 2、信件 3"来编号区分。

### 方案二：随机盐值

```text
def generate():
    timestamp = current_time_ms()
    salt = random_bytes(4)  # 4 billion combinations
    return f"{node_id}-{timestamp}-{salt}"
```

4 个随机字节可以产生约 40 亿种组合，在同一毫秒内碰撞的概率极低。

### 雪花 ID

Twitter 发明了**雪花 ID（Snowflake ID）** 来解决这个问题。一个 64 位的雪花 ID 包含：

  - **41 位** - 时间戳（可用约 69 年）

  - **10 位** - 机器 ID（最多 1024 台机器）

  - **12 位** - 序列号（每毫秒最多 4096 个 ID）

这样，每台机器每毫秒可以生成 *4096 个唯一 ID*。

## 涉及概念

- `randomness`
- `collision prevention`
- `UUID`

## 实现提示

- 在每个生成的 ID 中添加随机成分
- 对同一毫秒内生成的 ID 使用序列计数器
- 考虑将时间戳、节点标识和随机值组合起来

## 测试用例

### 1. 生成单个 ID

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

- [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID)：维基百科上关于 Twitter 雪花 ID 格式的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
