"""
Custom build step that compiles librcheevos.so (or .dylib / .dll) from the
bundled C sources and places it inside the pyrcheevos package directory before
setuptools assembles the wheel.

This runs automatically during:
  pip install .
  pip install -e .
  python -m build
"""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

# ---------------------------------------------------------------------------
# C source files (relative to the project root)
# ---------------------------------------------------------------------------

RCHEEVOS_SRCS: list[str] = [
    "rcheevos/src/rc_compat.c",
    "rcheevos/src/rc_util.c",
    "rcheevos/src/rc_version.c",
    "rcheevos/src/rcheevos/alloc.c",
    "rcheevos/src/rcheevos/condition.c",
    "rcheevos/src/rcheevos/condset.c",
    "rcheevos/src/rcheevos/consoleinfo.c",
    "rcheevos/src/rcheevos/format.c",
    "rcheevos/src/rcheevos/lboard.c",
    "rcheevos/src/rcheevos/memref.c",
    "rcheevos/src/rcheevos/operand.c",
    "rcheevos/src/rcheevos/rc_validate.c",
    "rcheevos/src/rcheevos/richpresence.c",
    "rcheevos/src/rcheevos/runtime.c",
    "rcheevos/src/rcheevos/runtime_progress.c",
    "rcheevos/src/rcheevos/trigger.c",
    "rcheevos/src/rcheevos/value.c",
    "rcheevos/src/rhash/aes.c",
    "rcheevos/src/rhash/cdreader.c",
    "rcheevos/src/rhash/hash.c",
    "rcheevos/src/rhash/hash_disc.c",
    "rcheevos/src/rhash/hash_encrypted.c",
    "rcheevos/src/rhash/hash_rom.c",
    "rcheevos/src/rhash/hash_zip.c",
    "rcheevos/src/rhash/md5.c",
    "rcheevos/src/rapi/rc_api_common.c",
    "rcheevos/src/rapi/rc_api_editor.c",
    "rcheevos/src/rapi/rc_api_info.c",
    "rcheevos/src/rapi/rc_api_runtime.c",
    "rcheevos/src/rapi/rc_api_user.c",
]

INCLUDE_DIRS: list[str] = [
    "rcheevos/include",
    "rcheevos/src",
]


def _lib_name() -> str:
    system = platform.system()
    if system == "Darwin":
        return "librcheevos.dylib"
    if system == "Windows":
        return "rcheevos.dll"
    return "librcheevos.so"


def _compiler() -> str:
    """Return 'gcc' on Linux/macOS, 'cl' is not supported - use mingw gcc on Windows."""
    if platform.system() == "Windows":
        # cibuildwheel Windows images provide gcc via mingw
        return "gcc"
    return "gcc"


def _compile_shared_lib(dest: Path) -> None:
    """Compile the rcheevos C sources into a shared library at *dest*."""
    system = platform.system()
    cc = _compiler()

    cmd: list[str] = [cc, "-O2", "-DRC_SHARED"]

    if system == "Darwin":
        cmd += ["-dynamiclib", "-fPIC"]
    elif system == "Windows":
        cmd += ["-shared"]
    else:
        cmd += ["-shared", "-fPIC"]

    for inc in INCLUDE_DIRS:
        cmd += ["-I", inc]

    cmd += RCHEEVOS_SRCS
    cmd += ["-o", str(dest)]

    if system != "Windows":
        cmd += ["-lz", "-lm"]

    print(f"[setup.py] Compiling {dest.name} ...", flush=True)
    print(f"[setup.py] {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd)


class BuildWithSharedLib(build_py):
    """Extends build_py to compile librcheevos before copying Python sources."""

    def run(self) -> None:
        # Resolve the destination inside the build tree so the .so ends up
        # inside the package when the wheel is assembled.
        pkg_build_dir = Path(self.build_lib) / "pyrcheevos"
        pkg_build_dir.mkdir(parents=True, exist_ok=True)
        dest = pkg_build_dir / _lib_name()
        _compile_shared_lib(dest)

        # Also drop a copy next to the source package so editable installs
        # (pip install -e .) pick it up immediately.
        src_pkg_dir = Path("pyrcheevos")
        src_copy = src_pkg_dir / _lib_name()
        if not src_copy.exists():
            import shutil
            shutil.copy2(dest, src_copy)

        super().run()


setup(cmdclass={"build_py": BuildWithSharedLib})
