"""Console ID constants and lookup helpers."""

from __future__ import annotations

from enum import IntEnum


class Console(IntEnum):
    UNKNOWN = 0
    MEGA_DRIVE = 1
    NINTENDO_64 = 2
    SUPER_NINTENDO = 3
    GAMEBOY = 4
    GAMEBOY_ADVANCE = 5
    GAMEBOY_COLOR = 6
    NINTENDO = 7
    PC_ENGINE = 8
    SEGA_CD = 9
    SEGA_32X = 10
    MASTER_SYSTEM = 11
    PLAYSTATION = 12
    ATARI_LYNX = 13
    NEOGEO_POCKET = 14
    GAME_GEAR = 15
    GAMECUBE = 16
    ATARI_JAGUAR = 17
    NINTENDO_DS = 18
    WII = 19
    WII_U = 20
    PLAYSTATION_2 = 21
    XBOX = 22
    MAGNAVOX_ODYSSEY2 = 23
    POKEMON_MINI = 24
    ATARI_2600 = 25
    MS_DOS = 26
    ARCADE = 27
    VIRTUAL_BOY = 28
    MSX = 29
    COMMODORE_64 = 30
    ZX81 = 31
    ORIC = 32
    SG1000 = 33
    VIC20 = 34
    AMIGA = 35
    ATARI_ST = 36
    AMSTRAD_PC = 37
    APPLE_II = 38
    SATURN = 39
    DREAMCAST = 40
    PSP = 41
    CDI = 42
    _3DO = 43
    COLECOVISION = 44
    INTELLIVISION = 45
    VECTREX = 46
    PC8800 = 47
    PC9800 = 48
    PCFX = 49
    ATARI_5200 = 50
    ATARI_7800 = 51
    X68K = 52
    WONDERSWAN = 53
    CASSETTEVISION = 54
    SUPER_CASSETTEVISION = 55
    NEO_GEO_CD = 56
    FAIRCHILD_CHANNEL_F = 57
    FM_TOWNS = 58
    ZX_SPECTRUM = 59
    GAME_AND_WATCH = 60
    NOKIA_NGAGE = 61
    NINTENDO_3DS = 62
    SUPERVISION = 63
    SHARPX1 = 64
    TIC80 = 65
    THOMSONTO8 = 66
    PC6000 = 67
    PICO = 68
    MEGADUCK = 69
    ZEEBO = 70
    ARDUBOY = 71
    WASM4 = 72
    ARCADIA_2001 = 73
    INTERTON_VC_4000 = 74
    ELEKTOR_TV_GAMES_COMPUTER = 75
    PC_ENGINE_CD = 76
    ATARI_JAGUAR_CD = 77
    NINTENDO_DSI = 78
    TI83 = 79
    UZEBOX = 80
    FAMICOM_DISK_SYSTEM = 81
    HUBS = 100
    EVENTS = 101
    STANDALONE = 102


# Common short aliases -> Console value
_ALIASES: dict[str, Console] = {
    "nes":              Console.NINTENDO,
    "fds":              Console.FAMICOM_DISK_SYSTEM,
    "snes":             Console.SUPER_NINTENDO,
    "n64":              Console.NINTENDO_64,
    "gb":               Console.GAMEBOY,
    "gbc":              Console.GAMEBOY_COLOR,
    "gba":              Console.GAMEBOY_ADVANCE,
    "ds":               Console.NINTENDO_DS,
    "dsi":              Console.NINTENDO_DSI,
    "3ds":              Console.NINTENDO_3DS,
    "genesis":          Console.MEGA_DRIVE,
    "megadrive":        Console.MEGA_DRIVE,
    "sega-genesis":     Console.MEGA_DRIVE,
    "md":               Console.MEGA_DRIVE,
    "sms":              Console.MASTER_SYSTEM,
    "segacd":           Console.SEGA_CD,
    "sega-cd":          Console.SEGA_CD,
    "32x":              Console.SEGA_32X,
    "ps1":              Console.PLAYSTATION,
    "psx":              Console.PLAYSTATION,
    "ps2":              Console.PLAYSTATION_2,
    "psp":              Console.PSP,
    "gc":               Console.GAMECUBE,
    "gamecube":         Console.GAMECUBE,
    "2600":             Console.ATARI_2600,
    "5200":             Console.ATARI_5200,
    "7800":             Console.ATARI_7800,
    "lynx":             Console.ATARI_LYNX,
    "jaguar":           Console.ATARI_JAGUAR,
    "jaguar-cd":        Console.ATARI_JAGUAR_CD,
    "pce":              Console.PC_ENGINE,
    "turbografx":       Console.PC_ENGINE,
    "tg16":             Console.PC_ENGINE,
    "pce-cd":           Console.PC_ENGINE_CD,
    "turbografx-cd":    Console.PC_ENGINE_CD,
    "neogeo-pocket":    Console.NEOGEO_POCKET,
    "neo-geo-cd":       Console.NEO_GEO_CD,
    "dreamcast":        Console.DREAMCAST,
    "saturn":           Console.SATURN,
    "c64":              Console.COMMODORE_64,
    "amiga":            Console.AMIGA,
    "arcade":           Console.ARCADE,
}


def find_console(name: str) -> Console | None:
    """Return a :class:`Console` matching *name* (case-insensitive).

    Accepts short aliases (e.g. ``"nes"``, ``"gba"``), enum member names
    (e.g. ``"NINTENDO"``), and hyphen/underscore-separated variants.
    Returns ``None`` if no match is found.
    """
    key = name.strip().lower().replace(" ", "-")
    if key in _ALIASES:
        return _ALIASES[key]

    # Normalise to underscore-upper for enum lookup
    enum_key = key.replace("-", "_").upper()
    try:
        return Console[enum_key]
    except KeyError:
        pass

    # Also try without leading underscore (e.g. "3DO" stored as "_3DO")
    try:
        return Console["_" + enum_key]
    except KeyError:
        pass

    return None
