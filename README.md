# AI Desktop App

A professional RAG-based ChatBot desktop application built with Tauri, Next.js, and Python FastAPI.

## Project Structure

```
ai-desktop-app
│
├── .github/workflows  # CI/CD Release pipelines (Win, Mac, Linux)
├── src-tauri          # Tauri desktop application (Rust)
├── frontend           # Next.js frontend (TypeScript & Tailwind)
├── backend            # Python FastAPI backend
│   ├── app            # Backend source code (Modular Layered Architecture)
│   └── data           # Retrieval data (Documents, Index)
├── models             # Local LLM models (*.gguf)
└── README.md
```

## Prerequisites

- [Node.js](https://nodejs.org/) (LTS)
- [Rust](https://www.rust-lang.org/tools/install)
- [Python 3.10+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (for Python package management)

## Setup & Development

### 1. Model Preparation
Place your LLM model (e.g., `mistral-7b-instruct.Q4_K_M.gguf`) in the `models/` directory at the project root.

### 2. Backend Configuration
Navigate to the `backend/` folder and set up your environment:
```bash
cd backend
cp .env.example .env
# Edit .env to match your model filename if necessary
uv sync
```

### 3. Frontend Setup
Navigate to the `frontend/` folder and install dependencies:
```bash
cd frontend
npm install
```

### 4. Running the App
From the project root, run:
```bash
# Start frontend dev server + tauri (backend sidecar will be spawned automatically)
npm run tauri dev
```

---

## Building the Application

### Manual Build (Windows/Local)
To generate a production installer locally:

1. **Build Python Sidecar**:
   ```bash
   cd backend
   uv run python build.py
   ```
   *This packages the backend into `src-tauri/binaries/backend-api-<triple>.exe`.*

2. **Build Desktop App**:
   ```bash
   # From root
   npm run tauri build
   ```

### Cross-Platform (GitHub Actions)
This project is configured for automated releases via GitHub Actions. 
- To trigger a build for Windows, macOS, and Linux:
  1. Commit your changes.
  2. Tag your commit: `git tag v0.1.0`
  3. Push tags: `git push origin --tags`
  4. Installations will appear in your GitHub Repository "Releases" as drafts.

## License
Powered by Neuro Kode | Copyright © 2024
