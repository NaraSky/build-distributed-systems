"""Regenerate local task docs and starter-code modules from the course site.

This script is intentionally conservative: it only writes inside this repository
and mirrors the current website track/task shape into Maven modules.
"""

from __future__ import annotations

import json
import re
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://builddistributedsystem.com"


def get_json(url: str, retries: int = 6, delay: float = 2.0) -> dict:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code == 429:
                time.sleep(delay * (attempt + 1))
                continue
            raise
        except Exception as exc:
            last = exc
            time.sleep(delay)
    raise RuntimeError(f"Failed to fetch {url}") from last


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read().decode("utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def generic_starter(track_slug: str, task_slug: str, title: str) -> str:
    return f"""// Website: {BASE}/tracks/{track_slug}/tasks/{task_slug}
// Task: {title}
// Java starter code
// Read from stdin, process data, write to stdout
// This is a general template - adapt it to your specific task

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {{
    public static void main(String[] args) {{
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

        try {{
            String line;
            while ((line = reader.readLine()) != null) {{
                System.out.println(line);
            }}
        }} catch (IOException e) {{
            System.err.println("Error reading input: " + e.getMessage());
            System.exit(1);
        }}
    }}
}}
"""


def main() -> None:
    for item in ROOT.iterdir():
        if item.is_dir() and item.name.startswith("track-"):
            shutil.rmtree(item)

    tracks = sorted(get_json(f"{BASE}/api/tracks")["data"]["tracks"], key=lambda t: t["order"])
    summary = []

    for track in tracks:
        order = int(track["order"])
        track_num = f"{order:02d}"
        track_slug = track["slug"]
        track_dir_name = f"track-{track_num}-{track_slug}"
        track_dir = ROOT / track_dir_name
        track_dir.mkdir(parents=True, exist_ok=True)

        html = get_text(f"{BASE}/tracks/{track_slug}")
        task_slugs = sorted(
            set(
                match.group(1).rstrip("\\")
                for match in re.finditer(
                    rf"/tracks/{re.escape(track_slug)}/tasks/([^\"'#?\\ ]+)", html
                )
            )
        )

        task_records = []
        for index, task_slug in enumerate(task_slugs, start=1):
            resp = get_json(f"{BASE}/api/tasks/{task_slug}")
            task = resp["data"]["task"]
            task_order = int(task.get("order") or index)
            title = task.get("title") or task_slug
            starter = task.get("starterCodeJava") or generic_starter(track_slug, task_slug, title)
            header = (
                f"// Website: {BASE}/tracks/{track_slug}/tasks/{task_slug}\n"
                f"// Track {order}: {track['title']}\n"
                f"// Task {task_order}: {title}\n\n"
            )

            task_dir = track_dir / task_slug
            write(task_dir / "src/main/java/Main.java", header + starter.lstrip())

            tests = task.get("testCases") or []
            if tests and tests[0].get("input"):
                write(task_dir / "samples/input.jsonl", tests[0]["input"])
            if tests and tests[0].get("expectedOutput"):
                write(task_dir / "samples/expected.txt", tests[0]["expectedOutput"])

            pom = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.example.distsys</groupId>
        <artifactId>{track_dir_name}</artifactId>
        <version>0.1.0-SNAPSHOT</version>
    </parent>
    <artifactId>{task_slug}</artifactId>
    <name>Track {track_num} Task {task_order} - {task.get("shortTitle") or task_slug}</name>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
        </dependency>
    </dependencies>
</project>
"""
            write(task_dir / "pom.xml", pom)
            task_records.append((task_order, task_slug, title))
            time.sleep(0.2)

        modules = "\n".join(f"        <module>{slug}</module>" for _, slug, _ in task_records)
        track_pom = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.example.distsys</groupId>
        <artifactId>build-distributed-systems-java</artifactId>
        <version>0.1.0-SNAPSHOT</version>
    </parent>
    <artifactId>{track_dir_name}</artifactId>
    <name>Track {track_num} - {track['title']}</name>
    <packaging>pom</packaging>
    <modules>
{modules}
    </modules>
</project>
"""
        write(track_dir / "pom.xml", track_pom)
        summary.append((order, track_dir_name, track["title"], len(task_records)))

    print(json.dumps({"tracks": len(summary), "tasks": sum(item[3] for item in summary)}))


if __name__ == "__main__":
    main()
