from flask import render_template, request, flash, redirect, url_for, session, g
import uuid
from main import bp
import re


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

        if department == "":
            error = 'Bitte wählen Sie eine Abteilung aus.'
            flash('ERROR: ' + error)
            return render_template('departmentSelektion.html')
        
        session['department'] = department
        return redirect(url_for('main.invitation'))

    return render_template('departmentSelektion.html')

@bp.route("/invitation")
def invitation():

    mail = session.get('mail')
    department = session.get('department')
    context = {'mail': mail, 'department': department}

    return render_template('invitation.html', **context)
