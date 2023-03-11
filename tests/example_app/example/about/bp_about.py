from flask import Blueprint, render_template

from example.about.our_story.bp_story import bp_aboutStory
from example.about.our_team.bp_team import bp_aboutTeam

bp_about = Blueprint("about",
                     __name__,
                     template_folder="./templates",
                     url_prefix="/about",
                     static_folder="static")

bp_about.register_blueprint(bp_aboutStory)
bp_about.register_blueprint(bp_aboutTeam)


@bp_about.route("/")
def about():
    return render_template("about.html")
