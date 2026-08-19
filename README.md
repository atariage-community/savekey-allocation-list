# SaveKey Allocation List

Community-maintained SaveKey/AtariVox memory allocation registry for Atari 2600 and compatible projects. Use it to reserve persistent-storage pages without colliding with other projects.

> This is a community-maintained project under `atariage-community`. It is not an official AtariAge repository.

## The canonical file

**[`allocations.yaml`](allocations.yaml) is the single source of truth.**

For a human-friendly view that reads `allocations.yaml` directly and provides a visual memory map, search and filtering, see:

https://atariage-community.github.io/savekey-allocation-list/allocations.html

The registry uses **64-byte pages**. By default, address ranges are derived from the page numbers:

- start address = `page × 64`
- end address = `start address + 63`

This avoids page/address mismatches.

A developer is normally assigned a complete 64-byte page. Because a game may
use only part of that page, the assigned developer can document multiple games
on the same page by declaring each game's exact inclusive
`addresses.start` / `addresses.end` range. A game with discontiguous storage can
declare `addresses` as a list of these ranges. Address ranges must not overlap
and must fall within, and cover the same page or pages as, the `pages` range.

## Adding or changing an allocation

To add or change an allocation:

1. Fork this repository to your own GitHub account.
2. Create a branch in your fork.
3. Edit **only `allocations.yaml`**.
4. Optionally run the local validator to catch mistakes before pushing:
   ```sh
   python -m pip install -r requirements.txt
   python tools/validate.py allocations.yaml
   ```
5. Commit, push, and open a pull request against this repository's `main` branch.

GitHub Actions validates every pull request. Local validation is optional, but can catch invalid or overlapping ranges before you push.

Before choosing a new range, it is still a good idea to check the current allocation map and any open pull requests to see what is already in use or being requested.

Example allocation:

```yaml
  - title: "My New Game"
    developer: "Your Name"
    kind: game
    status: reserved
    pages:
      start: 0x104
      end: 0x104
    urls:
      - "https://example.com/my-new-game"
    verified: "2026-08-17"
    notes: "High scores and game settings"
```

Use `status: reserved` when requesting space for a project that has not had a qualifying release. Change it to `status: allocated` when either a cartridge release or a released ROM actually uses the allotted SaveKey/AtariVox page. A released ROM may be played from a multi-ROM cartridge; the important criterion is that the released software uses the allotted page.

Use `status: abandoned` only when the project never had a qualifying cartridge or ROM release and there is clear evidence that the developer has abandoned it. An abandoned entry continues to protect its pages from reuse until maintainers explicitly free or reassign them. To make the pages available again, remove the abandoned entry; the viewer will then show them as available for future allocations.

If you are not comfortable using Git or creating a pull request, simply open an issue with the project name, developer, requested number of pages, and any preferred range. A maintainer can add it for you.

## Fields

Each allocation supports:

- `title` — game/project name
- `developer` — developer, author, team, or publisher credited by the source
- `platform` — optional; defaults to Atari 2600
- `kind` — `game`, `system`, `scratchpad`, or `utility`
- `status` — `reserved` before a qualifying release, `allocated` after released software uses the allotted page, or `abandoned` when an unreleased project is clearly discontinued
- `pages.start` / `pages.end` — inclusive hexadecimal page range
- `addresses` — optional inclusive hexadecimal byte range, or list of ranges, for a partial-page or discontiguous allocation
- `urls` — optional list of source URLs that verify the allocation or project status
- `verified` — optional date on which the sources were verified, quoted in ISO `YYYY-MM-DD` format
- `notes` — optional commentary that is not represented by another field

Please keep the schema simple. If a new field seems useful, discuss it in an issue before adding it broadly.

Shared-page allocations are represented as separate entries. For example:

```yaml
  - title: "My Other Game"
    developer: "Your Name"
    kind: game
    status: allocated
    pages:
      start: 0x023
      end: 0x023
    addresses:
      start: 0x08C0
      end: 0x08C2
```

Omit `addresses` when the allocation reserves complete pages.

Use a list when one game has multiple discontiguous ranges:

```yaml
    addresses:
      - start: 0x0600
        end: 0x0617
      - start: 0x061E
        end: 0x0626
```

## Validation

Validation is handled automatically by GitHub Actions for every pull request.

If you want to validate your changes locally before pushing, Python 3 and PyYAML are required:

```sh
python -m pip install -r requirements.txt
python tools/validate.py allocations.yaml
```

`validate.py` checks the allocation data for problems such as invalid ranges and overlapping byte allocations.

## Repository structure

The important parts of the repository are:

```text
allocations.yaml              # canonical allocation data
docs/
  allocations.html            # public web interface
tools/
  validate.py                 # allocation validator
.github/workflows/
  validate.yml                # automatic validation for pull requests
```

## Imported source

The initial data was imported from:

https://atariage.com/atarivox/atarivox_mem_list.html

The AtariAge page states that it was last updated **April 14, 2024**.

Contiguous pages belonging to the same assignment have been grouped into a single YAML entry. Two obvious source inconsistencies were normalized during import and are documented in `allocations.yaml`.

## Scratchpad

Pages `0x0C0–0x0FF` (`0x3000–0x3FFF`) are designated as non-permanent scratchpad space in the original allocation list. They are represented explicitly and are therefore not shown as available permanent allocations.

## Attribution

Thanks to Albert / AtariAge for maintaining the original SaveKey & AtariVox allocation list, and to the Atari homebrew community for coordinating use of persistent storage.

Special thanks to RevEng for creating the web-based allocation viewer used by this project.