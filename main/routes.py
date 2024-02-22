from flask import render_template, request, flash, redirect, url_for, session
from main import bp
import re
from models import db, Participant


def check_mail_domain(email, domain):
    pattern = r'@' + re.escape(domain) + r'\b'
    match = re.search(pattern, email)
    return bool(match)

@bp.route("/", methods=('GET', 'POST'))
def index():

    if request.method == 'POST':

        
        error = None
        mail = request.form.get('emailInput')

        if mail == '':
            error = 'Mail not found'
            flash('ERROR: ' + error)
            return render_template('index.html')

        session['mail'] = mail


        if check_mail_domain(mail, 'provadis.de'):
            return redirect(url_for('main.departments'))
    
        
        error = 'Mail not found'
        flash('ERROR: ' + 'Organization not found')

    return render_template('index.html')


@bp.route("/departments", methods=('GET', 'POST'))
def departments():
       
    if request.method == 'POST':
        error = None
        department = request.form.get('departmentSelect')
        name = request.form.get('nameInput')
        surname = request.form.get('surnameInput')
        date = request.form.get('dateSelect')

        if department == "":
            error = 'Bitte wähle eine Abteilung aus.'
            flash('ERROR: ' + error)
            return render_template('departmentSelektion.html')
        
        if name == "" or surname == "":
            error = 'Bitte gib deinen Namen ein.' + str(date)
            flash('ERROR: ' + error)
            return render_template('departmentSelektion.html')
        
        if date is None or date == "":
            error = 'Bitte wähle ein Datum aus.'
            flash('ERROR: ' + error)
            return render_template('departmentSelektion.html')

        
        session['department'] = department
        session['name'] = name
        session['surname'] = surname
        session['date'] = date
        return redirect(url_for('main.invitation'))

    return render_template('departmentSelektion.html')

@bp.route("/invitation")
def invitation():

    mail = session.get('mail')
    department = session.get('department')
    name = session.get('name')
    surname = session.get('surname')
    date = session.get('date')

    # save to db
    participant = Participant(mail = mail, department = department, name = name, surname = surname, date = date)
    db.session.add(participant)
    db.session.commit()

    context = {'mail': mail, 'department': department}

    return render_template('invitation.html', **context)
