# Implement Saga Pattern

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-4-sagas>

Track: 9. The Coordinator
Task order: 4
Short title: Sagas
Difficulty: advanced
Subtrack: Two-Phase Commit

## Problem

Sagas: sequence of local transactions with compensations. On failure, compensate in reverse order.

## Concept Notes

### Sagas

Sagas break transactions into local steps with compensations. No locks held. Eventually consistent.

## Concepts

- saga
- compensation
- eventual consistency

## Hints

- Each step has compensating action
- On failure, run compensations in reverse
- Eventual consistency

## Test Cases

### 1. Execute all steps in sequence

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"saga_execute","msg_id":2,"saga_id":"saga1","steps":[{"name":"reserve_inventory","action":"reserve","compensation":"release"},{"name":"charge_payment","action":"charge","compensation":"refund"},{"name":"ship_order","action":"ship","compensation":"cancel_shipment"}]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"saga_execute_ok","in_reply_to":2,"msg_id":1,"saga_id":"saga1","status":"completed","steps_executed":["reserve_inventory","charge_payment","ship_order"]}}
```

## Resources

- [Saga Pattern](https://microservices.io/patterns/data/saga.html): Microservices saga pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
