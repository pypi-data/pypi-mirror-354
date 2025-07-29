"""permalint: Lint URLs.

Exports:
    - normalize_url: Normalize URLs so it's easy to figure out canonical
      sources of truth for packages
"""

from __future__ import annotations

import warnings
from urllib.parse import ParseResult, urlparse

MIN_GITHUB_URL_PARTS = 2
MULTIPLE_DOMAINS = 2


def _only_protocol(url: str) -> bool:
    """Check if a URL is only a protocol."""
    return url.strip() in (
        "http://",
        "https://",
        "git://",
        "ssh://",
        "git+ssh://",
        "git+https://",
    )


def _is_malformed(url: str) -> bool:
    """Check if a URL is malformed."""
    try:
        urlparse(url)
    except ValueError:
        return True
    return False


def normalize_url(url: str) -> str:
    """Normalize a URL according to CHAI database rules.

    It could return an empty string if the URL is only the protocol

    - Ignore protocol (http, https, etc.)
    - For GitHub URLs, keep only owner/repo
    - Remove query strings and fragments
    - Remove trailing slashes
    - Lowercase the domain
    - Remove .git suffix
    - Handle SSH GitHub URLs (git@github.com:user/repo)
    - Handle git+ssh and git+https GitHub URLs.
    """
    # early warnings
    if _only_protocol(url):
        warnings.warn(
            f"Malformed URL with only protocol: '{url}', returning ''",
            UserWarning,
            stacklevel=2,
        )
        return ""

    # first, remove the .git suffix if it exists
    url = url.removesuffix(".git")

    # now, handle specific git style URLs: ssh, https, and git

    # ssh-style GitHub URLs
    if url.startswith("git@github.com:"):
        url = url.replace("git@github.com:", "github.com/")

    # git+ssh style GitHub URLs
    if url.startswith("git+ssh://git@github.com/"):
        url = url.replace("git+ssh://git@github.com/", "github.com/")

    # git+https style GitHub URLs
    if url.startswith("git+https://github.com/"):
        url = url.replace("git+https://github.com/", "github.com/")

    if _is_malformed(url):
        warnings.warn(
            f"Malformed URL: '{url}', returning ''",
            UserWarning,
            stacklevel=2,
        )
        return ""

    parsed = urlparse(url)

    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")

    # Remove www. for consistency
    netloc = netloc.removeprefix("www.")

    # GitHub special handling
    if netloc == "github.com":
        parts = [p for p in path.split("/") if p]
        if len(parts) >= MIN_GITHUB_URL_PARTS:
            path = f"{parts[0]}/{parts[1]}"
        elif parts:
            path = parts[0]
        else:
            path = ""
        return f"github.com/{path}".rstrip("/")

    # Remove query and fragment, ignore protocol
    result = f"{netloc}{path}" if netloc else path

    # Remove .git suffix if present - handle this once at the end
    return result.removesuffix(".git")


def guess_url(urls: list[str]) -> str | None:
    """Given a list of URLs, return the most likely canonical URL."""
    results: set[ParseResult] = set()
    for url in urls:
        normalized = normalize_url(url)
        if normalized in urls:
            results.add(normalized)

    if len(results) == 1:
        return results.pop()
    return None


def _add_name_with_lowercase(names: list[str], name: str) -> None:
    """Add a name to the list, and its lowercase variant if different.

    NOTE: I don't like this, ideally upstream application should handle
    searching by whatever case, but this is fine for now.
    """
    names.append(name)
    if name.lower() != name:
        names.append(name.lower())


def possible_names(url: str) -> list[str]:
    """Given a URL, return a list of possible names for the package.

    The list is ordered by relevance to the input. The original URL is always
    the first element in the returned list.

    For known hosting platforms (github.com, gitlab.com, bitbucket.org),
    extracts the repository name. For other recognizable services, extracts
    the most relevant identifier.
    """
    # early warnings
    if _only_protocol(url) or _is_malformed(url):
        warnings.warn(
            f"Invalid URL: '{url}', returning []",
            UserWarning,
            stacklevel=2,
        )
        return []

    # Treat the schema
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.strip("/")

    # Remove www. for consistency
    netloc = netloc.removeprefix("www.")

    names = []

    # Always add the full URL first
    if path:
        full_path = f"{netloc}/{path}"
        names.append(full_path)
    else:
        names.append(netloc)

    # Handle specific known platforms and services
    if netloc in ("github.com", "gitlab.com", "bitbucket.org") and path:
        # For code hosting platforms, extract repository name (last segment)
        last_segment = path.split("/")[-1]
        _add_name_with_lowercase(names, last_segment)
    elif netloc == "gist.github.com" and path:
        # For GitHub gists, only return the full URL since there's no
        # meaningful repo name
        pass
    elif netloc.endswith(".github.com") and path:
        # For GitHub pages, extract project name (last segment)
        last_segment = path.split("/")[-1]
        names.append(last_segment)
    elif netloc == "cloud.google.com" and path:
        # For Google Cloud, extract service name (first segment)
        first_segment = path.split("/")[0]
        names.append(first_segment)
    elif netloc.endswith(".sourceforge.net"):
        # For SourceForge, extract subdomain
        subdomain = netloc.split(".")[0]
        names.append(subdomain)
    elif path:
        # For other URLs with paths, extract last segment
        last_segment = path.split("/")[-1]
        _add_name_with_lowercase(names, last_segment)
    else:
        # Domain-only URLs
        domain_parts = netloc.split(".")
        if len(domain_parts) > 1:
            if len(domain_parts) > MULTIPLE_DOMAINS:
                # For cases like poppler.freedesktop.org, only extract the
                # subdomain, since the middle domain (freedesktop) is not
                # typically a package name
                names.append(domain_parts[0])  # e.g., "poppler"
            else:
                # For cases like elfutils.org
                names.append(domain_parts[0])  # e.g., "elfutils"

    return names


def is_canonical_url(url: str) -> bool:
    """Check if a URL is canonical."""
    if url == "":
        return False
    return normalize_url(url) == url


if __name__ == "__main__":
    print(possible_names("https://github.com/ethereum/web3.js#readme"))
