from __future__ import annotations
import base64
import re
import typing as _t
from dataclasses import dataclass

import requests

__all__ = ["DynamicFileImporter"]

# ---------------------------------------------------------------------------
# Utility data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _TreeEntry:
    """Represents a path inside the repo tree"""

    path: str  # POSIX path inside the repo, e.g. "folder/file.txt"
    type: str  # "blob" or "tree"
    sha: str


# ---------------------------------------------------------------------------
# Core implementation
# ---------------------------------------------------------------------------


class DynamicFileImporter:
    """Root object mirroring a GitHub repo’s folder structure, allowing
    retrieval of text-based files as plain text.

    Supports common text extensions but disallows binaries (including PDFs).

    Parameters
    ----------
    repo : str
        Repository spec in the form "owner/name".
    token : str | None
        GitHub personal access token for higher rate limits.
    branch : str, default "main"
        Branch, tag, or commit SHA to fetch from.
    preload : bool, default False
        If True, pre-fetch the full repo tree on init.
    """

    _TREE_API = "https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1"
    _BRANCH_API = "https://api.github.com/repos/{repo}/branches/{branch}"
    _BLOB_API = "https://api.github.com/repos/{repo}/git/blobs/{sha}"

    # Valid text file extensions
    _TEXT_EXTS = {".md", ".py", ".txt", ".json", ".yaml", ".yml", ".csv", ".rst"}

    # Regex for sanitizing identifiers
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

        self._tree: list[_TreeEntry] | None = None
        self._file_cache: dict[str, str] = {}
        if preload:
            _ = self._get_tree()

    def reload(self) -> None:
        """Clear caches and fetch a fresh repo tree"""
        self._tree = None
        self._file_cache.clear()
        _ = self._get_tree()

    def get_file_content(self, path: str) -> str:
        """Return file contents of a text file in the repo as a string.

        Parameters
        ----------
        path : str
            POSIX path to a file in the repo, including extension.

        Returns
        -------
        str
            File contents as decoded UTF-8 text.

        Raises
        ------
        FileNotFoundError
            If the path does not exist in the repo.
        RuntimeError
            If the file extension is not supported.
        """
        normalized = path.lstrip("/").replace("\\", "/")
        for entry in self._get_tree():
            if entry.path == normalized:
                return self._fetch_text(entry)
        raise FileNotFoundError(f"File not found: {path}")

    def __getattr__(self, item: str):
        # Allow attribute access for top-level directories
        ident = self._unsanitize(item)
        for entry in self._get_tree():
            if entry.path.startswith(f"{ident}/"):
                return _DirProxy(self, ident)
        raise AttributeError(item)

    def __dir__(self):
        base = set(super().__dir__())
        children = {self._sanitize(p.split("/", 1)[0]) for p in self._list_children("")}
        return sorted(base.union(children))

    def _get_tree(self) -> list[_TreeEntry]:
        if self._tree is not None:
            return self._tree
        # Fetch branch commit SHA
        r = self._session.get(
            self._BRANCH_API.format(repo=self._repo, branch=self._branch), timeout=30
        )
        r.raise_for_status()
        commit_sha = r.json()["commit"]["sha"]
        # Fetch full tree
        r = self._session.get(
            self._TREE_API.format(repo=self._repo, sha=commit_sha), timeout=60
        )
        r.raise_for_status()
        raw = r.json().get("tree", [])
        self._tree = [_TreeEntry(e["path"], e["type"], e["sha"]) for e in raw]
        return self._tree

    def _list_children(self, prefix: str) -> list[str]:
        prefix = prefix.rstrip("/")
        seen = set()
        for entry in self._get_tree():
            if prefix and not entry.path.startswith(prefix + "/"):
                continue
            rest = entry.path[len(prefix) + 1 :] if prefix else entry.path
            seen.add(rest.split("/", 1)[0])
        return list(seen)

    def _fetch_text(self, entry: _TreeEntry) -> str:
        """Fetch and decode text blobs, caching results"""
        if entry.path in self._file_cache:
            return self._file_cache[entry.path]
        # Download blob
        r = self._session.get(
            self._BLOB_API.format(repo=self._repo, sha=entry.sha), timeout=30
        )
        r.raise_for_status()
        data = r.json()
        if data.get("encoding") != "base64":
            raise RuntimeError("Unexpected blob encoding")
        raw = base64.b64decode(data["content"])
        ext = "." + entry.path.rsplit(".", 1)[-1].lower()
        if ext not in self._TEXT_EXTS:
            raise RuntimeError(f"Unsupported file type: {ext}")
        text = raw.decode("utf-8", errors="replace")
        self._file_cache[entry.path] = text
        return text

    @classmethod
    def _sanitize(cls, name: str) -> str:
        sanitized = cls._IDENT_RE.sub("_", name)
        if sanitized and sanitized[0].isdigit():
            sanitized = "_" + sanitized
        return sanitized

    @classmethod
    def _unsanitize(cls, ident: str) -> str:
        return ident.replace("_", "-")


class _DirProxy:
    """Proxy for subdirectories to support attribute access"""

    def __init__(self, importer: DynamicPromptImporter, prefix: str):
        self._importer = importer
        self._prefix = prefix.rstrip("/")

    def __getattr__(self, item: str):
        ident = self._importer._unsanitize(item)
        path = f"{self._prefix}/{ident}"
        # If subdirectory has further children, return proxy
        for entry in self._importer._get_tree():
            if entry.path.startswith(path + "/"):
                return _DirProxy(self._importer, path)
        raise AttributeError(item)

    def __dir__(self):
        children = self._importer._list_children(self._prefix)
        return [self._importer._sanitize(c.rsplit(".", 1)[0]) for c in children]

    def __repr__(self):
        return f"<DynamicPromptDir '{self._prefix}' @ {self._importer._repo}>"
