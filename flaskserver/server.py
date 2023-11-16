from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_cors import CORS
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.secret_key = "hadi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)


db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column("Id", db.Integer, primary_key=True)
    firstname = db.Column("FirstName", db.String(50))
    lastname = db.Column("LastName", db.String(50))
    phonenumber = db.Column("PhoneNumber", db.Integer)
    adresse = db.Column("Adresse", db.String(100))
    email = db.Column("Email", db.String(100))

    def __init__(self, id, firstname, lastname, phonenumber, adresse, email):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.phonenumber = phonenumber
        self.adresse = adresse
        self.email = email


@app.route("/tours")
def select_tours():
    return render_template("tours.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phonenumber = request.form["phonenumber"]
        adresse = request.form["adresse"]
        email = request.form["email"]

        if users.query.filter_by(email=email).first():
            flash("Email is already registered. Please choose a different email.")
            return redirect(url_for("register"))

        user = users(firstname=firstname, lastname=lastname, phonenumber=phonenumber, adresse=adresse, email=email)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! You can now log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user
        user_found = users.query.filter_by(id=user).first()
        if user_found:
            session["email"] = user_found.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        flash("you have been logged inn!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            user_found = users.query.filter_by(id=user).first()
            user_found.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email, user=user)
    else:
        flash("you are not logged in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("you have been logged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)