# 01 Messenger

The Maelstrom protocol uses one JSON message per line on stdin/stdout.

Important rules:

- Read requests from stdin.
- Write only protocol messages to stdout.
- Write diagnostics to stderr if needed.
- Reply messages swap `src` and `dest`.
- Replies include `body.in_reply_to` with the original `body.msg_id`.
