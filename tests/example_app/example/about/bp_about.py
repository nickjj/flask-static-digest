from flask import Blueprint, render_template

from example.about.story.bp_story import bp_story
from example.about.team.bp_team import bp_team

bp_about = Blueprint(
    "about",
    __name__,
    url_prefix="/about",
    template_folder="./templates",
    static_folder="static",
)

bp_about.register_blueprint(bp_story)
bp_about.register_blueprint(bp_team)


@bp_about.route("/")
def index():
    return render_template("about.html")
