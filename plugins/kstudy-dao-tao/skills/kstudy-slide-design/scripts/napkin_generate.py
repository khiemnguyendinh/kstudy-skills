#!/usr/bin/env python3
"""Generate one Napkin visual without exposing the API token."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_BASE = "https://api.napkin.ai/v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--context", default="")
    parser.add_argument("--context-file", type=Path)
    parser.add_argument("--visual-query", default="mindmap")
    parser.add_argument("--language", default="vi-VN")
    parser.add_argument("--orientation", default="horizontal")
    parser.add_argument("--width", type=int, default=1800)
    parser.add_argument("--format", choices=("svg", "png", "ppt"))
    parser.add_argument("--style-id")
    parser.add_argument("--style-env")
    parser.add_argument("--token-file", type=Path, default=Path(".napkin.local"))
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def read_local_token(path: Path) -> str | None:
    if not path.is_file():
        return None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "NAPKIN_API_TOKEN":
            return value.strip().strip("'\"")
    return None


def infer_format(output: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    suffix = output.suffix.lower()
    formats = {".svg": "svg", ".png": "png", ".ppt": "ppt", ".pptx": "ppt"}
    if suffix not in formats:
        raise SystemExit("Cannot infer format; use --format svg, png, or ppt.")
    return formats[suffix]


def request_bytes(
    method: str,
    url: str,
    token: str,
    payload: dict[str, object] | None = None,
    retries: int = 4,
) -> tuple[bytes, dict[str, str]]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    for attempt in range(retries + 1):
        request = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=45) as response:
                return response.read(), dict(response.headers.items())
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:1200]
            if exc.code == 429 or 500 <= exc.code < 600:
                if attempt < retries:
                    retry_after = exc.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else min(2**attempt, 8)
                    time.sleep(delay)
                    continue
            raise SystemExit(f"Napkin API HTTP {exc.code}: {body}") from exc
        except URLError as exc:
            if attempt < retries:
                time.sleep(min(2**attempt, 8))
                continue
            raise SystemExit(f"Napkin API connection failed: {exc.reason}") from exc
    raise SystemExit("Napkin API request failed after retries.")


def json_request(
    method: str,
    url: str,
    token: str,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    body, _ = request_bytes(method, url, token, payload)
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise SystemExit("Napkin API returned invalid JSON.") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("Napkin API returned an unexpected JSON response.")
    return parsed


def main() -> None:
    args = parse_args()
    if args.output.exists() and not args.force and not args.dry_run:
        print(json.dumps({"output": str(args.output), "status": "cached"}))
        return

    content = args.content_file.read_text(encoding="utf-8").strip()
    if not content:
        raise SystemExit("Content file is empty.")
    if len(content.encode("utf-8")) > 100_000:
        raise SystemExit("Content exceeds the Napkin API limit of 100,000 bytes.")
    context = args.context
    if args.context_file:
        context = args.context_file.read_text(encoding="utf-8").strip()

    output_format = infer_format(args.output, args.format)
    style_id = args.style_id
    if not style_id and args.style_env:
        style_id = os.environ.get(args.style_env)

    payload: dict[str, object] = {
        "format": output_format,
        "content": content,
        "language": args.language,
        "visual_query": args.visual_query,
        "transparent_background": True,
        "color_mode": "light",
        "number_of_visuals": 1,
        "width": args.width,
        "orientation": args.orientation,
        "text_extraction_mode": "preserve",
        "sort_strategy": "relevance",
    }
    if context:
        payload["context"] = context
    if style_id:
        payload["style_id"] = style_id

    if args.dry_run:
        summary = {
            "format": output_format,
            "content_bytes": len(content.encode("utf-8")),
            "context_bytes": len(context.encode("utf-8")),
            "visual_query": args.visual_query,
            "orientation": args.orientation,
            "width": args.width,
            "transparent_background": True,
            "style_id_set": bool(style_id),
        }
        print(json.dumps(summary, ensure_ascii=True, indent=2))
        return

    token = os.environ.get("NAPKIN_API_TOKEN") or read_local_token(args.token_file)
    if not token:
        raise SystemExit(
            "NAPKIN_API_TOKEN is missing. Set it in the environment or .napkin.local."
        )

    created = json_request("POST", f"{API_BASE}/visual", token, payload)
    request_id = created.get("id") or created.get("request_id")
    if not isinstance(request_id, str) or not request_id:
        raise SystemExit("Napkin API did not return a request ID.")

    deadline = time.monotonic() + args.timeout
    delay = 2.0
    status: dict[str, object] = created
    while status.get("status") not in ("completed", "failed"):
        if time.monotonic() >= deadline:
            raise SystemExit(f"Napkin request {request_id} timed out.")
        time.sleep(delay)
        status = json_request(
            "GET", f"{API_BASE}/visual/{request_id}/status", token
        )
        delay = min(delay * 1.5, 8.0)

    if status.get("status") == "failed" or status.get("error"):
        raise SystemExit(
            "Napkin generation failed: "
            + json.dumps(status.get("error"), ensure_ascii=True)
        )

    warnings = status.get("warnings") or []
    if isinstance(warnings, list):
        for warning in warnings:
            if isinstance(warning, dict):
                code = warning.get("code", "warning")
                message = warning.get("message", "")
                print(f"Napkin warning [{code}]: {message}", file=sys.stderr)

    files = status.get("generated_files")
    if not isinstance(files, list) or not files or not isinstance(files[0], dict):
        raise SystemExit("Napkin completed without a downloadable file.")
    file_url = files[0].get("url")
    if not isinstance(file_url, str) or not file_url:
        raise SystemExit("Napkin response did not include a file URL.")

    file_bytes, _ = request_bytes("GET", file_url, token)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(file_bytes)

    credits = status.get("credits")
    consumed = credits.get("consumed") if isinstance(credits, dict) else None
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": "completed",
                "request_id": request_id,
                "warnings": warnings,
                "credits_consumed": consumed,
            },
            ensure_ascii=True,
        )
    )


if __name__ == "__main__":
    main()
