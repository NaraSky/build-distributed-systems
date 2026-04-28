# 实现 Sticky Sessions

英文标题：Implement Sticky Sessions
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-3-sticky-sessions>

课程：14. 负载均衡器
任务序号：8
短标题：Sticky Sessions
难度：intermediate
子主题：Layer 7 Load Balancing

## 中文导读

本题要求你完成 `实现 Sticky Sessions`。

重点关注：`sticky sessions`、`session affinity`、`cookie-based routing`、`session persistence`、`stateful services`。

建议先按提示逐步实现：Extract session_id from 请求 cookies。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Sticky sessions (session affinity) ensure that all requests from a 客户端 are routed to the same backend 服务端, essential用于stateful services.

**Why sticky sessions?**: Problem occurs when 客户端 logs in on backend-1和session is stored in backend-1 memory. 请求 1: GET /login → backend-1 (session created). 请求 2: GET /profile → backend-2 (session not found) - this fails. Solution，包含sticky sessions: 请求 2: GET /profile，包含Cookie: session_id=abc123 → backend-1 (session found) - this works.

**Session mapping implementation**: Maintain Map of session_id to backend. Extract session_id from 请求 cookies. If session_id exists in map, route to known backend用于this session. If no session or unknown session, use load balancing to select backend. Store mapping of session_id to selected backend. Set cookie so future requests use this backend.

**Cookie-based routing**: Load balancer reads session_id from 请求 cookie. Looks up backend assigned to this session. Routes 请求 to that backend. If no cookie or unknown session, selects backend使用load balancing algorithm (round-robin, least connections, etc.). Sets 响应 cookie，包含session_id和backend identifier. 客户端 includes this cookie in all subsequent requests.

**Example sticky session flow**: First 请求 (no session cookie): 客户端 sends GET /api/profile without session cookie. Load balancer selects backend-1使用round-robin. Creates session ID abc123. Stores mapping abc123 → backend-1. Returns 响应，包含Set-Cookie: session_id=abc123; backend=backend-1. Second 请求 (with session cookie): 客户端 sends GET /api/profile，包含Cookie: session_id=abc123. Load balancer looks up abc123 in session map. Finds backend-1. Routes 请求 to backend-1. Session data found, 请求 succeeds.

**Handling backend failures**: When backend fails, detect which backends are healthy. For sessions assigned to failed backend, reassign to new healthy backend. Update session mapping，包含new backend. Update cookie，包含new backend identifier. This ensures session continuity even during failures. Monitor backend health使用health checks. Remove failed backends from rotation until recovery.

**Load balancing integration**: Sticky sessions work，包含any load balancing algorithm. For new sessions (no cookie), use configured algorithm (round-robin, least connections, IP hash, etc.). For existing sessions (with cookie), override load balancing和use assigned backend. This balances new session distribution while maintaining session affinity.

**Session expiration和cleanup**: Sessions expire after configured 超时 (e.g., 30 minutes of inactivity). Clean up expired session mappings to free memory. Track last activity time用于each session. Remove sessions when expired or on explicit logout. This prevents unbounded growth of session table.

**Implementation considerations**: Use consistent hashing用于backend selection to minimize reassignments on backend changes. Store session mapping in distributed 缓存用于load balancer scalability.处理cookie theft和session hijacking，包含security measures (HTTPS, secure cookies, same-site attribute). Support session draining用于graceful backend shutdown.

**Stateful service requirements**: Sticky sessions essential用于services maintaining in-memory session state (user authentication, shopping carts, multi-step workflows). Alternative approaches include session 复制 across backends (complex, 最终一致性 issues) or external session 存储 like Redis (adds dependency, 网络 latency). Sticky sessions provide simple solution用于many use cases.

**Monitoring和metrics**: Track session count per backend. Monitor session affinity violations (requests routed to wrong backend). Measure session lifecycle (creation, expiration, reassignment). Alert on uneven session distribution. Monitor backend health和session reassignment rate.

## 涉及概念

- `sticky sessions`
- `session affinity`
- `cookie-based routing`
- `session persistence`
- `stateful services`

## 实现提示

- Extract session_id from 请求 cookies
- Maintain a mapping: session_id → backend
- If session_id exists, route to the same backend
- If no session_id, use normal load balancing和set the cookie
-处理backend failures: re-assign session to new backend

## 测试用例

### 1. First request creates session

First 请求 should return a Set-Cookie header，包含session_id和backend.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/profile","cookies":{}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "set_cookie": "session_id=.*; backend=api-1"}}
```

### 2. Subsequent requests use same backend

请求，包含session_id=abc123 should route to the same backend (api-1).

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/profile","cookies":{"session_id":"abc123"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1"}}
```

## 参考资料

- [Sticky Sessions](https://www.nginx.com/blog/nginx-sticky-sessions-learning-presence/)：NGINX blog on sticky session implementations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
