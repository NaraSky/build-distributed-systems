# 实现会话粘性

英文标题：Implement Sticky Sessions
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-3-sticky-sessions>

课程：14. 负载均衡器
任务序号：8
短标题：Sticky Sessions
难度：进阶
子主题：七层负载均衡

## 中文导读

本题要求你实现会话粘性（Sticky Sessions）功能。想象你在银行办业务，第一次在 3 号窗口开始填表，中途离开后回来，如果被分到了 5 号窗口，工作人员完全不知道你之前的进度。会话粘性就是为了解决这个问题：确保同一个客户端的所有请求都路由到同一台后端服务器，这样服务器内存中保存的会话状态就不会丢失。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

会话粘性（也叫会话亲和性）确保来自同一客户端的所有请求都路由到同一台后端服务器，这对有状态服务至关重要。

**为什么需要会话粘性**：当客户端在 backend-1 上登录后，会话数据存储在 backend-1 的内存中。如果下一个请求被分配到了 backend-2，由于 backend-2 上没有该用户的会话数据，请求就会失败。有了会话粘性，后续请求会通过 Cookie 中的会话标识，始终被路由到 backend-1。

**会话映射的实现**：维护一个从会话标识到后端服务器的映射表。从请求的 Cookie 中提取会话标识。如果映射表中已有该会话对应的后端，就直接路由过去。如果是新会话或未知会话，则使用负载均衡算法选择后端，并将映射关系存储起来，同时设置 Cookie 以便后续请求使用。

**基于 Cookie 的路由**：负载均衡器从请求 Cookie 中读取会话标识，查找该会话对应的后端服务器，将请求路由过去。如果没有 Cookie 或会话未知，则使用负载均衡算法（轮询、最少连接数等）选择后端。响应中设置包含会话标识和后端信息的 Cookie，客户端后续请求会自动携带该 Cookie。

**会话粘性流程示例**：第一个请求（没有会话 Cookie）：客户端发送请求，负载均衡器通过轮询选择 backend-1，生成会话标识 abc123，存储映射关系 abc123 对应 backend-1，响应中返回 Set-Cookie。第二个请求（携带会话 Cookie）：客户端发送请求时带上会话 Cookie，负载均衡器查找映射表，找到 backend-1，将请求路由到 backend-1，会话数据存在，请求成功。

**后端故障处理**：当后端故障时，检测哪些后端仍然健康。将故障后端上的会话重新分配到新的健康后端，更新映射关系和 Cookie。通过健康检查监控后端状态，故障后端恢复前暂时移出轮转列表。

**与负载均衡的集成**：会话粘性可以与任何负载均衡算法配合使用。对于新会话（没有 Cookie），使用配置的算法（轮询、最少连接数、IP 哈希等）。对于已有会话（携带 Cookie），跳过负载均衡算法，直接使用之前分配的后端。这样既能均匀分配新会话，又能保持已有会话的亲和性。

**会话过期与清理**：会话在配置的超时时间后过期（例如 30 分钟无活动）。定期清理过期的会话映射以释放内存。跟踪每个会话的最后活跃时间，过期或显式登出时移除会话，防止会话表无限增长。

**实现要点**：可使用一致性哈希来选择后端，以减少后端变更时的会话重新分配。会话映射可存储在分布式缓存中，以支持负载均衡器的水平扩展。注意安全防护，使用 HTTPS、Secure Cookie、SameSite 属性等防止 Cookie 被盗用。支持会话排空，以便后端优雅关闭。

**有状态服务的需求**：会话粘性对于在内存中维护会话状态的服务至关重要，比如用户认证、购物车、多步骤工作流等。替代方案包括跨后端的会话复制（实现复杂，存在最终一致性问题）和外部会话存储（如 Redis，会增加额外依赖和网络延迟）。对很多场景而言，会话粘性是最简单有效的方案。

**监控与指标**：跟踪每个后端的会话数，监控会话亲和性违规（请求被路由到错误的后端），衡量会话生命周期（创建、过期、重新分配），在会话分布不均时告警，监控后端健康状况和会话重新分配率。

## 涉及概念

- `sticky sessions`
- `session affinity`
- `cookie-based routing`
- `session persistence`
- `stateful services`

## 实现提示

- 从请求的 Cookie 中提取会话标识
- 维护一个映射表：会话标识对应后端服务器
- 如果会话标识已存在，将请求路由到同一个后端
- 如果没有会话标识，使用正常的负载均衡算法，并设置 Cookie
- 处理后端故障时的会话重新分配

## 测试用例

### 1. 首次请求创建会话

首次请求应返回包含会话标识和后端信息的 Set-Cookie 响应头。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/profile","cookies":{}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "set_cookie": "session_id=.*; backend=api-1"}}
```

### 2. 后续请求使用同一后端

携带 session_id=abc123 的请求应路由到同一后端（api-1）。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/profile","cookies":{"session_id":"abc123"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1"}}
```

## 参考资料

- [Sticky Sessions](https://www.nginx.com/blog/nginx-sticky-sessions-learning-presence/)：关于会话粘性实现方案的详细介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
