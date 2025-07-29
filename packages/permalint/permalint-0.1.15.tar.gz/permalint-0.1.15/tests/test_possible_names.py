import pytest

from permalint import possible_names


@pytest.mark.parametrize(
    ("input_name", "probable_names"),
    [
        (
            "https://taku910.github.io/mecab/",
            ["taku910.github.io/mecab", "mecab"],
        ),
        (
            "https://taku910.github.io/mecab-ipadic/",
            ["taku910.github.io/mecab-ipadic", "mecab-ipadic"],
        ),
        # in this case, the last path segment is the name
        ("mozilla.org/cbindgen", ["mozilla.org/cbindgen", "cbindgen"]),
        # for freedesktop.org, we only care about the domain name
        (
            "poppler.freedesktop.org",
            ["poppler.freedesktop.org", "poppler"],
        ),
        # since there's a path, we're only interseted in that last segment.
        (
            "poppler.freedesktop.org/poppler-data",
            ["poppler.freedesktop.org/poppler-data", "poppler-data"],
        ),
        ("elfutils.org", ["elfutils.org", "elfutils"]),
        ("hdfgroup.org/HDF5", ["hdfgroup.org/HDF5", "HDF5", "hdf5"]),
        (
            "gist.github.com/stning/89b6ce57e45a68e2da77a960770e5773",
            ["gist.github.com/stning/89b6ce57e45a68e2da77a960770e5773"],
        ),
        (
            "cloud.google.com/resource-manager/docs/resource-settings/overview",
            [
                "cloud.google.com/resource-manager/docs/resource-settings/overview",
                "resource-manager",
            ],
        ),
        ("giflib.sourceforge.net", ["giflib.sourceforge.net", "giflib"]),
        (
            "retrofox.github.com/calendar-tools",
            ["retrofox.github.com/calendar-tools", "calendar-tools"],
        ),
        ("github.com/user/repo", ["github.com/user/repo", "repo"]),
        ("gitlab.com/user/repo", ["gitlab.com/user/repo", "repo"]),
        ("bitbucket.org/user/repo", ["bitbucket.org/user/repo", "repo"]),
        ("https://", []),
    ],
)
def test_possible_names(input_name: str, probable_names: list[str]) -> None:
    assert possible_names(input_name) == probable_names
