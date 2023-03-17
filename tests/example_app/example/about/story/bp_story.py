from flask import Blueprint, render_template

bp_story = Blueprint(
    "story",
    __name__,
    template_folder="./templates",
    static_folder="static_folder",
)


@bp_story.route("/story")
def index():
    return render_template("story.html")
