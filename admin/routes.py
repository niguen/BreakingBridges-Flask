from flask import render_template
from admin import bp
from auth.routes import login_required



@bp.route("/")
@login_required
def index():
    return render_template('admin/index.html')
