from flask import render_template, flash
from admin import bp
from auth.routes import login_required
from models import db, Participant



@bp.route("/")
@login_required
def index():

    participants = Participant.query.all()
    flash(participants)
    return render_template('admin/index.html')
