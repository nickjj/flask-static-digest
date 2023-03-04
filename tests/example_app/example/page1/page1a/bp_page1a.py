from flask import Blueprint, render_template

bp_page1a = Blueprint('page_1a', __name__,
                      template_folder='./templates',
                      static_url_path='/static/a',
                      static_folder='static')


@bp_page1a.route('/a')
def page1a():
    return render_template('page_1a.html')
