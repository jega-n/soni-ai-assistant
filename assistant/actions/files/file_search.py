import os
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

    planner_visible = True

    tool_type = ToolType.REASONING

    parameters = {
        "query": "string"
    }

    def execute(
        self,
        query: str,
        extension: str | None = None,
        **kwargs
    ):

        query = Path(query).stem.lower().strip()

        allowed_extensions = None

        if extension:
            extension = extension.lower().lstrip(".")

            allowed_extensions = (
                EXTENSION_MAP.get(extension, ["." + extension])
            )

        results = []

        for search_directory in SEARCH_DIRECTORIES:

            if not os.path.exists(search_directory):
                continue

            for root, dirs, files in os.walk(search_directory):

                dirs[:] = [
                    d for d in dirs
                    if d not in IGNORED_DIRECTORIES
                ]

                for filename in files:

                    filepath = Path(root) / filename

                    suffix = filepath.suffix.lower()

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

                        score = 0

                        if name == query:
                            score += 100
                        elif name.startswith(query):
                            score += 80
                        else:
                            score += 50

                        if suffix in {
                            ".pdf",
                            ".docx",
                            ".txt",
                            ".md",
                        }:
                            score += 10

                        results.append({
                            "name": filepath.name,
                            "path": str(filepath),
                            "extension": suffix,
                            "size": stat.st_size,
                            "modified": stat.st_mtime,
                            "score": score,
                        })

                    except OSError:
                        continue

        if not results:

            return {
                "success": False,
                "response": "I couldn't find that file.",
                "data": None,
                "llm": False
            }

        results.sort(
            key=lambda x: (
                x["score"],
                x["modified"]
            ),
            reverse=True
        )

        best = results[0]

        return {
            "success": True,
            "response": f"I found '{best['name']}' in '{best['path']}'.",
            "data": best,
            "llm": False
        }