
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "artifacts" / "dependency_exit_capsule.md"

st.set_page_config(
    page_title="RepoMedic AI",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #0b1020; color: #e8edf8; }
    [data-testid="stSidebar"] { background: #11182b; }
    .block-container { padding-top: 2rem; max-width: 1250px; }
    h1, h2, h3 { color: #f1f5ff; }
    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #334466;
        background: #182440;
        color: white;
        padding: 0.6rem 1rem;
    }
    div.stButton > button:hover {
        border-color: #7c83ff;
        color: #a5b4fc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🛡️ RepoMedic AI")
    st.caption("AI-powered repository maintenance")
    st.divider()
    page = st.radio(
        "Navigation",
        ["Dashboard", "Analysis Report", "Project Info"],
    )
    st.divider()
    st.caption("Local development • Ollama")

def validate_github_url(url):
    """Accept standard HTTPS URLs for public GitHub repositories."""
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme != "https" or parsed.hostname != "github.com":
            return False

        if parsed.port is not None or parsed.username or parsed.password:
            return False

        parts = parsed.path.strip("/").split("/")
        if len(parts) != 2:
            return False

        name_pattern = re.compile(r"^[A-Za-z0-9_.-]+$")
        return all(name_pattern.fullmatch(part) for part in parts)
    except (ValueError, AttributeError):
        return False


def analyze_github_repository(url):
    """Clone a public repository temporarily and analyze its files."""
    if not validate_github_url(url):
        raise ValueError(
            "Enter a public GitHub URL like "
            "https://github.com/owner/repository"
        )

    with tempfile.TemporaryDirectory(prefix="repomedic_") as temp_dir:
        checkout = Path(temp_dir) / "repository"

        result = subprocess.run(
            [
                "git",
                "-c", "core.hooksPath=NUL",
                "clone",
                "--depth", "1",
                "--no-recurse-submodules",
                "--",
                url.strip(),
                str(checkout),
            ],
            capture_output=True,
            text=True,
            timeout=120,
            shell=False,
        )

        if result.returncode != 0:
            detail = (result.stderr or "Git clone failed.")[-1500:]
            raise RuntimeError(detail)

        # Analyze while the temporary checkout still exists.
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "app.py"),
                "--repo",
                str(checkout),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=240,
            shell=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                (result.stderr or result.stdout or "Analysis failed.")[-3000:]
            )

        if not REPORT.exists():
            raise RuntimeError("Analysis finished but no report was created.")

        return REPORT.read_text(encoding="utf-8")


if page == "Dashboard":
    st.title("Repository Health Dashboard")
    st.write(
        "Analyze a public GitHub repository, inspect maintenance risks, "
        "and download the report."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Analysis Engine", "Gemma 3:4b")
    with col2:
        st.metric("Repository Source", "GitHub URL")
    with col3:
        st.metric("Latest Report", "Available" if REPORT.exists() else "None")

    st.divider()
    st.subheader("🔎 Analyze a Repository")

    with st.form("repository_form"):
        repo_url = st.text_input(
            "GitHub repository URL",
            placeholder="https://github.com/owner/repository",
            help="Use a public repository URL. Private repositories are not supported.",
        )
        submitted = st.form_submit_button(
            "Analyze Repository",
            use_container_width=True,
        )

    if submitted:
        if not validate_github_url(repo_url):
            st.error(
                "Invalid URL. Enter a public repository URL such as "
                "https://github.com/owner/repository"
            )
        else:
            try:
                with st.spinner(
                    "Cloning repository and asking Ollama to analyze its files..."
                ):
                    report_content = analyze_github_repository(repo_url)

                st.session_state["latest_report"] = report_content
                st.session_state["latest_repo_url"] = repo_url.strip()
                st.success("Repository analysis completed!")

            except subprocess.TimeoutExpired:
                st.error("The operation timed out. Try a smaller repository.")
            except (RuntimeError, ValueError, OSError) as exc:
                st.error(f"Analysis failed: {exc}")

    latest_report = st.session_state.get("latest_report")

    if latest_report:
        st.divider()
        st.subheader("Latest Analysis")
        st.caption(
            "Repository: " +
            st.session_state.get("latest_repo_url", "Unknown")
        )
        st.markdown(latest_report)

        json_data = {
            "repository_url": st.session_state.get("latest_repo_url", ""),
            "report_title": "RepoMedic AI Dependency Exit Capsule",
            "format": "markdown",
            "report_content": latest_report,
        }

        st.download_button(
            "⬇️ Download JSON Report",
            data=json.dumps(json_data, indent=2, ensure_ascii=False),
            file_name="dependency_exit_capsule.json",
            mime="application/json",
            use_container_width=True,
        )

    elif REPORT.exists():
        st.divider()
        st.subheader("Previous Report")
        st.info(
            "A previous report exists. Open Analysis Report to view it. "
            "It may refer to a different repository."
        )

elif page == "Analysis Report":
    st.title("Analysis Report")

    content = st.session_state.get("latest_report")

    if content:
        repo_url = st.session_state.get("latest_repo_url", "")
    elif REPORT.exists():
        content = REPORT.read_text(encoding="utf-8")
        repo_url = "Previous report; repository URL not recorded"
    else:
        content = None
        repo_url = ""

    if content:
        st.caption(f"Repository: {repo_url}")
        st.markdown(content)

        report_json = {
            "repository_url": repo_url,
            "report_title": "RepoMedic AI Dependency Exit Capsule",
            "format": "markdown",
            "report_content": content,
        }

        st.download_button(
            "⬇️ Download JSON Report",
            data=json.dumps(report_json, indent=2, ensure_ascii=False),
            file_name="dependency_exit_capsule.json",
            mime="application/json",
        )
    else:
        st.info("Analyze a repository from the Dashboard to generate a report.")

else:
    st.title("Project Information")
    st.markdown(
        """
        ### 🛡️ RepoMedic AI

        - `app.py` — repository analysis using Ollama
        - `ui.py` — Streamlit dashboard
        - `skills/skill.md` — maintenance instructions
        - `artifacts/` — generated analysis report

        **Safety:** Only public GitHub HTTPS repository URLs are accepted.
        Repository code is inspected as text and is not executed by this UI.
        AI findings should be verified before taking action.
        """
    )
