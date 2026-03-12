import PyInstaller.__main__
import sys
import os
import shutil
import platform

def get_target_triple():
    """Detect the target triple for the current platform."""
    # This is a simplified detection
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if machine == 'amd64' or machine == 'x86_64':
        arch = 'x86_64'
    elif machine == 'arm64' or machine == 'aarch64':
        arch = 'aarch64'
    else:
        arch = machine

    if system == 'windows':
        return f"{arch}-pc-windows-msvc"
    elif system == 'darwin':
        return f"{arch}-apple-darwin"
    elif system == 'linux':
        return f"{arch}-unknown-linux-gnu"
    return f"{arch}-unknown"

if __name__ == '__main__':
    # Get target triple from env or auto-detect
    triple = os.environ.get('TAURI_TARGET_TRIPLE') or get_target_triple()
    print(f"Targeting triple: {triple}")

    # Run PyInstaller
    PyInstaller.__main__.run([
        'app/main.py',
        '--onefile',
        '--name=backend-api',
        '--clean',
        '--noconfirm',
        '--hidden-import=app',
        '--hidden-import=app.core',
        '--hidden-import=app.core.config',
        '--hidden-import=app.models',
        '--hidden-import=app.models.schemas',
        '--hidden-import=app.services',
        '--hidden-import=app.services.llm_service',
        '--hidden-import=app.services.vector_service',
        '--hidden-import=app.api',
        '--hidden-import=app.api.chat',
        '--hidden-import=langchain',
        '--hidden-import=langchain_community',
        '--hidden-import=sentence_transformers',
        '--hidden-import=faiss',
        '--hidden-import=pypdf',
        '--hidden-import=ctransformers',
        '--hidden-import=pydantic',
        '--hidden-import=uvicorn',
        '--hidden-import=fastapi',
        '--hidden-import=starlette',
    ])

    # Move to Tauri binaries folder
    exe_ext = ".exe" if platform.system().lower() == 'windows' else ""
    src = os.path.join('dist', f'backend-api{exe_ext}')
    
    # Target directory: ../src-tauri/binaries/
    target_dir = os.path.join('..', 'src-tauri', 'binaries')
    os.makedirs(target_dir, exist_ok=True)
    
    target_name = f"backend-api-{triple}{exe_ext}"
    dest = os.path.join(target_dir, target_name)
    
    print(f"Moving {src} to {dest}")
    if os.path.exists(dest):
        os.remove(dest)
    shutil.move(src, dest)
    print("Done!")
