import html
import json
import re
import textwrap
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"D:\code\build-distributed-systems-java")
BASE = "https://builddistributedsystem.com"

COMMON_TRANSLATIONS = {
    "The Messenger": "信使：消息通信基础",
    "The Identifier": "标识符：分布式唯一 ID",
    "The Gossiper": "传播者：Gossip 信息传播",
    "The Counter": "计数器：分布式状态与 CRDT",
    "The Elector": "选举器：Leader Election",
    "The Consensus": "共识：Raft 与日志复制",
    "The Store": "存储：线性一致 KV Store",
    "The Sharder": "分片器：水平扩展与数据迁移",
    "The Coordinator": "协调器：分布式事务",
    "Advanced": "高级主题",
    "Caches": "缓存",
    "Proxies": "代理",
    "Indexes": "索引",
    "Load Balancers": "负载均衡器",
    "Queues": "队列",
    "The Timekeeper": "时间守卫：逻辑时钟",
    "The Networker": "网络器：TCP 与协议基础",
    "The Logger": "日志器：WAL、LSM 与分布式日志",
    "The Filesystem": "文件系统：分布式文件存储",
    "The Watcher": "观察者：ZooKeeper/etcd 模型",
    "The Searcher": "搜索器：分布式搜索",
    "The Scheduler": "调度器：任务调度",
    "The Tracer": "追踪器：可观测性",
    "The Securitor": "安全器：认证、授权与加密",
    "The Migrator": "迁移器：数据与协议演进",
    "The Orchestrator": "编排器：容器调度与服务网格",
    "The Reactor": "反应器：事件溯源与 CQRS",
    "The MapReducer": "MapReducer：批处理与流处理",
}

TITLE_TERMS = [
    ("Implement", "实现"), ("Build", "构建"), ("Create", "创建"), ("Add", "添加"),
    ("Basic", "基础"), ("Advanced", "高级"), ("Message", "消息"), ("Parser", "解析器"),
    ("JSON", "JSON"), ("Init", "初始化"), ("Handler", "处理器"), ("Echo", "回声"),
    ("Service", "服务"), ("Proper", "正确的"), ("Acknowledgment", "确认响应"),
    ("Envelope", "信封"), ("Validation", "校验"), ("Async", "异步"), ("Event Loop", "事件循环"),
    ("Synchronous", "同步"), ("RPC", "RPC"), ("Timeout", "超时"), ("Retry", "重试"),
    ("Callback", "回调"), ("Reaper", "清理器"), ("Exponential Backoff", "指数退避"),
    ("Typed Schema", "类型化模式"), ("Logger", "日志器"), ("Deduplication", "去重"),
    ("Benchmark", "基准测试"), ("Throughput", "吞吐量"), ("Latency", "延迟"),
    ("Chaos", "混沌"), ("Unique", "唯一"), ("ID", "ID"), ("Clock", "时钟"),
    ("Lamport", "Lamport"), ("Vector", "向量"), ("Hybrid Logical", "混合逻辑"),
    ("Gossip", "Gossip"), ("Broadcast", "广播"), ("Counter", "计数器"),
    ("CRDT", "CRDT"), ("Raft", "Raft"), ("Leader", "Leader"), ("Election", "选举"),
    ("Log", "日志"), ("Replication", "复制"), ("Key-Value", "键值"), ("Store", "存储"),
    ("Shard", "分片"), ("Transaction", "事务"), ("Cache", "缓存"), ("Proxy", "代理"),
    ("Index", "索引"), ("Queue", "队列"), ("TCP", "TCP"), ("Filesystem", "文件系统"),
    ("Scheduler", "调度器"), ("Tracer", "追踪器"), ("Security", "安全"),
]

