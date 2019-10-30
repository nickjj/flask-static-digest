from flask import Flask, render_template
from flask_static_digest import FlaskStaticDigest

flask_static_digest = FlaskStaticDigest()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.settings")

    flask_static_digest.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
