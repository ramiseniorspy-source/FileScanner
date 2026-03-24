# 🏴‍☠️ Scanner V5: AST-Aware Bug Bounty Engine

Scanner V5 is an advanced, AI-powered reconnaissance and Static Application Security Testing (SAST) engine purpose-built for bug bounty hunters.

Unlike traditional grep-based scanners, Scanner V5 deeply understands code architecture by parsing Abstract Syntax Trees (ASTs). It maps execution flows, traces dependencies, and leverages a local Large Language Model (`qwen2.5-coder:14b`) to pinpoint complex, critical business-logic vulnerabilities such as IDORs, SSRF, RCE, and Injection flaws.

## ✨ Core Features

- **AST Context Mapping**: Builds an execution graph of the repository (Native AST for Python, heuristic regex parsing for JS/TS/PHP/Go, etc.) to understand how functions and files connect.
- **Smart AI Triage**: Horizontally scales across massive codebases by chunking the AST and asking the AI to triage priority targets. This drastically reduces noise and saves compute.
- **Deep Semantic Analysis**: Analyzes priority execution contexts under extreme zero-hallucination constraints to surface real, exploitable vulnerabilities.
- **Automated Ingestion**: Automatically clone remote GitHub repositories or scan local directories.
- **Bug Bounty Ready Reports**: Outputs detailed findings, including vulnerability types, descriptions, proof-of-concept code snippets, and remediation steps to a `bounty_report.md` file.

## 🛠️ Prerequisites

- **Python 3.8+**
- **Git** (for remote repository ingestion)
- **Ollama** running locally with the `qwen2.5-coder:14b` model installed.
  ```bash
  ollama run qwen2.5-coder:14b
  ```

## 🚀 Usage

Run the scanner via `main.py`, providing a target repository (local path or GitHub URL):

```bash
python main.py --repo <path_or_url> --mode bounty
```

### Arguments

- `--repo`: **(Required)** The target repository to scan. Can be a local filesystem path or a remote HTTP/HTTPS Git URL.
- `--mode`: **(Optional)** Analysis mode. Currently supports `bounty` (default) and `recon`.

### Example

```bash
python main.py --repo https://github.com/example/vulnerable-app --mode bounty
```

## 🧠 How It Works

1. **Ingestion**: The orchestrator clones the target repository or indexes the local directory.
2. **Collection**: Filters out noise (binaries, node_modules, compiled assets) to focus strictly on logic files.
3. **AST Graph Building**: Parses code syntax to map out functions, classes, and imports across all files.
4. **AI Graph Triage**: Chunks the project graph and asks the AI to identify high-probability vulnerability targets based on structural and naming heuristics.
5. **Deep Analysis**: Assembles comprehensive execution contexts for the priority targets and performs deep AI semantic analysis looking for OWASP Top 10 vulnerabilities.
6. **Reporting**: Generates a clean, actionable markdown report (`bounty_report.md`) containing confirmed findings.

## ⚙️ Configuration

You can tweak Scanner V5's behavior by editing the `config.py` file:

- `OLLAMA_URL`: Ensure this points to your local (or remote) Ollama API endpoint.
- `MODEL`: Default is `qwen2.5-coder:14b`. Can be changed if you want to experiment with other reasoning or coding models.
- `MAX_THREADS` / `MAX_AI_THREADS`: Adjust concurrency based on your hardware capabilities.

## ⚠️ Disclaimer

Scanner V5 is built for educational and authorized Bug Bounty purposes only. Do not use this tool against targets you do not have explicit permission to test.
