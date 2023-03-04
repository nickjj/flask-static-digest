from flask import Flask, render_template
from flask_static_digest import FlaskStaticDigest

from .page1.bp_page1 import bp_page1
from .page2.bp_page2 import bp_page2

flask_static_digest = FlaskStaticDigest()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.settings")

    app.register_blueprint(bp_page1)
    app.register_blueprint(bp_page2)

    flask_static_digest.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
