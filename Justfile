default:
    just --list


parse-bios:
    uv run main.py find-most-verbose-bio bios/*.html