"""Command-line interface for pyrcheevos."""

from __future__ import annotations

import argparse
import sys

from ._lib import _lib
from .consoles import Console, find_console
from .hash import hash_file


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def _cmd_hash(args: argparse.Namespace) -> int:
    console: Console | int | None = None

    if args.console:
        result = find_console(args.console)
        if result is None:
            # Try raw integer
            try:
                console = int(args.console)
            except ValueError:
                print(
                    f"error: unknown console '{args.console}'. "
                    "Use 'pyrcheevos consoles' to list valid names.",
                    file=sys.stderr,
                )
                return 1
        else:
            console = result

    any_hashed = False
    for rom_path in args.rom:
        results = hash_file(rom_path, console=console, verbose=args.verbose)
        if not results:
            print(f"warning: no hash generated for '{rom_path}'", file=sys.stderr)
            continue
        any_hashed = True
        for hr in results:
            c = hr.console
            if isinstance(c, Console):
                console_name = c.name
            else:
                raw = _lib.rc_console_name(int(c))
                console_name = raw.decode() if raw else f"console:{c}"
            print(f"{rom_path}\t{console_name}\t{hr.hash}")

    return 0 if any_hashed else 1


def _cmd_consoles(_args: argparse.Namespace) -> int:
    print(f"{'ID':>4}  {'Name'}")
    print(f"{'--':>4}  {'----'}")
    for c in Console:
        raw = _lib.rc_console_name(int(c))
        name = raw.decode() if raw else c.name
        print(f"{int(c):>4}  {name}")
    return 0


def _cmd_version(_args: argparse.Namespace) -> int:
    raw = _lib.rc_version_string()
    version = raw.decode() if raw else "unknown"
    print(f"rcheevos {version}")
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyrcheevos",
        description="Hash ROM files for use with RetroAchievements.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # hash
    p_hash = sub.add_parser(
        "hash",
        help="Generate a RetroAchievements hash for one or more ROM files.",
    )
    p_hash.add_argument(
        "rom",
        nargs="+",
        metavar="ROM",
        help="Path(s) to ROM file(s).",
    )
    p_hash.add_argument(
        "--console", "-c",
        metavar="CONSOLE",
        default=None,
        help=(
            "Console name or ID to hash for (e.g. 'nes', 'snes', 'gba', '7'). "
            "When omitted the console is auto-detected from the file extension."
        ),
    )
    p_hash.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print diagnostic messages from the rcheevos library.",
    )

    # consoles
    sub.add_parser(
        "consoles",
        help="List all supported console names and their numeric IDs.",
    )

    # version
    sub.add_parser(
        "version",
        help="Print the rcheevos library version.",
    )

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "hash":
        return _cmd_hash(args)
    elif args.command == "consoles":
        return _cmd_consoles(args)
    elif args.command == "version":
        return _cmd_version(args)
    else:
        parser.print_help()
        return 0
