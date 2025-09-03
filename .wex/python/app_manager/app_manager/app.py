import sys
import os


def main(argv: list[str] | None = None) -> int:
    """Thin entrypoint delegating to shared manager if available."""
    if argv is None:
        argv = sys.argv[1:]

    # Try to import the shared manager package if installed
    try:
        from wexample_wex_core.app_manager import run as run_manager
    except Exception:
        app_root = os.getenv(
            "APP_ROOT",
            "/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip/app",
        )
        print(
            "app-manager: manager package not found.\n"
            f"Set APP_ROOT (current: {app_root}) or install 'wexample-wex-core'.\n"
            f"Args: {' '.join(argv)}"
        )
        return 0

    # Delegate execution
    return int(run_manager(argv))


if __name__ == "main":  # pragma: no cover
    raise SystemExit(main())
