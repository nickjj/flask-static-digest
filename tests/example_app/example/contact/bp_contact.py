from flask import Blueprint, render_template

bp_contact = Blueprint("contact",
                       __name__,
                       template_folder="./templates",
                       static_url_path="/contact/static",
                       static_folder="static")


@bp_contact.route("/contact")
def contact():
    return render_template("contact.html")
