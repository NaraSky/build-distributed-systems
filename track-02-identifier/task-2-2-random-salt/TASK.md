# Add Random Salt to Prevent Collisions

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-random-salt>

Track: 2. The Identifier
Task order: 2
Short title: Random Salt
Difficulty: beginner
Subtrack: Why Unique IDs Are Hard

## Problem

Your basic ID generator might produce duplicates if called multiple times within the same millisecond. Add a random component or sequence counter to ensure uniqueness even under high load.

Options for enhanced uniqueness:

1. Add a **sequence counter** that resets each millisecond
2. Include **random bytes** in each ID
3. Use a structure similar to **Twitter Snowflake IDs**

Your IDs must be unique across all nodes and all time, even if generate is called millions of times per second.

## Concept Notes

## The Same-Millisecond Problem

High-throughput systems can generate **thousands of IDs per millisecond**. Timestamp alone is not granular enough. You need an additional component.

### Option 1: Sequence Counter

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

### Option 2: Random Salt

```text
def generate():
    timestamp = current_time_ms()
    salt = random_bytes(4)  # 4 billion combinations
    return f"{node_id}-{timestamp}-{salt}"
```

### Snowflake IDs

Twitter invented **Snowflake IDs** for exactly this problem. A 64-bit Snowflake ID contains:

  - **41 bits** - timestamp (69 years)

  - **10 bits** - machine ID (1024 machines)

  - **12 bits** - sequence number (4096 IDs per millisecond)

This allows *4096 unique IDs per millisecond per machine*.

## Concepts

- randomness
- collision prevention
- UUID

## Hints

- Add a random component to each generated ID
- Use a sequence counter for IDs generated in the same millisecond
- Consider combining timestamp, node_id, and random value

## Test Cases

### 1. Generate single ID

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## Resources

- [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID): Wikipedia article on Twitter Snowflake ID format

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
