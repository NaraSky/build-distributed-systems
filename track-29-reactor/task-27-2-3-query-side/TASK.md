# Implement Query Side Optimization

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-3-query-side>

Track: 29. The Reactor
Task order: 8
Short title: Query Side
Difficulty: intermediate
Subtrack: CQRS (Command Query Responsibility Segregation)

## Problem

The query side is the read path in CQRS. Instead of querying the write model directly (which is normalized for writes), it reads from **pre-built read models** (projections) that are denormalized and indexed for the specific query being served. Query results can also be cached to avoid redundant work.

Implement a node that serves three query types:

```json
// Paginated user list from a denormalized listing projection
{ "type": "GetUserListing", "msg_id": 1,
  "params": {"page": 1, "limit": 10} }
-> { "type": "query_result", "in_reply_to": 1,
    "data": [{"id": "user-123", "name": "John Doe"}],
    "cached": false }

// Email lookup via index (second call returns from cache)
{ "type": "GetUserByEmail", "msg_id": 2,
  "params": {"email": "john@example.com"} }
-> { "type": "query_result", "in_reply_to": 2,
    "data": {"email": "john@example.com", "userId": "user-123"},
    "cached": true }

// Filtered query: users in a specific city
{ "type": "GetUsersByCity", "msg_id": 3,
  "params": {"city": "NYC"} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": [{"city": "NYC", "userId": "user-123"}],
    "cached": false }
```

The `cached` field indicates whether the result was served from the query cache. A query handler never modifies any state.

## Concepts

- read model
- query optimization
- caching
- denormalization
- pagination

## Hints

- Read models are denormalized: pre-join and pre-aggregate data for fast reads
- Cache query results with a TTL; return cached=true when the result comes from cache
- GetUserListing uses pagination (page, limit) to return a slice of the users list
- GetUserByEmail uses an email index for O(1) lookup rather than a full scan
- The query side never writes — it reads from projections built by the event side

## Test Cases

### 1. Query user listing

Should return first page of user listing from read model.

Input:

```json
{"src":"client","dest":"queryside","body":{"type":"GetUserListing","msg_id":1,"params":{"page":1,"limit":10}}}
```

Expected output:

```text
{"type": "query_result", "in_reply_to": 1, "data": [{"id": "user-123", "name": "John Doe"}], "cached": false}
```

### 2. Query with cache hit

Email index lookup should return cached=true on repeated query.

Input:

```json
{"src":"client","dest":"queryside","body":{"type":"GetUserByEmail","msg_id":1,"params":{"email":"john@example.com"}}}
```

Expected output:

```text
{"type": "query_result", "in_reply_to": 1, "data": {"email": "john@example.com", "userId": "user-123"}, "cached": true}
```

## Resources

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html): Query side design and read model optimizations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
