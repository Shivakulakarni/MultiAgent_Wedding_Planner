from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest


def _find_free_port() -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def streamlit_url(tmp_path_factory):
    port = _find_free_port()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run",
            os.path.join(project_root, "run_app.py"),
            "--server.headless", "true",
            "--server.port", str(port),
            "--browser.gatherUsageStats", "false",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        cwd=project_root,
        env={**os.environ, "GROQ_API_KEY": "", "TAVILY_API_KEY": ""},
    )
    deadline = time.time() + 45
    while time.time() < deadline:
        try:
            import urllib.request
            urllib.request.urlopen(f"http://localhost:{port}", timeout=2)
            break
        except Exception:
            time.sleep(0.5)
    else:
        stderr_output = proc.stderr.read(4096).decode(errors="replace") if proc.stderr else ""
        proc.kill()
        pytest.fail(f"Streamlit app did not start in time.\nstderr: {stderr_output}")
    yield f"http://localhost:{port}"
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture
def live_page(page, streamlit_url):
    page.goto(streamlit_url, wait_until="networkidle")
    yield page
