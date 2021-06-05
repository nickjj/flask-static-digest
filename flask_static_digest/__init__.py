import json
import os

from urllib.parse import urljoin, urlparse
from flask import url_for as flask_url_for


class FlaskStaticDigest(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Mutate the application passed in as explained here:
          https://flask.palletsprojects.com/en/1.1.x/extensiondev/

        :param app: Flask application
        :return: None
        """
        app.config.setdefault("FLASK_STATIC_DIGEST_BLACKLIST_FILTER", [])
        app.config.setdefault("FLASK_STATIC_DIGEST_GZIP_FILES", True)
        app.config.setdefault("FLASK_STATIC_DIGEST_HOST_URL", None)

        self.host_url, self.prefix = parse_digest_host_url(
            app.config.get("FLASK_STATIC_DIGEST_HOST_URL"))
        self.static_url_path = app.static_url_path

        self.manifest_path = os.path.join(app.static_folder,
                                          "cache_manifest.json")
        self.has_manifest = os.path.exists(self.manifest_path)

        self.manifest = {}

        if self.has_manifest:
            self.manifest = self._load_manifest(app)

        app.add_template_global(self.static_url_for)

    def _load_manifest(self, app):
        with app.open_resource(self.manifest_path, "r") as f:
            manifest_dict = json.load(f)

        return manifest_dict

    def _prepend_host_url(self, host, filename):
        parts = list( # removing empty strings
            filter(None, [self.prefix, self.static_url_path, filename]))

        return urljoin(self.host_url, "/".join(parts))

    def static_url_for(self, endpoint, **values):
        """
        This function uses Flask's url_for under the hood and accepts the
        same arguments. The only differences are it will prefix a host URL if
        one exists and if a manifest is available it will look up the filename
        from the manifest.

        :param endpoint: The endpoint of the URL
        :type endpoint: str
        :param values: Arguments of the URL rule
        :return: Static file path.
        """
        if not self.has_manifest:
            if self.host_url:
                return self._prepend_host_url(self.host_url,
                                              values.get("filename"))
            else:
                return flask_url_for(endpoint, **values)

        new_filename = {}
        filename = values.get("filename")

        if filename:
            # If the manifest lookup fails then use the original filename
            # so that Flask doesn't throw a 500, but instead a proper 404.
            # The above only happens if your template has an invalid filename.
            new_filename["filename"] = self.manifest.get(filename, filename)

        merged_values = {**values, **new_filename}

        if self.host_url:
            return self._prepend_host_url(self.host_url,
                                          merged_values.get("filename"))
        else:
            return flask_url_for(endpoint, **merged_values)


def parse_digest_host_url(host_url_prefix):
    """
    Detect if host_url_prefix contains a path element and returns a tuple with
    the elements (host_part, path_part), for example for

    host_url_prefix = "https://cdn.example.com/myapp/some/path/"

    This function should return:
    ('https://cdn.example.com', "/myapp/some/path/")

    :param host_url_prefix: CDN like URL prefix
    :type host_url_prefix: str
    :return: tuple with the elements (host_part, path_part).
    """
    scheme, netloc, path, _, _, _ = urlparse(host_url_prefix)

    if path and path.startswith("/"):
        path = path[1:]

    if path and path.endswith("/"):
        path = path[:-1]

    return (f"{scheme}://{netloc}", path)
