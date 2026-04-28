# Add Message Envelope Validation

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-4-envelope-validation>

Track: 1. The Messenger
Task order: 4
Short title: Envelope Validation
Difficulty: beginner
Subtrack: Hello, Distributed World

## Problem

Production systems must handle malformed input gracefully. Your node should validate that incoming messages have the required structure before processing.

Required validations:

1. Message must be valid JSON
2. Message must have `src`, `dest`, and `body` fields
3. Body must have a `type` field
4. For requests expecting responses, body should have a `msg_id`

If validation fails, log an error to stderr but do not crash. This defensive programming prevents a single bad message from taking down your node.

## Concept Notes

## Defensive Programming

In distributed systems, you **cannot trust the network or other nodes**. Messages may be corrupted, truncated, or malformed. Your node must validate inputs and fail gracefully.

### Why Validation Matters

Consider what happens without validation:

  - **Crashes** - accessing missing fields throws exceptions

  - **Security vulnerabilities** - malformed input could be exploited

  - **Cascading failures** - one bad message takes down the node

### Validation Strategy

A good validation strategy checks inputs at the **boundary** of your system:

```text
def validate_message(msg):
    # Check structure
    if not isinstance(msg, dict):
        return False, "Message must be an object"
    
    # Check required fields
    for field in ["src", "dest", "body"]:
        if field not in msg:
            return False, f"Missing field: {field}"
    
    # Check body structure
    if "type" not in msg["body"]:
        return False, "Body missing type field"
    
    return True, None
```

### Error Semantics

Maelstrom defines error responses with type `error` and error codes:

```text
{
  "type": "error",
  "in_reply_to": 1,
  "code": 10,
  "text": "Node not initialized"
}
```

Common error codes:

  - `0` - timeout

  - `1` - node not found

  - `10` - not supported

  - `11` - temporarily unavailable

  - `12` - malformed request

## Concepts

- validation
- error handling
- defensive programming

## Hints

- Check that required fields are present
- Handle malformed JSON gracefully
- Log validation errors to stderr

## Test Cases

### 1. Handle valid message

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Maelstrom Error Codes](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md#errors): Reference for error response format and codes

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
