# SaveKey / AtariVox Allocation List

A community-maintained list of **SaveKey** and **AtariVox** memory allocations used by Atari 2600 games and homebrew.

The goal of this repository is to provide a single, easy-to-maintain reference for developers using persistent storage, and to help avoid different games accidentally using the same memory locations.

## Background

The SaveKey is an aftermarket Atari 2600 device that plugs into joystick port 2 and provides non-volatile storage. AtariVox includes compatible storage functionality.

Games can use this memory for things such as:

- High scores
- Game settings
- Progress and unlocks
- Other persistent game data

Because the available memory is shared across games, developers need to coordinate which addresses or pages they use.

The original allocation list is maintained on AtariAge:

https://atariage.com/atarivox/atarivox_mem_list.html

This repository is intended to make community contributions, corrections, and additions easier to track and review.

## Allocation List

See the allocation list in this repository for the currently known assignments.

Before choosing an address range for a new game, please check the list for existing allocations.

If you are developing a new SaveKey/AtariVox-enabled game, please submit your intended allocation so that other developers can avoid using the same range.

## Contributing

Corrections and additions are welcome.

You can contribute by:

1. Opening an issue with the game name, developer/publisher, and memory range used or requested.
2. Submitting a pull request that updates the allocation list.
3. Providing a link or other reference confirming an existing allocation when possible.

For unreleased projects, allocations may be marked as **reserved** or **WIP**.

Please do not change an allocation already used by a released game unless there is clear evidence that the existing entry is incorrect.

## Purpose of This Repository

This repository exists to make the allocation list easier for the Atari 2600 development community to maintain collaboratively.

GitHub provides:

- A history of every change
- Pull requests for proposed additions
- Issues for discussing uncertain or conflicting allocations
- Multiple maintainers, so updates do not depend on a single person
- A convenient source that can be referenced by developers and documentation

## AtariAge Community

This repository is maintained under **atariage-community** as a community resource.

It is **not an official AtariAge repository** and is not intended to imply ownership of or affiliation with AtariAge.

The `atariage-community` name is simply intended to indicate that the project grew out of discussions within the AtariAge community.

If AtariAge or the original maintainers of the allocation list would prefer a different arrangement, the repository can be renamed or transferred.

## Credits

Thanks to **Albert / AtariAge** for maintaining the original SaveKey/AtariVox memory allocation list, and to the Atari 2600 homebrew community for documenting and coordinating their use of SaveKey-compatible storage.

## License

The allocation data is factual information collected from community sources.

A specific license for repository contributions can be added once the maintainers decide which license is most appropriate.
