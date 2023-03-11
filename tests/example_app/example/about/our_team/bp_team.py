from flask import Blueprint, render_template

bp_aboutTeam = Blueprint("our_team", __name__,
                         template_folder="./templates",
                         static_url_path="/static/team",
                         static_folder="static")


@bp_aboutTeam.route("/our-team")
def pageAboutTeam():
    return render_template("our_team.html")
