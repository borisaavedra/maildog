from flask import redirect, url_for, render_template, request, flash
from ..models import db, Codes, Users, Templates, Emails
from . import main
from flask_mail import Message
from app import mail
from flask_login import login_required, current_user
import os

ALLOWED_EXTENSIONS = {"csv"}


@main.route('/')
@login_required
def index():
   templates = Templates.query.filter_by(user_id=current_user.id).all()
   context = {
      "templates": templates,
      "mail_server_from_user": os.getenv("MAIL_SERVER"),
      "mail_port_from_user": os.getenv("MAIL_PORT"),
      "mail_username": os.getenv("MAIL_USERNAME"),
      "mail_password": os.getenv("MAIL_PASSWORD")
   }
   return render_template("index.html", **context)


@main.route("/signin", methods=["POST", "GET"])
def signin():

   if request.method == "POST":
      web_code = request.form["code"]
      db_code = Codes.query.filter_by(code=web_code).first()
      if db_code is not None:
         name = request.form["name"]
         email = request.form["email"]
         password = request.form["password"]
         new_user = Users(
            name=name,
            username=email,
            password=password
         )
         try:
            db.session.add(new_user)
            db.session.commit()
            flash("User added!", "success")
         except:
            db.session.rollback()
            flash("Something went wrong", "danger")
      else:
         flash("You need a valid invitation code, you punk!", "danger")

   return render_template("signin.html")


@main.route("/settings", methods=["POST", "GET"])
def settings():
   if request.method == "POST":
      try:
         os.environ["MAIL_SERVER"] = request.form["server"]
         os.environ["MAIL_PORT"] = request.form["port"]
         os.environ["MAIL_USERNAME"] = request.form["mail_username"]
         os.environ["MAIL_PASSWORD"] = request.form["mail_password"]
         flash("Change was saved successfully 👍", "success")
      except:
         flash("Something went wrong 😢 Please try again", "danger")
   return redirect(url_for("main.index"))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def send_mail(subject, sender, recipients, message):
   with mail.connect() as conn:
      for user in recipients:
         msg = Message(recipients=[user],
                           html=message,
                           sender=sender,
                           subject=subject)
         conn.send(msg)
   return True


@main.route("/create_campaign", methods=["POST", "GET"])
def create_campaign():
   if request.method == "POST":
      file = request.files["file"]
      if allowed_file(file.filename):
         mail = file.read().decode("ascii")
         mails = mail.split(",")
         if send_mail(request.form["subject"], request.form["sender"], mails, request.form["template"]):
            t = Templates(template=request.form["template"], user_id=current_user.id)
            for m in mails:
               new_mail = Emails(email=m, user_id=current_user.id)
               db.session.add(new_mail)
               db.session.commit()
            db.session.add(t)
            try:
               db.session.commit()
            except:
               flash("Something went wrong saving the template", "danger")
            flash("Message was sent", "success")
         else:
            flash("Sorry", "danger")
      else:
         flask("Wrong file type! 🐕", "danger")
   return render_template("create_campaign.html")

@main.route("/audience")
def audience():
   mails = Emails.query.filter_by(user_id=current_user.id).all()
   return render_template("audience.html", mails=mails)