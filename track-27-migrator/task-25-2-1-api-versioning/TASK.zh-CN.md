# 实现 API 版本管理

英文标题：Implement API Versioning
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-1-api-versioning>

课程：27. 迁移器：数据与协议演进
任务序号：6
短标题：API Versioning
难度：进阶
子主题：Protocol and API Evolution

## 中文导读

这道题要求你实现一个管理多版本接口的节点。在真实的分布式系统中，接口不可能一成不变，但升级接口又不能让老客户端突然用不了。版本管理就是解决这个问题的标准方案：同时支持多个版本、对即将废弃的版本发出警告、到期后彻底下线。

## 题目说明

接口版本管理（API Versioning）让你可以在不影响现有客户端的前提下迭代接口。你需要同时支持多个版本，通过响应头中的 `Deprecation` 和 `Sunset` 字段警告客户端某个版本即将废弃，并在日落日期到期后返回状态码 410 停止对该版本的服务。

请实现一个路由和管理接口版本的节点：

```json
// 路由到正确的版本处理器
{ "type": "get_users", "msg_id": 1, "version": "v2" }
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v2",
    "users": [{"id":1,"email":"user@example.com","full_name":"John Doe"}] }

// 已废弃的版本：添加警告头
{ "type": "get_users", "msg_id": 2, "version": "v1", "deprecated": true }
-> { "type": "users_response", "in_reply_to": 2,
    "version": "v1",
    "headers": {"Deprecation":"true","Sunset":"2024-12-31"} }

// 通过 Accept 头进行版本协商
{ "type": "get_users", "msg_id": 3 }
headers: { "Accept": "application/vnd.myapi.v2+json" }
-> { "type": "users_response", "in_reply_to": 3,
    "version": "v2", "content_type": "application/vnd.myapi.v2+json" }

// 已日落的版本返回 410 Gone
{ "type": "get_users", "msg_id": 4, "version": "v1", "sunset": true }
-> { "type": "error", "in_reply_to": 4, "status": 410,
    "error": "API version v1.0 has been sunset",
    "current_version": "v2.0" }
```

## 概念说明

版本管理就像给软件接口贴上"版本号标签"。当你要推出新功能或调整数据格式时，创建一个新版本，老版本继续保留一段时间。这就像高速公路改建：新路修好后，老路不会马上拆掉，而是先立个"即将关闭"的牌子，给大家一段过渡时间，到了截止日期才真正关闭。

## 涉及概念

- `API versioning`
- `URL versioning`
- `deprecation headers`
- `content negotiation`
- `sunset`

## 实现提示

- 根据请求中的 version 字段或 Accept 头将请求路由到正确的处理器
- 废弃头：在旧版本的响应中添加 `Deprecation: true` 和 `Sunset: <日期>`
- 内容协商：从 `Accept: application/vnd.myapi.v2+json` 中解析出版本号
- 日落处理：日落日期过后，拒绝请求并返回 410 状态码
- 在提前公告日落日期之前，绝不能直接移除某个版本

## 测试用例

### 1. 路由到正确的接口版本

应路由到 v2 处理器，返回包含 full_name 字段的响应。

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"version":"v2"}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": "v2", "users": [{"id": 1, "email": "user@example.com", "full_name": "John Doe"}]}
```

### 2. 废弃版本的响应头

已废弃的版本应包含 Deprecation 和 Sunset 响应头。

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"version":"v1","deprecated":true}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": "v1", "headers": {"Deprecation": "true", "Sunset": "2024-12-31"}}
```

## 参考资料

- [API Versioning Strategies](https://restfulapi.net/versioning/)：对比了路径版本管理、请求头版本管理和媒体类型版本管理三种方案
- [Semantic Versioning](https://semver.org/)：语义化版本规范

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
