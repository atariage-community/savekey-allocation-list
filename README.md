# SaveKey Allocation List

Community-maintained SaveKey/AtariVox memory allocation registry for Atari 2600 and compatible projects.

The goal is to provide one easy-to-review place where developers can reserve persistent-storage pages without accidentally colliding with another game.

> This is a community-maintained project under `atariage-community`. It is not an official AtariAge repository.

## The canonical file

**[`allocations.yaml`](allocations.yaml) is the single source of truth.**

All allocation data is maintained in this file.

For a human-friendly view of the current allocation map, including a visual memory map, search and filtering, see:

https://atariage-community.github.io/savekey-allocation-list/allocations.html

The web interface reads the allocation data directly from `allocations.yaml`, so there is no separate generated allocation list that needs to be kept in sync.

The registry uses **64-byte pages**. By default, address ranges are derived from the page numbers:

- start address = `page × 64`
- end address = `start address + 63`

This avoids page/address mismatches.

A developer is normally assigned a complete 64-byte page. Because a game may
use only part of that page, the assigned developer can document multiple games
on the same page by declaring each game's exact inclusive
`addresses.start` / `addresses.end` range. These byte ranges must not overlap
and must fall within, and cover the same page or pages as, the `pages` range.

## Adding or changing an allocation

For most developers, the workflow is:

1. Fork this repository to your own GitHub account.
2. Create a branch in your fork.
3. Edit **only `allocations.yaml`**.
4. Optionally run the local validator to catch mistakes before pushing:
   ```sh
   python -m pip install -r requirements.txt
   python tools/validate.py allocations.yaml
   ```
5. Commit and push your changes.
6. Open a pull request back to the `main` branch of this repository.

You **do not need Python installed locally** to contribute. GitHub Actions automatically validates every pull request. If you already have Python installed, running the validator locally is optional but recommended. It can catch problems, such as invalid or overlapping page ranges, before you push your changes.

Before choosing a new range, it is still a good idea to check the current allocation map and any open pull requests to see what is already in use or being requested.

Example allocation:

```yaml
  - title: "My New Game"
    developer: "Your Name"
    kind: game
    status: reserved
    pages:
      start: 0x104
      end: 0x105
    notes: "High scores and game settings"
```

Use `status: reserved` when requesting space for a new or unreleased project, and `status: allocated` for an allocation already in use.

If you are not comfortable using Git or creating a pull request, simply open an issue with the project name, developer, requested number of pages, and any preferred range. A maintainer can add it for you.

## Fields

Each allocation supports:

- `title` — game/project name
- `developer` — developer, author, team, or publisher credited by the source
- `platform` — optional; defaults to Atari 2600
- `kind` — `game`, `system`, `scratchpad`, or `utility`
- `status` — `reserved`, `allocated`, or `retired`
- `pages.start` / `pages.end` — inclusive hexadecimal page range
- `addresses.start` / `addresses.end` — optional inclusive hexadecimal byte range for a partial-page allocation
- `notes` — optional additional information
- `source_correction` — optional note documenting normalization/correction of source data

Please keep the schema simple. If a new field seems useful, discuss it in an issue before adding it broadly.

Shared-page allocations are represented as separate entries. For example:

```yaml
  - title: "Small Save"
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

There is intentionally no generated `ALLOCATIONS.md`. The YAML file is the authoritative data source, while the GitHub Pages interface provides the human-readable view.

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