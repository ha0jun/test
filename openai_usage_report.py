#!/usr/bin/env python3
"""
Fetch OpenAI organization usage and estimated costs for a date range.

Requires an admin-capable key in OPENAI_ADMIN_KEY (or OPENAI_API_KEY fallback).

Examples:
  python openai_usage_report.py --days 7
  python openai_usage_report.py --start 2026-03-01 --end 2026-03-25
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request

BASE_URL = "https://api.openai.com/v1/organization"


def iso_date(s: str) -> dt.date:
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def to_unix(d: dt.date) -> int:
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp())


def get_json(url: str, api_key: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {e.code} for {url}\n{body}") from e


def fetch_usage(start_ts: int, end_ts: int, api_key: str) -> dict:
    q = urllib.parse.urlencode({"start_time": start_ts, "end_time": end_ts, "bucket_width": "1d"})
    url = f"{BASE_URL}/usage/completions?{q}"
    return get_json(url, api_key)


def fetch_costs(start_ts: int, end_ts: int, api_key: str) -> dict:
    q = urllib.parse.urlencode({"start_time": start_ts, "end_time": end_ts, "bucket_width": "1d"})
    url = f"{BASE_URL}/costs?{q}"
    return get_json(url, api_key)


def main() -> int:
    p = argparse.ArgumentParser(description="OpenAI usage/cost report")
    p.add_argument("--start", help="Start date YYYY-MM-DD (UTC)")
    p.add_argument("--end", help="End date YYYY-MM-DD (UTC, exclusive). Default: tomorrow UTC")
    p.add_argument("--days", type=int, default=7, help="If --start not provided, use trailing N days")
    p.add_argument("--json", action="store_true", help="Print raw JSON")
    args = p.parse_args()

    api_key = os.getenv("OPENAI_ADMIN_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Missing OPENAI_ADMIN_KEY (preferred) or OPENAI_API_KEY", file=sys.stderr)
        return 2

    today = dt.datetime.now(dt.timezone.utc).date()
    if args.start:
        start = iso_date(args.start)
    else:
        start = today - dt.timedelta(days=args.days)

    if args.end:
        end = iso_date(args.end)
    else:
        end = today + dt.timedelta(days=1)

    if end <= start:
        print("end must be after start", file=sys.stderr)
        return 2

    start_ts, end_ts = to_unix(start), to_unix(end)

    usage = fetch_usage(start_ts, end_ts, api_key)
    costs = fetch_costs(start_ts, end_ts, api_key)

    if args.json:
        print(json.dumps({"usage": usage, "costs": costs}, indent=2))
        return 0

    total_input = 0
    total_output = 0
    total_cached_input = 0

    for bucket in usage.get("data", []):
        for r in bucket.get("results", []):
            total_input += int(r.get("input_tokens", 0) or 0)
            total_output += int(r.get("output_tokens", 0) or 0)
            total_cached_input += int(r.get("input_cached_tokens", 0) or 0)

    total_usd = 0.0
    for bucket in costs.get("data", []):
        for r in bucket.get("results", []):
            amt = r.get("amount", {})
            total_usd += float(amt.get("value", 0.0) or 0.0)

    print(f"OpenAI usage report ({start} to {end}, UTC)")
    print("-" * 48)
    print(f"Input tokens:         {total_input:,}")
    print(f"Cached input tokens:  {total_cached_input:,}")
    print(f"Output tokens:        {total_output:,}")
    print(f"Estimated cost (USD): ${total_usd:,.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
