✨ Overview
RepoMedic AI is a repository-maintenance assistant designed to help developers inspect project files, understand dependency declarations, and produce an actionable maintenance report with the help of a locally running large language model.
Instead of relying only on a quick glance at a codebase, RepoMedic AI gathers repository evidence and asks an AI model to explain potential risks and practical next steps. Its Streamlit interface brings the workflow into a simple dashboard.
Built for developers who want clearer repository insights—with evidence, not guesswork.


🚀 Key Features
- 🔎 Repository analysis — inspect supported project files and dependency declarations.
- 🧠 Local LLM-powered insights — generate analysis with Ollama and the gemma3:4b model.
- 📋 Structured maintenance report — organize findings, recommended actions, verification notes, and unresolved risks.
- 🧪 Test runner — run the project's pytest suite from the dashboard.
- 📄 Markdown report — save and review the generated Dependency Exit Capsule.
- ⬇️ JSON export — download the report in a machine-readable JSON wrapper from the UI when that feature is enabled.
- 🖥️ Streamlit dashboard — access analysis and project information from a single interface.
🧭 How It Works
Repository files
      │
      ▼
Collect supported source and dependency evidence
      │
      ▼
Build an analysis prompt using project instructions
      │
      ▼
Ollama + Gemma 3 (gemma3:4b)
      │
      ▼
Structured maintenance report
      │
      ├── View in Streamlit
      ├── Save as Markdown
      └── Export as JSON (through the UI)
🛠️ Technology Stack
Technology	Purpose
Python	Core application and repository analysis
Streamlit	Interactive web dashboard
Ollama	Local model runtime
Gemma 3 (gemma3:4b)	AI-generated repository analysis
Git	Clone and version-control repositories
pytest	Automated tests


📂 Project Structure
RepoMedic-AI/
├── app.py                         # Analysis workflow and Ollama integration
├── ui.py                          # Streamlit dashboard
├── skills/
│   └── skill.md                   # Analysis instructions
├── tests/                         # Automated tests
├── demo_repo/                     # Sample repository for local testing
├── artifacts/
│   └── dependency_exit_capsule.md # Generated analysis report
├── requirements.txt               # Python dependencies (if included)
└── README.md
Your local checkout may contain additional files or a slightly different structure.
⚡ Getting Started
Prerequisites
Install or prepare the following:
- Python 3.10 or newer (use a version supported by your dependencies)
- Git
- Ollama
- The gemma3:4b model available in Ollama
1. Clone the project
git clone https://github.com/dishanakhawa/H26_Gnapikas_RepoShield.git
cd H26_Gnapikas_RepoShield
2. Create and activate a virtual environment
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
If the project includes requirements.txt:
python -m pip install -r requirements.txt
If not, install the core UI and test packages:
python -m pip install streamlit pytest
4. Start Ollama and download the model
ollama pull gemma3:4b
Make sure Ollama is running locally. On systems where Ollama does not start automatically, launch the Ollama application or start its service before analysis.
5. Launch RepoMedic AI
python -m streamlit run ui.py
Streamlit will print a local URL—usually http://localhost:8501. Open it in your browser.
🧪 Run Tests
From the project root, with your virtual environment activated:
python -m pytest -v
You can also use the dashboard's Run Tests action if available.
📑 Reports & Exports
RepoMedic AI can produce a Markdown report named:
artifacts/dependency_exit_capsule.md
The report is intended to separate repository observations from AI-generated recommendations and to record verification notes. Where available, the dashboard also provides a JSON download for downstream tools or archival.
Important: AI-generated findings are suggestions, not proof of a vulnerability or a substitute for package-manager audits, security scanners, or running tests.
🔐 Security & Responsible Use
- Treat AI output as advisory and verify important findings against the actual files.
- Do not upload secrets, access tokens, private keys, credentials, or sensitive source code to a public repository.
- Review reports before committing them; they may contain paths or project details.
- Analyze only repositories you are authorized to inspect.
- Cloning a repository does not make its code trustworthy. Do not execute untrusted repository scripts as part of analysis.
- For public deployments, add appropriate resource limits and network protections, and avoid exposing a local Ollama endpoint.
🗺️ Roadmap
Potential future improvements:
- Dependency inventory and version comparison
- Integration with dedicated vulnerability databases and security scanners
- Report history and repository comparison
- CI workflow integration
- Additional report formats and configurable analysis rules
Roadmap items are ideas, not claims that these features are already implemented.
🤝 Contributing
Contributions, bug reports, and practical suggestions are welcome.
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add or update tests.
4. Run python -m pytest -v.
5. Open a pull request describing the change.
⚠️ Limitations
RepoMedic AI's analysis depends on the files it collects and the quality of the model response. It may miss issues, misinterpret code, or recommend changes that are not appropriate for a particular project. Always validate recommendations before applying them.
👩‍💻 Maintainer
Disha Nakhawa
## 👩‍💻 Maintainer

**Disha Nakhawa**

- **GitHub:** [dishanakhawa](https://github.com/dishanakhawa)
- **Live App:** [RepoMedic AI](https://h26gnapikasreposhield-jfm5mczzjwzavrevcza48t.streamlit.app/)
