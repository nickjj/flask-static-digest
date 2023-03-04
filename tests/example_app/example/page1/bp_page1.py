from flask import Blueprint, render_template
from .page1a.bp_page1a import bp_page1a
from .page1b.bp_page1b import bp_page1b

bp_page1 = Blueprint('page_1',
                     __name__,
                     template_folder='./templates',
                     url_prefix='/page-1',
                     static_folder='static')

bp_page1.register_blueprint(bp_page1a)
bp_page1.register_blueprint(bp_page1b)


@bp_page1.route('/')
def page1():
    return render_template('page_1.html')
