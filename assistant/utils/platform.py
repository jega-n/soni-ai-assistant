import platform
from pathlib import Path


class PlatformManager:

    @staticmethod
    def get_search_directories():

        system = platform.system()

        if system == "Windows":
            return [
                Path.home() / "Desktop",
                Path.home() / "Documents",
                Path.home() / "Downloads",
            ]

        elif system == "Linux":
            return [
                Path.home() / "Desktop",
                Path.home() / "Documents",
                Path.home() / "Downloads",
            ]

        elif system == "Android":
            # Placeholder for future Android implementation
            return []

        return []