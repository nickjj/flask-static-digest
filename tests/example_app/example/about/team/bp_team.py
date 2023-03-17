from flask import Blueprint, render_template

bp_team = Blueprint(
    "team",
    __name__,
    template_folder="./templates",
    static_folder="static",
    static_url_path="/static/team",
)


@bp_team.route("/team")
def index():
    return render_template("team.html")
