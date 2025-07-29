import base64
import types
import sys
from unittest.mock import MagicMock

import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create a minimal stub for the requests module since the real package may not
# be installed in the test environment.
class DummySession:
    def __init__(self):
        self.headers = {}
    def get(self, url, timeout=None):
        return fake_get(url)

def fake_get(url, *args, **kwargs):
    response = MagicMock()
    response.raise_for_status = lambda: None
    if url.endswith("/branches/main"):
        response.json.return_value = {"commit": {"sha": "sha-main"}}
    elif url.endswith("/git/trees/sha-main?recursive=1"):
        response.json.return_value = {
            "tree": [
                {"path": "folder/example.md", "type": "blob", "sha": "sha-blob"},
                {"path": "another-file.md", "type": "blob", "sha": "sha-blob2"},
                {"path": "bad-encoding.md", "type": "blob", "sha": "sha-bad"},
            ]
        }
    elif url.endswith("/git/blobs/sha-blob"):
        content = base64.b64encode(b"Test prompt").decode()
        response.json.return_value = {"encoding": "base64", "content": content}
    elif url.endswith("/git/blobs/sha-blob2"):
        content = base64.b64encode(b"Another prompt").decode()
        response.json.return_value = {"encoding": "base64", "content": content}
    elif url.endswith("/git/blobs/sha-bad"):
        response.json.return_value = {"encoding": "utf-8", "content": "oops"}
    else:
        raise AssertionError(f"Unexpected URL: {url}")
    return response

# Register the stubbed requests module
sys.modules['requests'] = types.SimpleNamespace(Session=DummySession)

from dynamic_prompt_importer import DynamicPromptImporter


def test_prompt_fetching():
    """Fetching a prompt via attribute access returns its contents."""
    print("[info] test_prompt_fetching - fetching 'folder/example.md'")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.folder.example
    assert text == "Test prompt"


def test_get_file_content():
    """get_file_content should retrieve a file explicitly."""
    print("[info] test_get_file_content - explicit file fetch")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.get_file_content("folder/example")
    assert text == "Test prompt"


def test_attribute_sanitization():
    """Attributes with unsafe characters are sanitized."""
    print("[info] test_attribute_sanitization - attribute name sanitization")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.another_file
    assert text == "Another prompt"


def test_dir_listing_and_reload():
    """dir() should list children and reload() clears caches."""
    print("[info] test_dir_listing_and_reload - dir listing and reload")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    _ = importer.folder.example  # prime cache
    assert "folder" in dir(importer)
    assert "example" in dir(importer.folder)
    assert importer._file_cache
    importer.reload()
    assert not importer._file_cache


def test_missing_attribute():
    """Accessing a missing attribute should raise AttributeError."""
    print("[info] test_missing_attribute - expect AttributeError")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    with pytest.raises(AttributeError):
        _ = importer.no_such_file


def test_get_file_content_missing():
    """get_file_content should raise when the file does not exist."""
    print("[info] test_get_file_content_missing - expect FileNotFoundError")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    with pytest.raises(FileNotFoundError):
        importer.get_file_content("folder/not_there")


def test_bad_blob_encoding():
    """Unexpected blob encoding should raise a RuntimeError."""
    print("[info] test_bad_blob_encoding - expect RuntimeError for encoding")
    importer = DynamicPromptImporter("owner/repo", preload=True)
    with pytest.raises(RuntimeError):
        importer.get_file_content("bad-encoding")
