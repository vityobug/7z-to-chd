# 7zip to CHD

Convert game archives and disc images to CHD format with ease!

## Overview

This tool automates converting `.7z` game archives and loose disc images (`.iso`, `.cue`/`.bin`, `.gdi`, `.img`) into `.chd` format using `chdman`. It runs inside Docker, making it fully portable across any system — no dependencies to install, no setup beyond Docker itself.

## Why Docker?

Docker is the primary way to run this tool. Since this project gets used across frequently-switching Linux distros and macOS, a containerized approach means it works identically everywhere without reinstalling dependencies or dealing with package manager differences.
Sorry Windows guys, you're on your own.

Everything runs in the container - Python, `chdman`, `p7zip` - so your host system stays clean.

## Features

- Converts `.7z` archives: extracts them, converts disc images inside, then cleans up
- Converts loose disc images directly: `.iso`, `.cue`/`.bin`, `.gdi`, `.img`
- `.cue` takes priority over `.iso` when both exist for the same title
- Prints conversion progress to the console
- Output `.chd` files land in a single output directory

## Requirements

- [Docker](https://docs.docker.com/get-docker/)

That's it.

## Setup

Clone the repo and build the image:

```bash
git clone https://github.com/vityobug/7z-to-chd.git
cd 7z-to-chd
docker build -t 7ziso-to-chd .
```

## Usage

```bash
docker run --rm \
  -v /path/to/your/games:/input \
  -v /path/to/output:/output \
  7ziso-to-chd
```

Replace `/path/to/your/games` with the folder containing your `.7z` archives or loose disc images, and `/path/to/output` with where you want the `.chd` files saved.

## Compatibility

Tested with PS1, PS2, and Dreamcast games. Works with any platform supported by `chdman`.

## Note

Feel free to redistribute and modify this to suit your needs. Happy gaming!
