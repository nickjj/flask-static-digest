from flask import Blueprint, render_template

bp_team = Blueprint("team", __name__,
                    template_folder="./templates",
                    static_url_path="/static/team",
                    static_folder="static")


@bp_team.route("/team")
def team():
    return render_template("team.html")