from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or random.getrandbits(128).to_bytes(16, "big")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_app.db"
db = SQLAlchemy(app)


class User(db.Model):
    """
    The SQLAlchemy Database model for the User table.
    This table stores user information including a unique username and password.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def homepage():
    """
    This is the homepage route. It checks if a user is logged in by verifying the session.
    If the user is not logged in, they are redirected to the login page.
    If they are logged in, it renders the index.html template and passes the username of the logged-in user to the template.
    """

    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template(
        "index.html", username=User.query.get(session["user_id"]).username
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    This is the login route. It handles both GET and POST requests.
    GET requests mean that the client is asking for the login page, so it renders the login.html template.
    POST requests mean that the client is submitting login credentials.
    The function checks if the provided username and password match any user in the database.
    If they do, it sets the user_id in the session and redirects to the homepage.
    If not, it renders the login.html template again with an error message indicating invalid credentials.
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    This is the signup route. It handles both GET and POST requests.
    GET requests mean that the client is asking for the signup page, so it renders the signup.html template.
    POST requests mean that the client is submitting signup credentials.
    The function checks if the provided username is unique and the password meets the requirements.
    If they do, it creates a new user and redirects to the login page. If not, it renders the signup.html template again with an error message.
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username in [
            user.username for user in User.query.with_entities(User.username).all()
        ] and not password in [
            user.password for user in User.query.with_entities(User.password).all()
        ]:
            user = User(username=username, password=password)
            with app.app_context():
                db.session.add(user)
                db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("signup.html", error="Username already exists")
    return render_template("signup.html")


@app.route("/logout")
def logout():
    """
    This is the logout route. It checks if a user is logged in by verifying the session.
    If the user is logged in, it removes the user_id from the session and redirects to the login page.
    If the user is not logged in, it simply redirects to the login page.
    """

    if session.get("user_id"):
        session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/delete_account", methods=["POST"])
def delete_account():
    """
    This is the delete account route. It checks if a user is logged in by verifying the session.
    If the user is logged in, it deletes the user from the database and removes the user_id from the session, then redirects to the login page.
    If the user is not logged in, it simply redirects to the login page.
    """

    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if user:
        with app.app_context():
            db.session.delete(user)
            db.session.commit()
    session.pop("user_id", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG") == "True",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")) if os.getenv("PORT") else 5000,
        use_reloader=os.getenv("DEBUG") == "True",
    )
