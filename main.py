#!/usr/bin/env python3
"""Copy the bundled front-page image to the grader output dir.

No network. Deterministic: writes the exact bundled bytes.
Respects MAKEFUN_OUTPUT_DIR (default /output). Clears the output
dir's CONTENTS ONLY -- never removes the output dir itself.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

# SHA-256 of the bundled entry.png (computed after generating it).
EXPECTED_SHA256 = "e4dfea1bcb6312660064080856beae7c58a696f513a0bdae3b6b1fe117cf7536"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def clear_contents(out_dir):
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def main():
    if sha256_of(SRC) != EXPECTED_SHA256:
        print("ERROR: bundled entry.png failed SHA-256 check", file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    clear_contents(out_dir)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    if sha256_of(dest) != EXPECTED_SHA256:
        print("ERROR: copied entry.png failed SHA-256 check", file=sys.stderr)
        sys.exit(1)
    print("wrote", dest, os.path.getsize(dest), "bytes, sha256 verified")


if __name__ == "__main__":
    main()
