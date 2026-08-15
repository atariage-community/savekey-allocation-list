# SaveKey Allocation List

Community-maintained SaveKey/AtariVox memory allocation registry for Atari 2600 and compatible projects.

The goal is to provide one easy-to-review place where developers can reserve persistent-storage pages without accidentally colliding with another game.

> This is a community-maintained project under `atariage-community`. It is not an official AtariAge repository.

## The canonical file

**[`allocations.yaml`](allocations.yaml) is the source of truth.**

[`ALLOCATIONS.md`](ALLOCATIONS.md) is generated from the YAML and provides a convenient table of allocated and currently unallocated ranges.

The registry uses **64-byte pages**. The address range is derived from the page number, so contributors do not have to maintain both values manually:

- start address = `page × 64`
- end address = `start address + 63`

This avoids page/address mismatches.

## Reserving space

1. Check [`ALLOCATIONS.md`](ALLOCATIONS.md) and current open pull requests/issues for conflicts.
2. Add your project to `allocations.yaml`.
3. Set `status: reserved` for a new reservation, or `status: allocated` for an already established allocation.
4. Run the validator.
5. Regenerate `ALLOCATIONS.md`.
6. Submit a pull request.

Example:

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

If you are not comfortable creating a pull request, open an issue with the project name, developer, requested number of pages, and any preferred range. A maintainer can add it for you.

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

## Validate and generate

Requires Python 3 and PyYAML:

```sh
python -m pip install -r requirements.txt
python tools/validate.py allocations.yaml
python tools/generate.py allocations.yaml ALLOCATIONS.md
```

The GitHub Actions workflow runs validation and checks that `ALLOCATIONS.md` has been regenerated.

## Imported source

The initial data was imported from:

https://atariage.com/atarivox/atarivox_mem_list.html

The AtariAge page states that it was last updated **April 14, 2024**.

Contiguous pages belonging to the same assignment have been grouped into a single YAML entry. Two obvious source inconsistencies were normalized during import and are documented in `allocations.yaml` and `ALLOCATIONS.md`.

## Scratchpad

Pages `0x0C0–0x0FF` (`0x3000–0x3FFF`) are designated as non-permanent scratchpad space in the original allocation list. They are represented explicitly and are therefore not shown as available permanent allocations.

## Attribution

Thanks to Albert / AtariAge for maintaining the original SaveKey & AtariVox allocation list, and to the Atari homebrew community for coordinating use of persistent storage.
