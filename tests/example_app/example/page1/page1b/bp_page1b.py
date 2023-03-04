from flask import Blueprint, render_template

bp_page1b = Blueprint('page_1b', __name__,
                      template_folder='./templates')


@bp_page1b.route('/b')
def page1b():
    return render_template('page_1b.html')
