import os

# Base directory
BASE_DIR = os.getcwd()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:14b"

# V5 Specific Constraints
MAX_FILE_SIZE = 2_000_000  # We can handle slightly larger files as AST filtering drops noise
MAX_THREADS = 8
MAX_AI_THREADS = 1         # 14B models are heavy, limit concurrency to 1

# Ignore rules (compiled binaries, assets, etc.)
IGNORE_EXT = {
    '.exe', '.dll', '.bin', '.ckpt', '.pyc', '.class', '.o', '.so',
    '.safetensors', '.zip', '.jpg', '.png', '.mp4', '.pdf', '.woff', '.ttf'
}

IGNORE_DIRS = {
    '.git', 'node_modules', 'venv', 'env', 
    '__pycache__', '.pytest_cache', 'build', 'dist', 'vendor'
}
