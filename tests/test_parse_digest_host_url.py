from flask_static_digest import parse_digest_host_url

import pytest as pt


@pt.mark.parametrize(
    "digest_host_url, expected", [
        (
            "https://cdn.example.com",
            ("https://cdn.example.com", "")
        ),
        (
            "https://cdn.example.com/",
            ("https://cdn.example.com", "")
        ),
        (
            "https://cdn.example.com/myapp",
            ("https://cdn.example.com", "myapp")
        ),
        (
            "https://cdn.example.com/myapp/",
            ("https://cdn.example.com", "myapp")
        ),
        (
            "https://cdn.example.com/myapp/anotherdir",
            ("https://cdn.example.com", "myapp/anotherdir")
        ),
        (
            "https://cdn.example.com/myapp/anotherdir/",
            ("https://cdn.example.com", "myapp/anotherdir")
        ),
    ]
)
def test_parse_function(digest_host_url, expected):
    assert parse_digest_host_url(digest_host_url) == expected


def test_joined_urls():
    pass
