import sys


def main(argv: list[str] | None = None) -> int:
    """Entrypoint for the files-state app."""
    if argv is None:
        argv = sys.argv[1:]

    # TODO: Replace with real logic
    print("app-manager: hello world", " ".join(argv))
    return 0


if __name__ == "main":  # pragma: no cover
    raise SystemExit(main())
