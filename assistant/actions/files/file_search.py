import os
from datetime import datetime
from pathlib import Path

from assistant.actions.base_tool import BaseTool, ToolType
from assistant.config.settings import (
    EXTENSION_MAP,
    MAX_SEARCH_RESULTS,
    IGNORED_DIRECTORIES,
)

from assistant.utils.platform import PlatformManager
SEARCH_DIRECTORIES = PlatformManager.get_search_directories()

class FileSearchTool(BaseTool):

    name = "file_search"

    description = "Search local files by filename."

    tool_type = ToolType.REASONING

    parameters = {
        "query": "string"
    }

    examples = [
        "Find my resume",
        "Search README",
        "Find report.pdf",
        "Find Python files",
        "Search invoice"
    ]

    def execute(
        self,
        query: str,
        extension: str | None = None,
        **kwargs
    ):

        query = Path(query).stem.lower().strip()

        # Convert extension alias to actual extensions
        allowed_extensions = None

        if extension:
            extension = extension.lower().lstrip(".")

            if extension in EXTENSION_MAP:
                allowed_extensions = EXTENSION_MAP[extension]
            else:
                allowed_extensions = ["." + extension]

        results = []

        for search_directory in SEARCH_DIRECTORIES:

            if not os.path.exists(search_directory):
                continue

            for root, dirs, files in os.walk(search_directory):

                # Skip ignored folders
                dirs[:] = [
                    d for d in dirs
                    if d not in IGNORED_DIRECTORIES
                ]

                for filename in files:

                    filepath = Path(root) / filename

                    suffix = filepath.suffix.lower()

                    # Filter by extension if requested
                    if (
                        allowed_extensions is not None
                        and suffix not in allowed_extensions
                    ):
                        continue

                    name = filepath.stem.lower()

                    if query not in name:
                        continue

                    try:
                        stat = filepath.stat()

                        # ---------- Relevance Score ----------
                        score = 0

                        if name == query:
                            score += 100

                        elif name.startswith(query):
                            score += 80

                        elif query in name:
                            score += 50

                        if suffix in {
                            ".pdf",
                            ".docx",
                            ".txt",
                            ".md",
                        }:
                            score += 10

                        modified = stat.st_mtime

                        results.append({
                            "name": filepath.name,
                            "path": str(filepath),
                            "extension": suffix,
                            "size": stat.st_size,
                            "modified": modified,
                            "score": score,
                        })

                        # Stop searching after collecting enough matches
                        if len(results) >= MAX_SEARCH_RESULTS:
                            break

                    except OSError:
                        continue

                if len(results) >= MAX_SEARCH_RESULTS:
                    break

            if len(results) >= MAX_SEARCH_RESULTS:
                break

        # No matches
        if not results:
            return {
                "success": False,
                "response": "I couldn't find that file.",
                "data": None,
                "llm": False
            }

        # Best match first
        results.sort(
            key=lambda x: (
                x["score"],
                x["modified"],
            ),
            reverse=True,
        )

        best = results[0]

        return {
            "success": True,
            "response": None,
            "data": best,
            "llm": False
        }