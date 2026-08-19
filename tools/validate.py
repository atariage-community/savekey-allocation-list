#!/usr/bin/env python3
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

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
    format_version = int(data.get("format_version", 0))
    total_pages = int(data.get("total_pages", 0))
    page_size = int(data.get("page_size", 0))
    allocations = data.get("allocations", [])

    if format_version != 2:
        ok &= fail(f"format_version must be 2, got {format_version}")
    if page_size != 64:
        ok &= fail(f"page_size must be 64, got {page_size}")
    if total_pages != 512:
        ok &= fail(f"total_pages must be 512, got {total_pages}")

    occupied_addresses = {}
    occupied_pages = set()
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

        urls = item.get("urls", [])
        if not isinstance(urls, list) or not urls:
            if "urls" in item:
                ok &= fail(f"{label}: urls must be a non-empty list")
        else:
            for url in urls:
                parsed_url = urlparse(url) if isinstance(url, str) else None
                if parsed_url is None or parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                    ok &= fail(f"{label}: invalid URL {url!r}")

        verified = item.get("verified")
        if verified is not None:
            if not isinstance(verified, str):
                ok &= fail(f"{label}: verified must be a quoted ISO date in YYYY-MM-DD format")
            else:
                try:
                    if date.fromisoformat(verified).isoformat() != verified:
                        raise ValueError
                except ValueError:
                    ok &= fail(f"{label}: invalid verified date {verified!r}; expected YYYY-MM-DD")

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
            occupied_pages.add(page)

        addresses = item.get("addresses")
        if addresses is None:
            raw_address_ranges = [{"start": start * page_size, "end": (end + 1) * page_size - 1}]
        elif isinstance(addresses, dict):
            raw_address_ranges = [addresses]
        elif isinstance(addresses, list) and addresses:
            raw_address_ranges = addresses
        else:
            ok &= fail(f"{label}: addresses must be a range mapping or a non-empty list of ranges")
            continue

        address_ranges = []
        try:
            for address_range in raw_address_ranges:
                address_ranges.append((as_int(address_range["start"]), as_int(address_range["end"])))
        except Exception as exc:
            ok &= fail(f"{label}: invalid address range: {exc}")
            continue

        range_pages = set()
        valid_ranges = True
        for address_start, address_end in address_ranges:
            if address_start > address_end:
                ok &= fail(f"{label}: start address is greater than end address")
                valid_ranges = False
                continue
            if address_start < start * page_size or address_end > (end + 1) * page_size - 1:
                ok &= fail(
                    f"{label}: address range 0x{address_start:04X}-0x{address_end:04X} "
                    f"falls outside page range 0x{start:03X}-0x{end:03X}"
                )
                valid_ranges = False
                continue
            range_pages.update(range(address_start // page_size, address_end // page_size + 1))

        if not valid_ranges:
            continue
        expected_pages = set(range(start, end + 1))
        if range_pages != expected_pages:
            ok &= fail(f"{label}: address ranges do not cover page range 0x{start:03X}-0x{end:03X}")
            continue

        for address_start, address_end in address_ranges:
            for address in range(address_start, address_end + 1):
                if address in occupied_addresses:
                    ok &= fail(
                        f"overlap at address 0x{address:04X}: {label!r} conflicts with "
                        f"{occupied_addresses[address]!r}"
                    )
                else:
                    occupied_addresses[address] = label

    # Require deterministic ordering to keep PR diffs easy to review.
    starts = [as_int(i["pages"]["start"]) for i in allocations]
    if starts != sorted(starts):
        ok &= fail("allocations are not sorted by starting page")

    if ok:
        print(
            f"OK: {len(allocations)} allocations; "
            f"{len(occupied_pages)} of {total_pages} pages assigned."
        )
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
