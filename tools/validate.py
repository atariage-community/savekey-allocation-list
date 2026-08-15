#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml

ALLOWED_STATUS = {"reserved", "allocated", "retired"}
ALLOWED_KIND = {"game", "system", "scratchpad", "utility"}

def as_int(value):
    if isinstance(value, int):
        return value
    return int(str(value), 0)

def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return False

def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "allocations.yaml")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    ok = True
    total_pages = int(data.get("total_pages", 0))
    page_size = int(data.get("page_size", 0))
    allocations = data.get("allocations", [])

    if page_size != 64:
        ok &= fail(f"page_size must be 64, got {page_size}")
    if total_pages != 512:
        ok &= fail(f"total_pages must be 512, got {total_pages}")

    occupied = {}
    for index, item in enumerate(allocations, start=1):
        label = item.get("title", f"entry #{index}")
        if not item.get("title"):
            ok &= fail(f"entry #{index}: missing title")

        status = item.get("status")
        if status not in ALLOWED_STATUS:
            ok &= fail(f"{label}: invalid status {status!r}; expected one of {sorted(ALLOWED_STATUS)}")

        kind = item.get("kind")
        if kind not in ALLOWED_KIND:
            ok &= fail(f"{label}: invalid kind {kind!r}; expected one of {sorted(ALLOWED_KIND)}")

        try:
            start = as_int(item["pages"]["start"])
            end = as_int(item["pages"]["end"])
        except Exception as exc:
            ok &= fail(f"{label}: invalid page range: {exc}")
            continue

        if start < 0 or end < 0 or start >= total_pages or end >= total_pages:
            ok &= fail(f"{label}: page range 0x{start:X}-0x{end:X} outside 0x000-0x{total_pages-1:03X}")
            continue
        if start > end:
            ok &= fail(f"{label}: start page is greater than end page")
            continue

        for page in range(start, end + 1):
            if page in occupied:
                ok &= fail(
                    f"overlap on page 0x{page:03X}: {label!r} conflicts with {occupied[page]!r}"
                )
            else:
                occupied[page] = label

    # Require deterministic ordering to keep PR diffs easy to review.
    starts = [as_int(i["pages"]["start"]) for i in allocations]
    if starts != sorted(starts):
        ok &= fail("allocations are not sorted by starting page")

    if ok:
        print(f"OK: {len(allocations)} allocations; {len(occupied)} of {total_pages} pages assigned.")
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
