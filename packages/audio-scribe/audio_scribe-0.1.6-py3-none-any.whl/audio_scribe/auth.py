"""Authentication and token management for Audio Scribe."""

import os
import json
import base64
import logging
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)


class TokenManager:
    """Handles secure storage and retrieval of the Hugging Face authentication token."""

    def __init__(self):
        # Store config in ~/.pyannote/config.json
        self.config_dir = Path.home() / ".pyannote"
        self.config_file = self.config_dir / "config.json"
        self._initialize_config()

    def _initialize_config(self) -> None:
        """Initialize configuration directory and file with secure permissions."""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self._save_config({})

        # Set secure file and directory permissions on POSIX systems
        if os.name == "posix":
            os.chmod(self.config_dir, 0o700)
            os.chmod(self.config_file, 0o600)

    def _get_encryption_key(self) -> bytes:
        """Generate an encryption key from system-specific data."""
        salt = b"pyannote-audio-salt"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(str(Path.home()).encode())
        return base64.urlsafe_b64encode(key)

    def _save_config(self, config: dict) -> None:
        """Securely save configuration to file."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f)

    def _load_config(self) -> dict:
        """Load configuration from file."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def store_token(self, token: str) -> bool:
        """Securely store authentication token."""
        try:
            fernet = Fernet(self._get_encryption_key())
            encrypted_token = fernet.encrypt(token.encode())

            config = self._load_config()
            config["token"] = encrypted_token.decode()

            self._save_config(config)
            return True
        except Exception as e:
            logger.error(f"Failed to store token: {e}")
            return False

    def retrieve_token(self) -> Optional[str]:
        """Retrieve stored authentication token."""
        try:
            config = self._load_config()
            if "token" in config:
                fernet = Fernet(self._get_encryption_key())
                return fernet.decrypt(config["token"].encode()).decode()
        except Exception as e:
            logger.error(f"Failed to retrieve token: {e}")
        return None

    def delete_token(self) -> bool:
        """Delete stored authentication token."""
        try:
            config = self._load_config()
            if "token" in config:
                del config["token"]
                self._save_config(config)
            return True
        except Exception as e:
            logger.error(f"Failed to delete token: {e}")
            return False


def get_token(token_manager: TokenManager) -> Optional[str]:
    """Get authentication token from storage or user input."""
    stored_token = token_manager.retrieve_token()
    if stored_token:
        choice = input("\nUse the stored Hugging Face token? (y/n): ").lower().strip()
        if choice == "y":
            return stored_token

    print("\nA HuggingFace token is required for speaker diarization.")
    print("Get your token at: https://huggingface.co/settings/tokens")
    print("\nEnsure you have accepted:")
    print("  1. pyannote/segmentation-3.0 conditions")
    print("  2. pyannote/speaker-diarization-3.1 conditions")

    token = input("\nEnter HuggingFace token: ").strip()
    if token:
        choice = input("Save token for future use? (y/n): ").lower().strip()
        if choice == "y":
            if token_manager.store_token(token):
                print("Token saved successfully.")
            else:
                print("Failed to save token. It will be used for this session only.")
    return token if token else None
