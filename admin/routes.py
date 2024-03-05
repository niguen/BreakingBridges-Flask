from flask import render_template, flash, request, redirect, url_for, session
from admin import bp
from auth.routes import login_required
from models import db, Participant
from openai import OpenAI
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import os

def sendMail(participants):

    port = os.environ.get("MAIL_PORT")
    mail = os.environ.get("MAIL_ADDRESS")
    password = os.environ.get("MAIL_PASSWORD")
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail, password)
        # TODO: Send email here

        for participant in participants:

            message = MIMEMultipart()
            message["Subject"] = "Deine Einladung zum Secret Lunch"
            message["From"] = mail
            message["To"] = participant.mail

            # Add your message body

                 # Read the HTML from a file in the static directory
            with open('static/email_template.html', 'r', encoding='utf-8') as f:
                body = f.read().format(name=participant.name, group=participant.group, question=participant.question)

            message.attach(MIMEText(body, "html", _charset='utf-8'))
            server.sendmail(mail, participant.mail, message.as_string())


@bp.route("/", methods=('GET', 'POST'))
@login_required
def index():
    
    if request.method == 'POST':

        groupSize = int(request.form.get('groupSizeSelect'))

        if groupSize < 5 and groupSize > 1:
            session['groupSize'] = groupSize
            return redirect(url_for("admin.groups"))    
    
    participantCount = len(Participant.query.all())
    
    return render_template('admin/index.html', participantCount = participantCount)


@bp.route("/groups", methods=('GET', 'POST'))
@login_required
def groups():

    if request.method == "POST":
         return redirect(url_for("admin.sendInvites"))


    # Ask chatGPT to create groups and save result to database
    participants = Participant.query.all()
    participants_json = [u.__dict__ for u in participants]

    from openai import OpenAI
    import json

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Es wird eine Liste von Teilnehmern im JSON Format geliefert. Die Teilnehmer in der Liste sollen in Gruppen aufgeteilt werden."}, 
            {"role": "system", "content": "Gebe nur die valide Json liste zurück. Bitte keine Veränderungen der Struktur, nur die einzelnen Felder sollen ausgefüllt werden."},

            {"role": "system", "content": "Die Gruppen haben immer zwei oder drei Teilnehmer und es dürfen keine zwei Teilnehmer aus einer Abteilung in einer Gruppe sein. Trage die Gruppennummer im JSON für jeden Teilnehmer im json in das Feld 'group' ein." },
            {"role": "system", "content": "Zusätzlich zur Gruppe erhält jeder Teilnehmer eine personalisierte Frage,  welche sich auf das Hobby im Feld 'aboutMe'  bezieht. Die Frage soll im Feld 'question' gespeichert werden."},
            {"role": "user", "content": str({'participants' : participants_json})}
        ],
        response_format = { "type": "json_object" },
        model="gpt-4-turbo-preview",
    )

    # convert string to json
    groups = json.loads(chat_completion.choices[0].message.content.strip())
    groups

    for item in groups['participants']:
        current = Participant.query.filter(Participant.id == item['id']).first()
        if current:
            current.group = item['group']
            current.question = item['question']
            db.session.commit()
    
    participants = Participant.query.all()

    return render_template('admin/groups.html', participants = participants)


@bp.route("/sendInvites")
@login_required
def sendInvites():

    participants = Participant.query.all()

    sendMail(participants)

    return render_template('admin/sendInvitations.html')

