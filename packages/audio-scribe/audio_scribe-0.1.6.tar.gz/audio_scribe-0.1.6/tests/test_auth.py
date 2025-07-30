"""Tests for authentication and token management."""

import os
import pytest
from unittest.mock import patch, Mock
from src.audio_scribe.auth import TokenManager, get_token


@pytest.fixture
def token_manager(tmp_dir):
    """Create a TokenManager with a temporary config directory."""
    tm = TokenManager()
    tm.config_dir = tmp_dir
    tm.config_file = tm.config_dir / "config.json"
    tm._initialize_config()
    return tm


def test_token_manager_initialization(token_manager, tmp_dir):
    """Test TokenManager initialization and file creation."""
    assert token_manager.config_dir == tmp_dir
    assert token_manager.config_file.exists()
    if os.name == "posix":
        assert oct(token_manager.config_file.stat().st_mode)[-3:] == "600"
        assert oct(token_manager.config_dir.stat().st_mode)[-3:] == "700"


def test_token_store_retrieve(token_manager):
    """Test storing and retrieving a token."""
    test_token = "test-token-12345"

    # Store token
    assert token_manager.store_token(test_token) is True

    # Retrieve token
    retrieved = token_manager.retrieve_token()
    assert retrieved == test_token


def test_token_delete(token_manager):
    """Test deleting a stored token."""
    # Store and verify
    token_manager.store_token("test-token")
    assert token_manager.retrieve_token() is not None

    # Delete and verify
    assert token_manager.delete_token() is True
    assert token_manager.retrieve_token() is None


def test_get_token_stored(token_manager, monkeypatch):
    """Test get_token using a stored token."""
    token_manager.store_token("stored-token")
    monkeypatch.setattr("builtins.input", lambda _: "y")

    assert get_token(token_manager) == "stored-token"


def test_get_token_new_save(token_manager, monkeypatch):
    """Test get_token with new token and saving."""
    responses = iter(["new-token-123", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    token = get_token(token_manager)
    assert token == "new-token-123"
    assert token_manager.retrieve_token() == "new-token-123"


def test_get_token_new_dont_save(token_manager, monkeypatch):
    """Test get_token with new token without saving."""
    responses = iter(["another-token", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    token = get_token(token_manager)
    assert token == "another-token"
    assert token_manager.retrieve_token() is None


def test_get_token_none(token_manager, monkeypatch):
    """Test get_token when user provides no input."""
    responses = iter(["", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert get_token(token_manager) is None


def test_encryption_different_machines(token_manager):
    """Test that tokens are properly encrypted/decrypted."""
    test_token = "test-token-encryption"

    # Store token
    token_manager.store_token(test_token)

    # Verify stored data is not plaintext
    with open(token_manager.config_file, "r") as f:
        stored_data = f.read()
    assert test_token not in stored_data

    # But we can still retrieve it
    assert token_manager.retrieve_token() == test_token


def test_token_manager_initialization_error(token_manager, tmp_dir):
    """Test TokenManager initialization with permission errors."""
    with patch("json.dump", side_effect=PermissionError), patch(
        "builtins.open", create=True
    ) as mock_open:
        mock_open.return_value.__enter__ = lambda x: x
        mock_open.return_value.__exit__ = Mock()

        # This should handle the error gracefully
        token_manager._initialize_config()


def test_token_store_permission_error(token_manager):
    """Test storing token with file permission errors."""
    with patch("json.dump", side_effect=PermissionError):
        assert token_manager.store_token("test-token") is False


def test_token_retrieve_corrupted_config(token_manager):
    """Test retrieving token with corrupted config file."""
    # Write invalid JSON to config file
    with open(token_manager.config_file, "w") as f:
        f.write("invalid json")

    assert token_manager.retrieve_token() is None


def test_token_delete_permission_error(token_manager):
    """Test deleting token with permission errors."""
    # First store a token
    token_manager.store_token("test-token")

    with patch("json.dump", side_effect=PermissionError):
        assert token_manager.delete_token() is False


def test_get_token_invalid_choice(token_manager, monkeypatch):
    """Test get_token with invalid user input."""
    token_manager.store_token("stored-token")

    # Create a list to track input calls
    inputs = []

    def mock_input(prompt):
        inputs.append(prompt)
        if "Use the stored" in prompt:
            return "invalid" if len(inputs) == 1 else "n"
        if "Enter HuggingFace token" in prompt:
            return "new-test-token"
        if "Save token" in prompt:
            return "n"
        return "n"  # default response

    monkeypatch.setattr("builtins.input", mock_input)

    token = get_token(token_manager)
    assert token == "new-test-token"
    # Verify we got the expected prompts
    assert len(inputs) >= 3, "Expected at least 3 prompts"
    assert any("Use the stored" in prompt for prompt in inputs)
    assert any("Enter HuggingFace token" in prompt for prompt in inputs)
    assert any("Save token" in prompt for prompt in inputs)


def test_encryption_error_handling(token_manager):
    """Test encryption error handling in token storage."""
    with patch(
        "cryptography.fernet.Fernet.encrypt", side_effect=Exception("Encryption failed")
    ):
        assert token_manager.store_token("test-token") is False


def test_decryption_error_handling(token_manager):
    """Test decryption error handling in token retrieval."""
    # Store an invalid encrypted token
    config = token_manager._load_config()
    config["token"] = "invalid-encrypted-data"
    token_manager._save_config(config)

    assert token_manager.retrieve_token() is None
