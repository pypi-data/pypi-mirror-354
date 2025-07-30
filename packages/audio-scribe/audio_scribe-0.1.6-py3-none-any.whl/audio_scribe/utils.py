"""Utility functions and classes for Audio Scribe."""

import os
import glob
import logging
import importlib.metadata
from typing import List, Optional, Dict
from importlib.metadata import PackageNotFoundError

logger = logging.getLogger(__name__)


def complete_path(text: str, state: int) -> Optional[str]:
    """
    Return the 'state'-th completion for 'text'.
    This function will be used by 'readline' to enable file path autocompletion.
    """
    # If the user typed a glob pattern (with * or ?)
    if "*" in text or "?" in text:
        matches: List[str] = sorted(glob.glob(text))
    else:
        # Split off the directory name and partial file/directory name
        directory, partial = os.path.split(text)
        if not directory:
            directory = "."
        try:
            # List everything in 'directory' that starts with 'partial'
            entries = sorted(os.listdir(directory))
        except OSError:
            # If directory doesn't exist or we lack permission, no matches
            entries = []

        matches = []
        for entry in entries:
            if entry.startswith(partial):
                if directory == ".":
                    # Don't prefix current directory paths
                    full_path = entry
                else:
                    # Keep the directory prefix for subdirectories
                    full_path = os.path.join(directory, entry)

                # If it's a directory, add a trailing slash to indicate that
                if os.path.isdir(full_path) and not full_path.endswith(os.path.sep):
                    full_path += os.path.sep
                matches.append(full_path)

    # If 'state' is beyond last match, return None
    return matches[state] if state < len(matches) else None


class DependencyManager:
    """Manages and verifies system dependencies."""

    REQUIRED_PACKAGES: Dict[str, Optional[str]] = {
        "torch": None,
        "pyannote.audio": None,
        "openai-whisper": None,
        "pytorch-lightning": None,
        "keyring": None,
    }

    @classmethod
    def verify_dependencies(cls) -> bool:
        """
        Verify all required dependencies are installed with correct versions.
        Returns True if all are installed and correct, False otherwise.
        """
        missing: List[str] = []
        outdated: List[str] = []

        for package, required_version in cls.REQUIRED_PACKAGES.items():
            try:
                installed_version = importlib.metadata.version(package)
                if required_version and installed_version != required_version:
                    outdated.append(
                        f"{package} (installed: {installed_version}, required: {required_version})"
                    )
            except PackageNotFoundError:
                missing.append(package)

        if missing or outdated:
            if missing:
                logger.error("Missing packages: %s", ", ".join(missing))
            if outdated:
                logger.error("Outdated packages: %s", ", ".join(outdated))
            logger.info(
                "Install required packages: pip install %s",
                " ".join(
                    f"{pkg}=={ver}" if ver else pkg
                    for pkg, ver in cls.REQUIRED_PACKAGES.items()
                ),
            )
            return False
        return True
