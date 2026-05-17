# AI Web App

A premium, RAG-based web application for healthcare professionals, built with **Next.js**, and **FastAPI**.

## 🚀 Overview

AI Web App provides a seamless, high-performance interface for interacting with LLMs locally. It leverages a modular layered architecture to ensure scalability and ease of maintenance.

### Key Features
- **Local RAG**: Context-aware chat using your own documents.
- **FastAPI Backend**: High-performance Python API for LLM orchestration.
- **Next.js Frontend**: Modern, responsive UI with Tailwind CSS.

---

## 📂 Project Structure

```text
ai-web-app/
├── web/              # React / Next.js UI (TypeScript & Tailwind)
├── api/              # Python AI API (FastAPI & Modular Architecture)
├── models/           # Local LLM models (*.gguf)
├── docker-compose.yml # Containerized orchestration
└── README.md         # Project documentation
```

---

## 🛠️ Prerequisites

- **Node.js** (LTS)
- **Python 3.10+**
- **uv** (Python package manager)
- **Docker & Docker Compose** (Optional, for containerized dev)

---

## ⚡ Quick Start

### 1. Unified Setup
From the project root, run the following to install all dependencies:
```bash
npm install
cd web && npm install
cd ../api && uv sync
```

### 2. Model Preparation
Place your LLM model (e.g., `mistral-7b-instruct.Q4_K_M.gguf`) in the `models/` directory.

### 3. Development Mode
Start the entire stack in development mode:
```bash
npm run dev
```

---

## 🐳 Docker Deployment

To run the application services using Docker:
```bash
docker-compose up --build
```

---

## 🏗️ Building for Production

### Local Build (Windows)
1. **Build Python Sidecar**:
   ```bash
   npm run backend:build
   ```
2. **Build Desktop Installer**:
   ```bash
   npm run tauri build
   ```

---

## 📄 License

Powered by **Neuro Kode's** | Copyright © 2024

