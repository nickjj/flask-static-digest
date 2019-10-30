import click

from flask import current_app
from flask.cli import with_appcontext

from flask_static_digest.digester import compile as _compile
from flask_static_digest.digester import clean as _clean


@click.group()
def digest():
    """md5 tag and gzip static files."""
    pass


@digest.command()
@with_appcontext
def compile():
    """Generate optimized static files and a cache manifest."""
    _compile(current_app.static_folder,
             current_app.static_folder,
             current_app.config.get("FLASK_STATIC_DIGEST_BLACKLIST_FILTER"),
             current_app.config.get("FLASK_STATIC_DIGEST_GZIP_FILES"))


@digest.command()
@with_appcontext
def clean():
    """Remove generated static files and cache manifest."""
    _clean(current_app.static_folder,
           current_app.config.get("FLASK_STATIC_DIGEST_BLACKLIST_FILTER"),
           current_app.config.get("FLASK_STATIC_DIGEST_GZIP_FILES"))
