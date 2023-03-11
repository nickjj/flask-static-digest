from flask import Blueprint, render_template

bp_aboutStory = Blueprint("our_story", __name__,
                          template_folder="./templates")


@bp_aboutStory.route("/our-story")
def pageAboutStory():
    return render_template("our_story.html")
