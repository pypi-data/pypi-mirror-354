"""Dynamic Prompt Importer
===========================
A small utility that lets you treat a GitHub repository full of Markdown
prompts as a first-class Python object.  Example:

>>> from dynamic_prompt_importer import DynamicPromptImporter
>>> dpi = DynamicPromptImporter("octo-org/awesome-prompts", "ghp_…TOKEN…")
>>> dpi.marketing.welcome   # => str with the contents of marketing/welcome.md

Autocompletion works out-of-the-box because every directory and file is
exposed as an attribute and ``__dir__`` enumerates each level’s children.
Only ``*.md`` files are exposed; other paths are ignored for safety.
"""

from __future__ import annotations
import base64
import functools
import re
import typing as _t
from dataclasses import dataclass

import requests

__all__ = ["DynamicPromptImporter"]

# ---------------------------------------------------------------------------
# Utility data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _TreeEntry:  # Represents a path inside the repo tree
    path: str  # e.g. "folder/file.md" (always POSIX with "/")
    type: str  # "blob" or "tree"
    sha: str


# ---------------------------------------------------------------------------
# Core implementation
# ---------------------------------------------------------------------------


class DynamicPromptImporter:
    """Root object that mirrors a GitHub repo’s folder structure.

    Parameters
    ----------
    repo : str
        Repository spec in the form ``"owner/name"``.
    token : str | None
        GitHub personal access token (can be ``None`` for public repos but
        rate-limited).
    branch : str, default "main"
        Which branch/ref to pull.  Use a tag or commit SHA for immutability.
    preload : bool, default False
        If *True* the entire repo tree is fetched immediately; otherwise it is
        fetched lazily when first accessed.
    """

    _TREE_API = "https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1"
    _BRANCH_API = "https://api.github.com/repos/{repo}/branches/{branch}"
    _BLOB_API = "https://api.github.com/repos/{repo}/git/blobs/{sha}"

    # regex used to map file or dir names → valid python identifiers
    _IDENT_RE = re.compile(r"[^0-9a-zA-Z_]")

    def __init__(
        self,
        repo: str,
        token: str | None = None,
        *,
        branch: str = "main",
        preload: bool = False,
    ):
        self._repo = repo
        self._token = token
        self._branch = branch

        self._session = requests.Session()
        if token:
            self._session.headers.update({"Authorization": f"token {token}"})
        self._session.headers.update({"User-Agent": "dynamic-prompt-importer/0.1"})

        # Will be populated on first access (or now if preload)
        self._tree: list[_TreeEntry] | None = None
        self._file_cache: dict[str, str] = {}

        if preload:
            _ = self._get_tree()

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------

    def reload(self) -> None:
        """Clear caches and fetch a fresh copy of the repo tree."""
        self._tree = None
        self._file_cache.clear()
        _ = self._get_tree()

    def get_file_content(self, path: str) -> str:
        """Return the contents of *path* from the repository.

        Parameters
        ----------
        path : str
            Repository-relative POSIX path to a Markdown file. The ``.md``
            extension may be omitted.

        Returns
        -------
        str
            The file contents as text.
        """

        path = path.lstrip("/").replace("\\", "/")
        if not path.endswith(".md"):
            path = f"{path}.md"

        for entry in self._get_tree():
            if entry.path == path:
                return self._get_file_text(entry.path)

        raise FileNotFoundError(path)

    # ---------------------------------------------------------------------
    # Dunder methods to expose folders/files as attributes
    # ---------------------------------------------------------------------

    def __getattr__(self, item: str):
        # Called only if attribute *item* is not found by normal means.
        # Interpret *item* as either a subdirectory or markdown file.
        ident = self._unsanitize(item)
        node_path = ident  # relative path under repo root

        # Is there at least one tree entry that begins with this path?
        for entry in self._get_tree():
            if entry.path == f"{node_path}.md":
                return self._get_file_text(entry.path)  # direct file hit
            if entry.path.startswith(f"{node_path}/"):
                # It's a sub-directory → return a *Proxy* representing that folder
                return _DirProxy(self, node_path)

        raise AttributeError(item)

    # For autocompletion support (e.g. in ipython/IDE)
    def __dir__(self):
        base = set(super().__dir__())
        children = {self._sanitize(p.split("/", 1)[0]) for p in self._list_children("")}
        return sorted(base.union(children))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_tree(self) -> list[_TreeEntry]:
        if self._tree is not None:
            return self._tree

        # 1. Resolve branch → commit SHA
        r = self._session.get(
            self._BRANCH_API.format(repo=self._repo, branch=self._branch), timeout=30
        )
        r.raise_for_status()
        commit_sha: str = r.json()["commit"]["sha"]

        # 2. Download full recursive tree (single API call!)
        r = self._session.get(
            self._TREE_API.format(repo=self._repo, sha=commit_sha), timeout=60
        )
        r.raise_for_status()
        raw_tree = r.json()["tree"]

        self._tree = [_TreeEntry(e["path"], e["type"], e["sha"]) for e in raw_tree]
        return self._tree

    def _list_children(self, prefix: str) -> list[str]:
        """Return immediate child names under *prefix* (a directory path)."""
        prefix = prefix.rstrip("/")
        seen = set()
        for entry in self._get_tree():
            if prefix:
                if not entry.path.startswith(prefix + "/"):
                    continue
                remainder = entry.path[len(prefix) + 1 :]
            else:
                remainder = entry.path
            name = remainder.split("/", 1)[0]
            if name not in seen:
                seen.add(name)
        return list(seen)

    def _get_file_text(self, path: str) -> str:
        """Fetch a blob’s raw text, caching on first download."""
        if path in self._file_cache:
            return self._file_cache[path]

        # Look up the SHA for this path from the previously obtained tree
        sha = next(e.sha for e in self._get_tree() if e.path == path)
        r = self._session.get(
            self._BLOB_API.format(repo=self._repo, sha=sha), timeout=30
        )
        r.raise_for_status()
        data = r.json()
        if data.get("encoding") != "base64":
            raise RuntimeError("Unexpected blob encoding – expected base64")
        text = base64.b64decode(data["content"]).decode()
        self._file_cache[path] = text
        return text

    # ------------------------------------------------------------------
    # Identifier sanitization helpers
    # ------------------------------------------------------------------

    @classmethod
    def _sanitize(cls, name: str) -> str:
        """Make *name* a valid Python identifier."""
        name = cls._IDENT_RE.sub("_", name)
        if name and name[0].isdigit():
            name = "_" + name
        return name

    @classmethod
    def _unsanitize(cls, ident: str) -> str:
        # NOTE: This naive impl assumes original names didn’t clash. We simply
        # reverse underscores back to hyphens & dots where appropriate so that
        # "file_md" maps back to "file.md".
        # Future: maintain explicit mapping in _get_tree.
        return ident.replace("_", "-")


