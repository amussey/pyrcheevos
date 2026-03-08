"""High-level Python wrappers for rcheevos ROM hashing."""

from __future__ import annotations

import ctypes
import os
from typing import NamedTuple

from ._lib import _lib, HashIterator, DeprecatedMessageCb
from .consoles import Console


class HashResult(NamedTuple):
    console: Console | int
    hash: str


# Keep a module-level reference so the callback isn't garbage-collected while
# the library might still call it.
_active_verbose_cb: DeprecatedMessageCb | None = None
_active_error_cb: DeprecatedMessageCb | None = None


def _as_console(console_id: int) -> Console | int:
    try:
        return Console(console_id)
    except ValueError:
        return console_id


def _set_verbose(enabled: bool) -> None:
    global _active_verbose_cb, _active_error_cb

    if enabled:
        def _vcb(msg: bytes) -> None:
            print(f"[rcheevos] {msg.decode(errors='replace')}")

        def _ecb(msg: bytes) -> None:
            print(f"[rcheevos ERROR] {msg.decode(errors='replace')}")

        _active_verbose_cb = DeprecatedMessageCb(_vcb)
        _active_error_cb = DeprecatedMessageCb(_ecb)
        _lib.rc_hash_init_verbose_message_callback(_active_verbose_cb)
        _lib.rc_hash_init_error_message_callback(_active_error_cb)
    else:
        # Pass a null-equivalent to clear the global callbacks
        null_cb = ctypes.cast(None, DeprecatedMessageCb)
        _lib.rc_hash_init_verbose_message_callback(null_cb)
        _lib.rc_hash_init_error_message_callback(null_cb)
        _active_verbose_cb = None
        _active_error_cb = None


def hash_file(
    path: str,
    console: Console | int | None = None,
    verbose: bool = False,
) -> list[HashResult]:
    """Hash a ROM file and return a list of :class:`HashResult` instances.

    Parameters
    ----------
    path:
        Path to the ROM file (UTF-8 string).
    console:
        Specific :class:`Console` (or raw integer ID) to hash for.
        When ``None`` (default) the console is auto-detected from the file
        extension and all matching hashes are returned.
    verbose:
        Print diagnostic messages emitted by the rcheevos library to stdout.

    Returns
    -------
    list[HashResult]
        Each entry is a ``(console, hash)`` named tuple.  The list may be
        empty if the file could not be hashed.
    """
    if verbose:
        _set_verbose(True)

    path_bytes = os.fsencode(path) if isinstance(path, str) else path

    results: list[HashResult] = []

    if console is not None:
        console_id = int(console)
        hash_buf = ctypes.create_string_buffer(33)
        iterator = HashIterator()
        _lib.rc_hash_initialize_iterator(
            ctypes.byref(iterator), path_bytes, None, 0
        )
        ok = _lib.rc_hash_generate(hash_buf, console_id, ctypes.byref(iterator))
        _lib.rc_hash_destroy_iterator(ctypes.byref(iterator))
        if ok:
            results.append(HashResult(_as_console(console_id), hash_buf.value.decode()))
    else:
        hash_buf = ctypes.create_string_buffer(33)
        iterator = HashIterator()
        _lib.rc_hash_initialize_iterator(
            ctypes.byref(iterator), path_bytes, None, 0
        )
        while _lib.rc_hash_iterate(hash_buf, ctypes.byref(iterator)):
            # After a successful rc_hash_iterate call, index has already been
            # incremented past the entry that was just used.
            used_idx = iterator.index - 1
            if 0 <= used_idx < 12:
                console_id = iterator.consoles[used_idx]
            else:
                console_id = 0
            results.append(HashResult(_as_console(console_id), hash_buf.value.decode()))
        _lib.rc_hash_destroy_iterator(ctypes.byref(iterator))

    if verbose:
        _set_verbose(False)

    return results
