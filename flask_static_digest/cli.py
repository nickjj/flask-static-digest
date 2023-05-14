import sys

import click
from flask import current_app
from flask.cli import with_appcontext

from flask_static_digest.digester import clean as _clean
from flask_static_digest.digester import compile as _compile


@click.group()
@click.pass_context
@with_appcontext
def digest(ctx):
    """md5 tag and compress static files."""

    ctx.ensure_object(dict)

    ctx.obj["gzip"] = False
    ctx.obj["brotli"] = False
    ctx.obj["blacklist_filter"] = current_app.config.get(
        "FLASK_STATIC_DIGEST_BLACKLIST_FILTER"
    )

    compression = current_app.config.get("FLASK_STATIC_DIGEST_COMPRESSION")

    for algo in compression:
        if algo == "gzip":
            ctx.obj["gzip"] = True
        elif algo == "brotli":
            try:
                import brotli  # noqa: F401
            except ModuleNotFoundError:
                click.echo("Error: Python package 'brotli' not installed.")
                sys.exit(78)  # sysexits.h 78 EX_CONFIG configuration error
            else:
                ctx.obj["brotli"] = True
        else:
            click.echo(
                f"{algo} is not a supported compression value, it must be"
                " 'gzip' or 'brotli'"
            )
            sys.exit(78)


@digest.command()
@click.pass_context
@with_appcontext
def compile(ctx):
    """Generate optimized static files and a cache manifest."""
    for blueprint in [current_app, *current_app.blueprints.values()]:
        if not blueprint.static_folder:
            continue

        _compile(
            blueprint.static_folder,
            blueprint.static_folder,
            ctx.obj["blacklist_filter"],
            ctx.obj["gzip"],
            ctx.obj["brotli"],
        )


@digest.command()
@click.pass_context
@with_appcontext
def clean(ctx):
    """Remove generated static files and cache manifest."""
    for blueprint in [current_app, *current_app.blueprints.values()]:
        if not blueprint.static_folder:
            continue

        _clean(
            blueprint.static_folder,
            ctx.obj["blacklist_filter"],
            ctx.obj["gzip"],
            ctx.obj["brotli"],
        )
