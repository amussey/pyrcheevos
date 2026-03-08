# pyrcheevos

Python bindings and command-line interface for [rcheevos](https://github.com/RetroAchievements/rcheevos), the C library used to generate ROM hashes for [RetroAchievements](https://retroachievements.org). Games whose hashes match the RetroAchievements database are eligible for achievements.

## Requirements

- Python 3.11 or later
- GCC and zlib development headers (to build the shared library)
- The `rcheevos` source tree cloned into the project root as `rcheevos/`

## Building the shared library

Before using pyrcheevos, compile `librcheevos.so`:

```sh
make
```

The resulting `librcheevos.so` must be present in either the package directory or the project root. pyrcheevos will look in both locations automatically.

## Installation

```sh
pip install -e .
```

## Command-line usage

### Hash a ROM file

Auto-detect the console from the file extension and print all generated hashes:

```
$ pyrcheevos hash Super\ Mario\ Bros.\ \(E\).nes
Super Mario Bros. (E).nes    NINTENDO    4d9abcef768c448d53bc4e43a64e0a45
```

Target a specific console by name or numeric ID:

```
$ pyrcheevos hash --console nes game.nes
$ pyrcheevos hash --console 7 game.nes
```

Hash multiple files at once:

```
$ pyrcheevos hash rom1.sfc rom2.sfc rom3.sfc
```

Print diagnostic output from the rcheevos library:

```
$ pyrcheevos hash --verbose game.nes
[rcheevos] Found 1 potential consoles for nes file extension
[rcheevos] Trying console 7
[rcheevos] Opened game.nes
[rcheevos] Buffering game.nes (40976 bytes)
[rcheevos] Ignoring NES header
[rcheevos] Hashing 40960 byte buffer
[rcheevos] Generated hash 4d9abcef768c448d53bc4e43a64e0a45
game.nes    NINTENDO    4d9abcef768c448d53bc4e43a64e0a45
```

Output is tab-separated: `<path>\t<console>\t<hash>`.

### List supported consoles

```
$ pyrcheevos consoles
  ID  Name
  --  ----
   0  Unknown
   1  Sega Genesis
   2  Nintendo 64
   3  Super Nintendo Entertainment System
   ...
```

### Print the rcheevos library version

```
$ pyrcheevos version
rcheevos 12.3
```

## Python API

### `hash_file`

```python
from pyrcheevos import hash_file, Console

results = hash_file("game.nes")
# [HashResult(console=<Console.NINTENDO: 7>, hash='4d9abcef768c448d53bc4e43a64e0a45')]

for result in results:
    print(result.console, result.hash)
```

Pass a specific `Console` to hash for a single target:

```python
results = hash_file("game.nes", console=Console.NINTENDO)
```

Set `verbose=True` to print rcheevos diagnostic messages to stdout:

```python
results = hash_file("game.nes", verbose=True)
```

`hash_file` returns a list of `HashResult` named tuples, each with two fields:

| Field | Type | Description |
|---|---|---|
| `console` | `Console \| int` | Console the hash was generated for |
| `hash` | `str` | 32-character MD5 hex string |

When no `console` argument is given, the file extension is used to determine candidate consoles and the list may contain more than one entry.

### `Console`

`Console` is an `IntEnum` containing all console IDs defined by rcheevos (80+ systems). It can be used anywhere a raw integer console ID is expected.

```python
from pyrcheevos import Console

print(Console.NINTENDO)          # Console.NINTENDO
print(int(Console.NINTENDO))     # 7
print(Console.SUPER_NINTENDO)    # Console.SUPER_NINTENDO
```

### `find_console`

Looks up a `Console` by name, accepting both canonical enum member names and common aliases:

```python
from pyrcheevos import find_console

find_console("nes")       # Console.NINTENDO
find_console("gba")       # Console.GAMEBOY_ADVANCE
find_console("genesis")   # Console.MEGA_DRIVE
find_console("NINTENDO")  # Console.NINTENDO
find_console("unknown")   # None
```

## Console aliases

In addition to the full enum member names, the following short aliases are recognised by `find_console` and `--console`:

| Alias | Console |
|---|---|
| `nes` | Nintendo Entertainment System |
| `fds` | Famicom Disk System |
| `snes` | Super Nintendo |
| `n64` | Nintendo 64 |
| `gb` | Game Boy |
| `gbc` | Game Boy Color |
| `gba` | Game Boy Advance |
| `ds` | Nintendo DS |
| `3ds` | Nintendo 3DS |
| `genesis` / `md` / `megadrive` | Sega Genesis / Mega Drive |
| `sms` | Master System |
| `segacd` / `sega-cd` | Sega CD |
| `32x` | Sega 32X |
| `ps1` / `psx` | PlayStation |
| `ps2` | PlayStation 2 |
| `psp` | PSP |
| `gc` / `gamecube` | GameCube |
| `pce` / `turbografx` / `tg16` | PC Engine / TurboGrafx-16 |
| `pce-cd` / `turbografx-cd` | PC Engine CD |
| `dreamcast` | Dreamcast |
| `saturn` | Saturn |
| `2600` / `5200` / `7800` | Atari 2600 / 5200 / 7800 |
| `lynx` | Atari Lynx |
| `jaguar` | Atari Jaguar |
| `c64` | Commodore 64 |
| `arcade` | Arcade |

Run `pyrcheevos consoles` for the full list of numeric IDs and names.

## License

pyrcheevos is provided under the MIT License. The bundled rcheevos library is copyright RetroAchievements contributors and is also MIT-licensed - see [`rcheevos/LICENSE`](rcheevos/LICENSE).
