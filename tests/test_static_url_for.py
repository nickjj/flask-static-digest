from flask import Flask
from flask_static_digest import FlaskStaticDigest
import pytest as pt
import json


fake_manifest = {
    "hey.png": "hey-HASH.png",
    "images/hey.png": "images/hey-HASH.png",
    "images/card/hey.png": "images/card/hey-HASH.png"
}


def make_app(tmp_path, host_url, static_url_path):
    appdir = tmp_path / 'fakeappdir'
    appdir.mkdir()

    staticdir = appdir / 'static'
    staticdir.mkdir()

    manifest_f = staticdir / 'cache_manifest.json'
    manifest_f.write_text(json.dumps(fake_manifest))

    app = Flask(
        __name__, root_path=appdir, static_folder=staticdir,
        static_url_path=static_url_path)
    app.config['TESTING'] = True
    app.config['FLASK_STATIC_DIGEST_HOST_URL'] = host_url

    with app.app_context():
        return app


@pt.mark.parametrize(
    "host_url, static_url_path, file, expected", [
        (
            "https://cdn.example.com", None, "hey.png",
            "https://cdn.example.com/static/hey-HASH.png"
        ),
        (
            "https://cdn.example.com", None, "images/hey.png",
            "https://cdn.example.com/static/images/hey-HASH.png"
        ),
        (
            "https://cdn.example.com", "/static/something/", "hey.png",
            "https://cdn.example.com/static/something/hey-HASH.png"
        ),
        (
            pt.param(
                "https://cdn.example.com", "static/something/", "hey.png",
                "https://cdn.example.com/static/something/hey-HASH.png",
                marks=pt.mark.xfail(raises=ValueError)
            )
        ),
        (
            "https://cdn.example.com/myapp", None, "images/hey.png",
            "https://cdn.example.com/myapp/static/images/hey-HASH.png"
        ),
        (
            "https://cdn.example.com/myapp", '/static', "images/hey.png",
            "https://cdn.example.com/myapp/static/images/hey-HASH.png"
        ),
        (
            "https://cdn.example.com/myapp", "/static/something/", "hey.png",
            "https://cdn.example.com/myapp/static/something/hey-HASH.png"
        ),
        (
            "https://cdn.example.com/myapp/anotherdir", None, "images/hey.png",
            "https://cdn.example.com/myapp/anotherdir"
            "/static/images/hey-HASH.png"
        ),
        (None, None, "hey.png", "/static/hey-HASH.png"),
        (None, '/mystatic/url', "hey.png", "/mystatic/url/hey-HASH.png"),
    ]
)
def test_get_url(tmp_path, host_url, static_url_path, file, expected):
    app = make_app(tmp_path, host_url, static_url_path)
    ext = FlaskStaticDigest(app=app)

    ret = ext.static_url_for('static', filename=file)

    assert ret == expected