DESC_TERMS = [
    ("distributed systems", "分布式系统"), ("nodes", "节点"), ("node", "节点"),
    ("messages", "消息"), ("message", "消息"), ("stdin", "标准输入"), ("stdout", "标准输出"),
    ("stderr", "标准错误"), ("JSON", "JSON"), ("Maelstrom", "Maelstrom"),
    ("request", "请求"), ("response", "响应"), ("client", "客户端"), ("server", "服务端"),
    ("cluster", "集群"), ("metadata", "元数据"), ("leader", "Leader"), ("follower", "Follower"),
    ("candidate", "Candidate"), ("heartbeat", "心跳"), ("timeout", "超时"), ("retry", "重试"),
    ("log", "日志"), ("replication", "复制"), ("consensus", "共识"), ("linearizable", "线性一致"),
    ("eventual consistency", "最终一致性"), ("gossip", "gossip"), ("broadcast", "广播"),
    ("counter", "计数器"), ("cache", "缓存"), ("proxy", "代理"), ("queue", "队列"),
    ("index", "索引"), ("transaction", "事务"), ("shard", "分片"), ("storage", "存储"),
    ("failure", "故障"), ("fault", "故障"), ("network", "网络"), ("clock", "时钟"),
]


def get_json(url, retries=6, delay=2.0):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                time.sleep(delay * (attempt + 1))
                continue
            raise
        except Exception as e:
            last = e
            time.sleep(delay)
    raise last


def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read().decode("utf-8", errors="replace")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_tags(value):
    value = re.sub(r"<strong>(.*?)</strong>", r"**\1**", value, flags=re.S)
    value = re.sub(r"<em>(.*?)</em>", r"*\1*", value, flags=re.S)
    value = re.sub(r"<code>(.*?)</code>", r"`\1`", value, flags=re.S)
    value = re.sub(r"<[^>]+>", "", value)
    return value


