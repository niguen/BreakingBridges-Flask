from flask import render_template, flash, request, redirect, url_for, session
from admin import bp
from auth.routes import login_required
from models import db, Participant



@bp.route("/", methods=('GET', 'POST'))
@login_required
def index():
    
    if request.method == 'POST':

        
        groupSize = int(request.form.get('groupSizeSelect'))

        if groupSize < 5 and groupSize > 2:
            session['groupSize'] = groupSize
            return redirect(url_for("admin.groups"))
        
        flash("ERROR: Invalid group size")
    
    participants = Participant.query.all()
    participantCount = len(participants)
    # flash(participants)

    return render_template('admin/index.html', participantCount = participantCount)


@bp.route("/groups", methods=('GET', 'POST'))
@login_required
def groups():

    groupSize = session.get('groupSize')
    participants = Participant.query.all()
    participantCount = len(participants)

    # departments = Participant.query('department').distinct().all()
    # flash(departments)

    numGroups = participants // groupSize
    if participantCount % groupSize != 0:  # Check if there are remaining people
        numGroups += 1  # Add an extra group for the remaining people

    

    if request.method == "POST":
        pass
    
    return render_template('admin/groups.html', participants = participants)

