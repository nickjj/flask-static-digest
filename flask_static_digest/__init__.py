import json
import os

from urllib.parse import urljoin

from flask import _request_ctx_stack, url_for as flask_url_for


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

        self.host_url = app.config.get("FLASK_STATIC_DIGEST_HOST_URL")

        self.manifests = {}

        def ingestScaffold(endpoint, scaffold):
            if not scaffold.has_static_folder:
                return

            manifest_path = os.path.join(scaffold.static_folder,
                                         "cache_manifest.json")
            has_manifest = os.path.exists(manifest_path)

            if has_manifest:
                manifest = self._load_manifest(scaffold, manifest_path)
                self.manifests[endpoint] = manifest

        ingestScaffold('static', app)
        for endpoint, scaffold in app.blueprints.items():
            ingestScaffold(endpoint + '.static', scaffold)

        app.add_template_global(self.static_url_for)

    def _prepend_host_url(self, flask_url):
        return urljoin(self.host_url, flask_url)

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
        new_filename = {}
        filename = values.get("filename")

        # note: this is taken from flask's url_for
        # ( resolves relative endpoints )
        req_ctx = _request_ctx_stack.top
        if req_ctx is not None:
            blueprint_name = req_ctx.request.blueprint

            # If the endpoint starts with "." and the request matches a
            # blueprint, the endpoint is relative to the blueprint.
            if endpoint[:1] == ".":
                if blueprint_name is not None:
                    endpoint = f"{blueprint_name}{endpoint}"
                else:
                    endpoint = endpoint[1:]
        # endnote

        if filename:
            # If the manifest lookup fails then use the original filename
            # so that Flask doesn't throw a 500, but instead a proper 404.
            # The above only happens if your template has an invalid filename.
            manifest = self.manifests.get(endpoint)
            if manifest:
                new_filename["filename"] = manifest.get(filename, filename)

        merged_values = {**values, **new_filename}

        flask_url = flask_url_for(endpoint, **merged_values)

        return self._prepend_host_url(flask_url)

    def _load_manifest(self, scaffold, manifest_path):
        with scaffold.open_resource(manifest_path, "r") as f:
            manifest_dict = json.load(f)

        return manifest_dict
