from flask import Blueprint, render_template

bp_page2 = Blueprint("page_2",
                     __name__,
                     template_folder="./templates",
                     static_url_path="/page-2/static",
                     static_folder="static")


@bp_page2.route("/page-2")
def page2():
    return render_template("page_2.html")
