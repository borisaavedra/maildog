from flask import redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user, login_required
from ..models import Users
from ..auth import auth

@auth.route('/login', methods=["GET", "POST"])
def login():
   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]
      user = Users.query.filter_by(username=username).first()
      remember = request.form.get("rememberme")
      if user is not None and user.verify_password(password):
         login_user(user, remember)
         return redirect(request.args.get("next") or url_for("main.index"))
      flash("Wrong username or password", "danger")
   return render_template("auth/login.html")

@auth.route("/logout")
@login_required
def logout():
   logout_user()
   flash("You have been logged out", "success")
   return redirect(url_for("main.index"))
