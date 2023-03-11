from flask import Flask, render_template
from flask_static_digest import FlaskStaticDigest

from example.about.bp_about import bp_about
from example.contact.bp_contact import bp_contact

flask_static_digest = FlaskStaticDigest()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.settings")

    app.register_blueprint(bp_about)
    app.register_blueprint(bp_contact)

    flask_static_digest.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