class _DirProxy:
    """Proxy object representing a sub-directory within the repo."""

    def __init__(self, importer: DynamicPromptImporter, prefix: str):
        self._importer = importer
        self._prefix = prefix.rstrip("/")

    # Dynamically dispatch deeper
    def __getattr__(self, item: str):
        ident = self._importer._unsanitize(item)
        node_path = f"{self._prefix}/{ident}" if self._prefix else ident

        for entry in self._importer._get_tree():
            if entry.path == f"{node_path}.md":
                return self._importer._get_file_text(entry.path)
            if entry.path.startswith(f"{node_path}/"):
                return _DirProxy(self._importer, node_path)

        raise AttributeError(item)

    def __dir__(self):
        children = self._importer._list_children(self._prefix)
        return [
            self._importer._sanitize(ch.split("/", 1)[0].rsplit(".", 1)[0])
            for ch in children
        ]

    # Nice repr for the REPL
    def __repr__(self):
        return f"<DynamicPromptDir {self._prefix!r} @ {self._importer._repo}>"


# ---------------------------------------------------------------------------
# Convenience API shortcut (so user can `import dynamic_prompt_importer as dpi`)
# ---------------------------------------------------------------------------

# Users may prefer `import dynamic_prompt_importer as dpi` and then
# `dpi.DynamicPromptImporter`.