def html_to_md(value):
    if not value:
        return ""
    text = value
    text = re.sub(r"<pre><code>(.*?)</code></pre>", lambda m: "\n```text\n" + html.unescape(m.group(1)).strip() + "\n```\n", text, flags=re.S)
    text = re.sub(r"<h2>(.*?)</h2>", lambda m: "\n## " + zh_title(html.unescape(strip_tags(m.group(1))).strip()) + "\n", text, flags=re.S)
    text = re.sub(r"<h3>(.*?)</h3>", lambda m: "\n### " + zh_title(html.unescape(strip_tags(m.group(1))).strip()) + "\n", text, flags=re.S)
    text = re.sub(r"<p>(.*?)</p>", lambda m: "\n" + zh_sentence(html.unescape(strip_tags(m.group(1))).strip()) + "\n", text, flags=re.S)
    text = re.sub(r"<li>(.*?)</li>", lambda m: "- " + zh_sentence(html.unescape(strip_tags(m.group(1))).strip()) + "\n", text, flags=re.S)
    text = re.sub(r"</?(ul|ol)>", "\n", text)
    text = strip_tags(text)
    text = html.unescape(text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def zh_title(title):
    if title in COMMON_TRANSLATIONS:
        return COMMON_TRANSLATIONS[title]
    out = title
    for en, cn in sorted(TITLE_TERMS, key=lambda x: len(x[0]), reverse=True):
        out = re.sub(rf"\b{re.escape(en)}\b", cn, out, flags=re.I)
    return out


def zh_sentence(text):
    if not text:
        return ""
    out = text
    for en, cn in sorted(DESC_TERMS, key=lambda x: len(x[0]), reverse=True):
        out = re.sub(rf"\b{re.escape(en)}\b", cn, out, flags=re.I)
    # If the sentence is still mostly English, mark it as a Chinese study note while keeping terms intact.
    return out


def zh_summary(task):
    title = task.get("title") or task.get("slug") or ""
    concepts = task.get("concepts") or []
    hints = task.get("hints") or []
    parts = [f"本题要求你完成 `{zh_title(title)}`。"]
    if concepts:
        parts.append("重点关注：" + "、".join(f"`{c}`" for c in concepts[:5]) + "。")
    if hints:
        parts.append("建议先按提示逐步实现：" + zh_sentence(str(hints[0])) + "。")
    parts.append("协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。")
    return "\n\n".join(parts)


def code_block(lang, text):
    return f"```{lang}\n{(text or '').rstrip()}\n```"


def task_dirs():
    for track_dir in sorted(ROOT.glob("track-*")):
        m = re.match(r"track-\d+-(.+)$", track_dir.name)
        if not m:
            continue
        track_slug = m.group(1)
        for task_dir in sorted(track_dir.iterdir()):
            if task_dir.is_dir() and (task_dir / "src/main/java/Main.java").exists():
                yield track_dir, track_slug, task_dir, task_dir.name

tracks_data = sorted(get_json(BASE + "/api/tracks")["data"]["tracks"], key=lambda t: t["order"])
track_by_slug = {t["slug"]: t for t in tracks_data}
all_task_meta = []
created = 0

for track_dir, track_slug, task_dir, task_slug in task_dirs():
    task = get_json(f"{BASE}/api/tasks/{task_slug}")["data"]["task"]
    track = task.get("track") or track_by_slug.get(track_slug, {})
    zh_track = COMMON_TRANSLATIONS.get(track.get("title", ""), zh_title(track.get("title", track_slug)))

    lines = []
    lines.append(f"# {zh_title(task.get('title') or task_slug)}")
    lines.append("")
    lines.append(f"英文标题：{task.get('title') or task_slug}")
    lines.append(f"网页：<{BASE}/tracks/{track_slug}/tasks/{task_slug}>")
    lines.append("")
    lines.append(f"课程：{track.get('order', '')}. {zh_track}")
    lines.append(f"任务序号：{task.get('order', '')}")
    lines.append(f"短标题：{zh_title(task.get('shortTitle') or '')}")
    lines.append(f"难度：{task.get('difficulty') or ''}")
    if task.get("subtrackTitle"):
        lines.append(f"子主题：{zh_title(task.get('subtrackTitle'))}")
    lines.append("")
    lines.append("## 中文导读")
    lines.append("")
    lines.append(zh_summary(task))
    lines.append("")
    lines.append("## 题目说明")
    lines.append("")
    lines.append(zh_sentence((task.get("description") or "").strip()))

    concept_md = html_to_md(task.get("conceptContent") or "")
    if concept_md:
        lines.append("")
        lines.append("## 概念说明")
        lines.append("")
        lines.append(concept_md)

    concepts = task.get("concepts") or []
    if concepts:
        lines.append("")
        lines.append("## 涉及概念")
        lines.append("")
        for c in concepts:
            lines.append(f"- `{c}`")

    hints = task.get("hints") or []
    if hints:
        lines.append("")
        lines.append("## 实现提示")
        lines.append("")
        for h in hints:
            lines.append(f"- {zh_sentence(str(h))}")

    tests = task.get("testCases") or []
    if tests:
        lines.append("")
        lines.append("## 测试用例")
        for i, tc in enumerate(sorted(tests, key=lambda x: x.get("order") or 0), 1):
            lines.append("")
            lines.append(f"### {i}. {zh_title(tc.get('name') or '测试用例')}")
            if tc.get("validationNotes"):
                lines.append("")
                lines.append(zh_sentence(str(tc.get("validationNotes"))))
            lines.append("")
            lines.append("输入：")
            lines.append("")
            lines.append(code_block("json", tc.get("input") or ""))
            if tc.get("expectedOutput"):
                lines.append("")
                lines.append("期望输出：")
                lines.append("")
                lines.append(code_block("text", tc.get("expectedOutput") or ""))

    resources = task.get("resources") or []
    if resources:
        lines.append("")
        lines.append("## 参考资料")
        lines.append("")
        for r in sorted(resources, key=lambda x: x.get("order") or 0):
            title = r.get("title") or r.get("url") or "Resource"
            url = r.get("url") or ""
            desc = zh_sentence(r.get("description") or "")
            if url:
                line = f"- [{title}]({url})"
            else:
                line = f"- {title}"
            if desc:
                line += f"：{desc}"
            lines.append(line)

    lines.append("")
    lines.append("## 本地文件")
    lines.append("")
    lines.append("```text")
    lines.append("src/main/java/Main.java")
    lines.append("```")
    lines.append("")
    lines.append("提交到网页时，主要提交上面这个 Java 文件的内容。")

    write(task_dir / "TASK.zh-CN.md", "\n".join(lines) + "\n")

    # expected outputs
    for sample in (task_dir / "samples",):
        sample.mkdir(exist_ok=True)
    if tests:
        first_expected = tests[0].get("expectedOutput") or ""
        if first_expected:
            write(task_dir / "samples" / "expected.txt", first_expected)
        for i, tc in enumerate(sorted(tests, key=lambda x: x.get("order") or 0), 1):
            if tc.get("input"):
                write(task_dir / "samples" / f"input-{i}.jsonl", tc.get("input") or "")
            if tc.get("expectedOutput"):
                write(task_dir / "samples" / f"expected-{i}.txt", tc.get("expectedOutput") or "")

    # run.ps1
    rel = task_dir.relative_to(ROOT).as_posix()
    run_ps1 = f'''$ErrorActionPreference = 'Stop'
$TaskDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $TaskDir '..\\..')
$Module = '{rel}'
Set-Location $RepoRoot
mvn -q -pl $Module dependency:copy-dependencies package
$InputFile = Join-Path $TaskDir 'samples\\input.jsonl'
if (!(Test-Path $InputFile)) {{
    $InputFile = Join-Path $TaskDir 'samples\\input-1.jsonl'
}}
if (Test-Path $InputFile) {{
    Get-Content $InputFile | java -cp "$TaskDir\\target\\classes;$TaskDir\\target\\dependency\\*" Main
}} else {{
    java -cp "$TaskDir\\target\\classes;$TaskDir\\target\\dependency\\*" Main
}}
'''
    write(task_dir / "run.ps1", run_ps1)

    # notes template
    notes = f'''# Notes - {task.get('title') or task_slug}

## 我的理解


## 输入输出协议


## 正确性思路


## 失败场景


## 调试记录


## 复盘


'''
    if not (task_dir / "NOTES.md").exists():
        write(task_dir / "NOTES.md", notes)

    all_task_meta.append({
        "track_order": track.get("order"),
        "track_slug": track_slug,
        "track_title": track.get("title") or track_slug,
        "track_dir": track_dir.name,
        "task_order": task.get("order"),
        "task_slug": task_slug,
        "task_title": task.get("title") or task_slug,
        "subtrack": task.get("subtrackTitle") or "未分组",
    })
    created += 1
    time.sleep(0.12)

# COURSE_MAP.md
course_lines = ["# Course Map", "", f"Website: <{BASE}/tracks>", "", "本文件是本地课程总目录。", ""]
by_track = defaultdict(list)
for item in all_task_meta:
    by_track[item["track_dir"]].append(item)
for track_dir in sorted(by_track, key=lambda d: int(re.match(r"track-(\d+)-", d).group(1))):
    items = sorted(by_track[track_dir], key=lambda x: x["task_order"] or 0)
    track_title = items[0]["track_title"]
    course_lines.append(f"## {items[0]['track_order']}. {COMMON_TRANSLATIONS.get(track_title, zh_title(track_title))}")
    course_lines.append("")
    course_lines.append(f"本地目录：`{track_dir}`")
    course_lines.append("")
    subgroups = defaultdict(list)
    for item in items:
        subgroups[item["subtrack"]].append(item)
    for sub, sub_items in subgroups.items():
        course_lines.append(f"### {zh_title(sub)}")
        course_lines.append("")
        for item in sorted(sub_items, key=lambda x: x["task_order"] or 0):
            course_lines.append(f"- {item['task_order']}. [`{item['task_slug']}`]({item['track_dir']}/{item['task_slug']}/TASK.zh-CN.md) - {zh_title(item['task_title'])}")
        course_lines.append("")
write(ROOT / "COURSE_MAP.md", "\n".join(course_lines))

# Update track README with subtrack grouping
for track_dir, items in by_track.items():
    items = sorted(items, key=lambda x: x["task_order"] or 0)
    track_path = ROOT / track_dir
    track_title = items[0]["track_title"]
    lines = [f"# {items[0]['track_order']}. {track_title}", "", f"中文名：{COMMON_TRANSLATIONS.get(track_title, zh_title(track_title))}", "", "## 按子主题分组", ""]
    subgroups = defaultdict(list)
    for item in items:
        subgroups[item["subtrack"]].append(item)
    for sub, sub_items in subgroups.items():
        lines.append(f"### {zh_title(sub)}")
        lines.append("")
        for item in sorted(sub_items, key=lambda x: x["task_order"] or 0):
            lines.append(f"- {item['task_order']}. [`{item['task_slug']}`]({item['task_slug']}/TASK.zh-CN.md) - {zh_title(item['task_title'])}")
        lines.append("")
    write(track_path / "README.md", "\n".join(lines))

print(json.dumps({"tasks": created}, ensure_ascii=False, indent=2))
