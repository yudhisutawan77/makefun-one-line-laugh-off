"""One-Line Laugh-Off entry.

Writes exactly one funny line to the output path the harness provides.
The harness writes the artifact to /output/entry.txt; the output location
may be given as a file path or as a directory (then entry.txt inside it).
The kit harness exports MAKEFUN_OUTPUT_DIR and reads
``$MAKEFUN_OUTPUT_DIR/entry.txt`` afterwards, so that variable is
honoured here (after an explicit ENTRY_OUT).
Standard library only.
"""

import os

def joke() -> str:
    """The single funny line, kept as one literal string."""
    return (
        "I finally found the perfect work-life balance: "
        "I do all my work in bed and all my sleeping at my desk."
    )


def resolve_output_path() -> str:
    """Return the file path to write, from env or the default location.

    Priority: ENTRY_OUT first, then the kit harness directory
    MAKEFUN_OUTPUT_DIR, then ENTRY_OUT_DIR / OUTPUT_DIR / OUTPUT,
    and finally /output/entry.txt.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        if os.path.isdir(entry_out) or entry_out.endswith(os.sep):
            return os.path.join(entry_out, "entry.txt")
        return entry_out
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        # MAKEFUN_OUTPUT_DIR always names a directory, even when it
        # does not exist yet (makedirs in main() creates it).
        return os.path.join(makefun_dir, "entry.txt")
    for key in ("ENTRY_OUT_DIR", "OUTPUT_DIR", "OUTPUT"):
        value = os.environ.get(key)
        if value:
            if os.path.isdir(value) or value.endswith(os.sep):
                return os.path.join(value, "entry.txt")
            return value
    return "/output/entry.txt"


def main() -> None:
    text = joke()
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


if __name__ == "__main__":
    main()
