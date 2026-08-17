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

The registry uses **64-byte pages**. Address ranges are derived from the page numbers:

- start address = `page × 64`
- end address = `start address + 63`

This avoids page/address mismatches.

## Adding or changing an allocation

For most developers, the workflow is:

1. Fork this repository to your own GitHub account.
2. Create a branch in your fork.
3. Edit **only `allocations.yaml`**.
4. Commit and push your changes.
5. Open a pull request back to the `main` branch of this repository.

If you already have write access to this repository, you can create a branch directly instead of making a fork.

You **do not need Python installed locally**.

When you submit a pull request, GitHub Actions automatically validates `allocations.yaml`, including checks for invalid or overlapping page ranges.

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
- `notes` — optional additional information
- `source_correction` — optional note documenting normalization/correction of source data

Please keep the schema simple. If a new field seems useful, discuss it in an issue before adding it broadly.

## Validation

Validation is handled automatically by GitHub Actions, so contributors normally do not need to run anything locally.

If you do want to validate the file locally, Python 3 and PyYAML are required:

```sh
python -m pip install -r requirements.txt
python tools/validate.py allocations.yaml
```

`validate.py` checks the allocation data for problems such as invalid ranges and overlapping allocations.

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
