import json
import logging
import os
from urllib.parse import urljoin

from flask import request
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
        app.config.setdefault("FLASK_STATIC_DIGEST_HOST_URL", None)
        app.config.setdefault("FLASK_STATIC_DIGEST_COMPRESSION", ["gzip"])

        compression = set(app.config["FLASK_STATIC_DIGEST_COMPRESSION"])
        app.config["FLASK_STATIC_DIGEST_COMPRESSION"] = list(compression)

        self.host_url = app.config.get("FLASK_STATIC_DIGEST_HOST_URL")

        self.manifests = {}

        self._load_manifest("static", app)
        for endpoint, blueprint in app.blueprints.items():
            self._load_manifest(f"{endpoint}.static", blueprint)

        app.add_template_global(self.static_url_for)

    def _load_manifest(self, endpoint, scaffold):
        if not scaffold.has_static_folder:
            return

        manifest_path = os.path.join(
            scaffold._static_folder, "cache_manifest.json"
        )
        try:
            with scaffold.open_resource(manifest_path, "r") as f:
                self.manifests[endpoint] = json.load(f)
        except json.JSONDecodeError:
            logging.warning(f"Couldn't decode file: {manifest_path}")
        except PermissionError:
            logging.warning(f"Couldn't access file: {manifest_path}")
        except (FileNotFoundError, Exception):
            pass

    def _prepend_host_url(self, host, filename):
        return urljoin(
            self.host_url, "/".join([self.static_url_path, filename])
        )

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
        if request is not None:
            blueprint_name = request.blueprint
            if endpoint[:1] == ".":
                if blueprint_name is not None:
                    endpoint = f"{blueprint_name}{endpoint}"
                else:
                    endpoint = endpoint[1:]

        manifest = self.manifests.get(endpoint, {})
        filename = values.get("filename", None)
        values["filename"] = manifest.get(filename, filename)

        return urljoin(self.host_url, flask_url_for(endpoint, **values))
