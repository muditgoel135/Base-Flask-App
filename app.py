from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    logout_user,
    login_user,
    current_user,
)
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or random.getrandbits(128).to_bytes(16, "big")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_app.db"
db = SQLAlchemy(app)
CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    """
    This is the User model class that represents a user in the database.
    It inherits from db.Model and UserMixin, which provides default implementations for user authentication methods.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """
    This function is used by Flask-Login to load a user from the database given their user_id.
    It queries the User model for a user with the specified user_id and returns the user object.
    If no user is found, it returns None.

    :param user_id: The ID of the user to load.
    :return: The User object if found, otherwise None.
    """

    return User.query.get(int(user_id))


@app.route("/")
@login_required
def homepage():
    """
    This is the homepage route. It checks if a user is logged in by verifying the session.
    If the user is not logged in, they are redirected to the login page.
    If they are logged in, it renders the index.html template and passes the username of the logged-in user to the template.
    """

    return render_template("index.html", username=current_user.username)


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

    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("homepage"))

        else:
            flash("Invalid username or password.", "error")
            return render_template("login.html")

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
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("signup.html")

        if not username in [
            user.username for user in User.query.with_entities(User.username).all()
        ]:
            user = User(username=username, password=generate_password_hash(password))
            with app.app_context():
                db.session.add(user)
                db.session.commit()

            flash("Account created successfully.", "success")
            return redirect(url_for("login"))

        else:
            flash("Username already exists.", "error")
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    """
    This is the logout route. It checks if a user is logged in by verifying the session.
    If the user is logged in, it removes the user_id from the session and redirects to the login page.
    If the user is not logged in, it simply redirects to the login page.
    """

    logout_user()
    return redirect(url_for("login"))


@app.route("/delete_account", methods=["POST"])
def delete_account():
    """
    This is the delete account route. It checks if a user is logged in by verifying the session.
    If the user is logged in, it deletes the user from the database and removes the user_id from the session, then redirects to the login page.
    If the user is not logged in, it simply redirects to the login page.
    """

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    user = current_user
    logout_user()

    if user:
        with app.app_context():
            db.session.delete(user)
            db.session.commit()

    flash("Your account has been deleted.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        debug=(os.getenv("DEBUG") == "True"),
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT") or "5000"),
        use_reloader=(os.getenv("DEBUG") == "True"),
    )
