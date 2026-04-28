"""Seed Onyx EE enterprise settings with the Insight brand.

Runs idempotently. Writes to the KV store (application name + custom logo flags)
and uploads the logo + logotype PNGs into the file store. After this runs,
the app chrome (title, favicon, login, sidebar, emails) shows Insight
without further source-code changes.

Usage:

    # Full-Docker deployment (default). The script auto-detects a running
    # api_server container, copies itself into it, and runs inside.
    python scripts/insight_brand.py

    # Hybrid / in-container invocation. Run inside the api_server container
    # where Postgres, MinIO, Redis are all reachable at their internal hosts.
    python scripts/insight_brand.py --in-container

    # Target a specific container (default: onyx-api_server-1)
    python scripts/insight_brand.py --container onyx-api_server-1

    # Override the application name (default: Insight)
    python scripts/insight_brand.py --name Insight
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND = REPO_ROOT / "backend"

IN_CONTAINER_STATIC = Path("/app/static/images")
HOST_STATIC = BACKEND / "static" / "images"

DEFAULT_CONTAINER = "insight-api_server-1"


def _is_in_container() -> bool:
    return IN_CONTAINER_STATIC.is_dir() and Path("/app").is_dir()


def _bootstrap_path() -> None:
    """Make `ee.*` and `onyx.*` importable when run from repo root.

    Inside the api_server container, /app is already on sys.path.
    """
    if _is_in_container():
        if "/app" not in sys.path:
            sys.path.insert(0, "/app")
        os.chdir("/app")
    else:
        sys.path.insert(0, str(BACKEND))
        os.chdir(BACKEND)


def seed(name: str, logo: Path, logotype: Path) -> None:
    _bootstrap_path()

    from ee.onyx.server.enterprise_settings.models import EnterpriseSettings
    from ee.onyx.server.enterprise_settings.store import (
        load_settings,
        store_settings,
        upload_logo,
    )
    from onyx.db.engine.sql_engine import SqlEngine
    from onyx.utils.variable_functionality import global_version

    global_version.set_ee()
    SqlEngine.init_engine(pool_size=5, max_overflow=2)

    current = load_settings()

    merged = EnterpriseSettings(
        **{
            **current.model_dump(),
            "application_name": name,
            "use_custom_logo": True,
            "use_custom_logotype": True,
        }
    )
    store_settings(merged)
    print(f"[ok] enterprise_settings.application_name = {name!r}")
    print("[ok] use_custom_logo = True, use_custom_logotype = True")

    if not logo.is_file():
        raise SystemExit(f"[err] logo not found: {logo}")
    if not logotype.is_file():
        raise SystemExit(f"[err] logotype not found: {logotype}")

    if not upload_logo(str(logo), is_logotype=False):
        raise SystemExit(f"[err] failed to upload logo {logo}")
    print(f"[ok] uploaded logo  <- {logo}")

    if not upload_logo(str(logotype), is_logotype=True):
        raise SystemExit(f"[err] failed to upload logotype {logotype}")
    print(f"[ok] uploaded logotype  <- {logotype}")

    print("\n[done] Insight brand seeded. Hard-refresh the browser to pick up changes.")


def _exec_in_container(container: str, name: str) -> int:
    """Copy this script into the running api_server container and run it there.

    This path is used when the user invokes the script from the host but the
    full stack (including MinIO) is running under Docker Compose, so only the
    container has a resolvable `minio` hostname and the S3 credentials.
    """
    if shutil.which("docker") is None:
        raise SystemExit(
            "[err] 'docker' not on PATH and --in-container was not used. "
            "Install Docker or run inside the api_server container."
        )

    inspect = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container],
        capture_output=True,
        text=True,
    )
    if inspect.returncode != 0 or inspect.stdout.strip() != "true":
        raise SystemExit(
            f"[err] container {container!r} is not running. "
            "Start the stack with `./run-platform.sh dev` or pass --container <name>."
        )

    remote_path = "/tmp/insight_brand.py"
    this_file = Path(__file__).resolve()

    print(f"[info] copying {this_file.name} -> {container}:{remote_path}")
    subprocess.run(
        ["docker", "cp", str(this_file), f"{container}:{remote_path}"],
        check=True,
    )

    print(f"[info] executing inside {container}")
    cmd = [
        "docker",
        "exec",
        container,
        "python",
        remote_path,
        "--in-container",
        "--name",
        name,
    ]
    completed = subprocess.run(cmd)
    return completed.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="Insight", help="application_name to seed")
    parser.add_argument(
        "--container",
        default=DEFAULT_CONTAINER,
        help="Docker container name to exec into (host mode only)",
    )
    parser.add_argument(
        "--in-container",
        action="store_true",
        help="Run the seed logic directly (assumed to be inside the api_server container).",
    )
    parser.add_argument(
        "--logo",
        type=Path,
        default=None,
        help="Path to square logo PNG (defaults to /app/static/images/logo.png "
        "inside the container or backend/static/images/logo.png on the host).",
    )
    parser.add_argument(
        "--logotype",
        type=Path,
        default=None,
        help="Path to horizontal logotype PNG (defaults to /app/static/images/logotype.png "
        "inside the container or backend/static/images/logotype.png on the host).",
    )
    args = parser.parse_args()

    if args.in_container or _is_in_container():
        static = IN_CONTAINER_STATIC if _is_in_container() else HOST_STATIC
        logo = (args.logo or (static / "logo.png")).resolve()
        logotype = (args.logotype or (static / "logotype.png")).resolve()
        seed(name=args.name, logo=logo, logotype=logotype)
        return

    rc = _exec_in_container(args.container, args.name)
    sys.exit(rc)


if __name__ == "__main__":
    main()
