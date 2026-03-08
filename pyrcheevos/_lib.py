"""Low-level ctypes bindings for librcheevos.so."""

from __future__ import annotations

import ctypes
import ctypes.util
import os


def _find_lib() -> str:
    # Look next to this file (installed package dir), then the project root.
    search_dirs = [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ]
    for d in search_dirs:
        candidate = os.path.join(d, "librcheevos.so")
        if os.path.exists(candidate):
            return candidate

    name = ctypes.util.find_library("rcheevos")
    if name:
        return name

    raise OSError(
        "Cannot find librcheevos.so. "
        "Build it first by running 'make' in the project root."
    )


_lib = ctypes.CDLL(_find_lib())

# ---------------------------------------------------------------------------
# Struct definitions matching rc_hash.h / rc_hash_iterator_t
# ---------------------------------------------------------------------------

class _HashFileReader(ctypes.Structure):
    _fields_ = [
        ("open",  ctypes.c_void_p),
        ("seek",  ctypes.c_void_p),
        ("tell",  ctypes.c_void_p),
        ("read",  ctypes.c_void_p),
        ("close", ctypes.c_void_p),
    ]


class _HashCDReader(ctypes.Structure):
    _fields_ = [
        ("open_track",          ctypes.c_void_p),
        ("read_sector",         ctypes.c_void_p),
        ("close_track",         ctypes.c_void_p),
        ("first_track_sector",  ctypes.c_void_p),
        ("open_track_iterator", ctypes.c_void_p),
    ]


class _HashEncryption(ctypes.Structure):
    _fields_ = [
        ("get_3ds_cia_normal_key",   ctypes.c_void_p),
        ("get_3ds_ncch_normal_keys", ctypes.c_void_p),
    ]


class _HashCallbacks(ctypes.Structure):
    _fields_ = [
        ("verbose_message", ctypes.c_void_p),
        ("error_message",   ctypes.c_void_p),
        ("filereader",      _HashFileReader),
        ("cdreader",        _HashCDReader),
        ("encryption",      _HashEncryption),
    ]


class HashIterator(ctypes.Structure):
    """Mirrors rc_hash_iterator_t from rc_hash.h."""
    _fields_ = [
        ("buffer",      ctypes.POINTER(ctypes.c_uint8)),
        ("buffer_size", ctypes.c_size_t),
        ("consoles",    ctypes.c_uint8 * 12),
        ("index",       ctypes.c_int),
        ("path",        ctypes.c_char_p),
        ("userdata",    ctypes.c_void_p),
        ("callbacks",   _HashCallbacks),
    ]


# ---------------------------------------------------------------------------
# Deprecated global message callback (void (*)(const char*))
# ---------------------------------------------------------------------------

DeprecatedMessageCb = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

_lib.rc_hash_init_verbose_message_callback.restype = None
_lib.rc_hash_init_verbose_message_callback.argtypes = [DeprecatedMessageCb]

_lib.rc_hash_init_error_message_callback.restype = None
_lib.rc_hash_init_error_message_callback.argtypes = [DeprecatedMessageCb]

# ---------------------------------------------------------------------------
# Hash iterator API
# ---------------------------------------------------------------------------

_lib.rc_hash_initialize_iterator.restype = None
_lib.rc_hash_initialize_iterator.argtypes = [
    ctypes.POINTER(HashIterator),   # iterator
    ctypes.c_char_p,                # path (UTF-8)
    ctypes.POINTER(ctypes.c_uint8), # buffer (or NULL)
    ctypes.c_size_t,                # buffer_size
]

_lib.rc_hash_iterate.restype = ctypes.c_int
_lib.rc_hash_iterate.argtypes = [
    ctypes.c_char_p,              # hash[33] output buffer
    ctypes.POINTER(HashIterator),
]

_lib.rc_hash_generate.restype = ctypes.c_int
_lib.rc_hash_generate.argtypes = [
    ctypes.c_char_p,              # hash[33] output buffer
    ctypes.c_uint32,              # console_id
    ctypes.POINTER(HashIterator),
]

_lib.rc_hash_destroy_iterator.restype = None
_lib.rc_hash_destroy_iterator.argtypes = [ctypes.POINTER(HashIterator)]

# Deprecated single-call helpers (still reliable for known console+file combos)
_lib.rc_hash_generate_from_file.restype = ctypes.c_int
_lib.rc_hash_generate_from_file.argtypes = [
    ctypes.c_char_p,  # hash[33] output buffer
    ctypes.c_uint32,  # console_id
    ctypes.c_char_p,  # path
]

# ---------------------------------------------------------------------------
# Console info / version
# ---------------------------------------------------------------------------

_lib.rc_console_name.restype = ctypes.c_char_p
_lib.rc_console_name.argtypes = [ctypes.c_uint32]

_lib.rc_version.restype = ctypes.c_uint32
_lib.rc_version.argtypes = []

_lib.rc_version_string.restype = ctypes.c_char_p
_lib.rc_version_string.argtypes = []
