"""
Application Configuration

This file contains all configurable settings for the assistant.
Changing values here automatically affects the entire project.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================
# Assistant Information
# ==========================

ASSISTANT_NAME = "Soni"

VERSION = "1.0.0"

LANGUAGE = "en"

# ==========================
# Speech Settings
# ==========================

VOICE_RATE = 180          # Words per minute

VOICE_VOLUME = 1.0        # 0.0 to 1.0

# ==========================
# Microphone Settings
# ==========================

MIC_TIMEOUT = 5

PHRASE_TIME_LIMIT = 5

# ==========================
# Database
# ==========================

DATABASE_PATH = "database/assistant.db"

# ==========================
# Logging
# ==========================

LOG_LEVEL = "INFO"

LOG_FILE = PROJECT_ROOT / "logs" / "assistant.log"

# ==========================
# Whisper Settings
# ==========================

WHISPER_MODEL = "base"

COMPUTE_TYPE = "int8"

DEVICE = "cpu"

BEAM_SIZE = 5

# ==========================
# Piper Configuration
# ==========================

PIPER_PATH = r"assets/piper/piper.exe"

VOICE_MODEL = r"assets/voices/en_US-lessac-medium.onnx"

OUTPUT_AUDIO = r"assets/temp/output.wav"

# ==========================
# LLM Configuration
# ==========================

LLM_MODEL = "qwen2.5:3b"

OLLAMA_HOST = "http://localhost:11434"

# ==========================
# Application Configuration
# ==========================

APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe",
}
# ==========================
# Playwright(browser) Configuration
# ==========================
PLAYWRIGHT_HEADLESS = True

SEARCH_ENGINE = "https://duckduckgo.com/?q={query}"

# ==========================
# File search configuration
# ==========================

EXTENSION_MAP = {
    "pdf": [".pdf"],
    "python": [".py"],
    "image": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
    "video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "excel": [".xlsx", ".xls"],
    "word": [".docx", ".doc"],
    "text": [".txt", ".md"],
}

MAX_SEARCH_RESULTS = 20

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode"
}

SUPPORTED_TEXT_FILES = {
    ".txt",
    ".md",
    ".py",
    ".java",
    ".json",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".csv",
    ".yaml",
    ".yml",
    ".ini",
    ".log"
}

# ==========================
# wake word detection configuration
# ==========================

WAKE_WORD_THRESHOLD = 0.1
WAKE_WORD_SAMPLE_RATE = 16000
WAKE_WORD_BLOCK_SIZE = 1280

WAKE_WORD = "hey_jarvis"