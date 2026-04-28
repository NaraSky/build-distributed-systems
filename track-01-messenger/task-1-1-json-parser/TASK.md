# Implement Basic JSON Message Parser

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-1-json-parser>

Track: 1. The Messenger
Task order: 1
Short title: JSON Parser
Difficulty: beginner
Subtrack: Hello, Distributed World

## Problem

In distributed systems, nodes communicate by exchanging messages. The Maelstrom framework uses JSON messages over stdin/stdout for simplicity and language-agnosticism.

Your task is to implement a basic message parser that reads JSON messages from stdin. Each message has the following structure:

```json
{
  "src": "c1",        // Source node ID
  "dest": "n1",       // Destination node ID
  "body": {           // Message payload
    "type": "...",    // Message type
    "msg_id": 1       // Optional message ID
  }
}
```

Read messages from stdin (one JSON object per line), parse them, and **print the parsed fields to stdout** in the format: `PARSED: src|dest|body_type`. Also log detailed information to stderr for debugging.

Your node should continue reading until stdin is closed.

## Concept Notes

## Message-Based Communication

Distributed systems communicate through **messages** because nodes cannot share memory. This is a fundamental constraint that shapes how we design distributed algorithms.

### Why Messages?

In a single-machine program, threads can share memory directly. But in a distributed system:

  - **Nodes are on different machines** - they have separate memory spaces

  - **Networks are unreliable** - messages can be delayed, duplicated, or lost

  - **Failures are partial** - some nodes may crash while others continue

Each message must be *self-contained* with enough information for the recipient to process it independently.

### The Maelstrom Protocol

Maelstrom uses a simple JSON-based protocol with three required fields:

  - `src` - identifies who sent the message

  - `dest` - identifies the intended recipient

  - `body` - contains the actual payload with a `type` field

### Why stdin/stdout?

Using standard streams makes the protocol **language-agnostic**. Maelstrom can spawn your binary and communicate with it regardless of what language you wrote it in. This same pattern is used by many real systems for inter-process communication (IPC).

### Message Flow Example

```text
Client (c1) --> Node (n1)
{
  "src": "c1",
  "dest": "n1", 
  "body": {"type": "echo", "msg_id": 1, "echo": "hello"}
}

Node (n1) --> Client (c1)
{
  "src": "n1",
  "dest": "c1",
  "body": {"type": "echo_ok", "msg_id": 0, "in_reply_to": 1, "echo": "hello"}
}
```

## Concepts

- JSON parsing
- stdin/stdout
- message format

## Hints

- Read one line at a time from stdin
- Each line is a complete JSON object
- Parse the message and extract src, dest, and body fields
- Print "PARSED: src|dest|body_type" to stdout for validation
- Use .get("type", "unknown") to handle missing type field gracefully

## Test Cases

### 1. Parse single message and extract fields

Must parse JSON and output "PARSED: src|dest|body_type" format. Should extract src=c1, dest=n1, type=echo.

Input:

```json
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":1}}
```

Expected output:

```text
PARSED: c1|n1|echo
```

## Resources

- [Maelstrom Protocol Specification](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md): Official protocol documentation describing message format and semantics
- [Python JSON Module](https://docs.python.org/3/library/json.html): Python standard library documentation for JSON parsing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
