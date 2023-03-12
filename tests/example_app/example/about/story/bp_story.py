from flask import Blueprint, render_template

bp_story = Blueprint("story", __name__,
                     static_folder='static_folder',
                     template_folder="./templates")


@bp_story.route("/story")
def index():
    return render_template("index.html")
