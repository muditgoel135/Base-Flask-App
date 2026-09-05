# Base Flask App

A minimal starter Flask application with user authentication (signup, login, logout) and account deletion, ready to use as a foundation for new projects.

## Features

- User registration and login with session management (Flask-Login)
- CSRF protection (Flask-WTF)
- SQLite database via SQLAlchemy
- Bootstrap 5 front-end
- Flash messages for user feedback

## Prerequisites

- Python 3.10+
- pip

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/muditgoel135/Base-Flask-App.git
   cd Base-Flask-App
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root. At minimum:

   ```env
   SECRET_KEY=your-secret-key-here
   ```

   Optional settings used by `app.py`:

   ```env
   DEBUG=True
   HOST=127.0.0.1
   PORT=5000
   ```

   If `SECRET_KEY` is not set, a random key is generated at runtime.

## Usage

Run the app:

```bash
flask run
```

Then open <http://127.0.0.1:5000> in your browser.
If the host or port has been changed in `.env`, then open <http://{HOST}:{PORT}>.

The SQLite database (`instance/base_app.db`) is created automatically on first run. Tables are created when the app starts.

## Project Structure

```text
Base-Flask-App/
├── app.py                 # Application entry point and routes
├── static/                # CSS and Bootstrap assets
├── templates/             # HTML templates
│   ├── index.html         # Homepage (login required)
│   ├── login.html         # Login page
│   └── signup.html        # Signup page
├── .env                   # Environment variables (not committed)
└── requirements.txt       # Python dependencies
```

## Routes

| Method   | Path             | Description                       |
| -------- | ---------------- | --------------------------------- |
| GET      | `/`              | Homepage (requires login)         |
| GET/POST | `/login`         | Log in a user                     |
| GET/POST | `/signup`        | Create a new account              |
| GET      | `/logout`        | Log out the current user          |
| POST     | `/delete_account`| Delete the current user's account |

## Environment Variables

| Variable    | Default          | Description                           |
| ----------- | ---------------- | ------------------------------------- |
| `SECRET_KEY`| random (runtime) | Flask secret key for signing data     |
| `DEBUG`     | `False`          | Enables debug mode and auto-reload    |
| `HOST`      | `127.0.0.1`      | Host to bind the server to            |
| `PORT`      | `5000`           | Port to bind the server to            |

## AI Disclosure

Minimal AI assistance was used in the creation of the main application (mainly autofills and inline suggestions). AI was significantly used for finding errors, but all bug fixes are human-made. Most commit messages are AI-generated. This README is AI-generated.

## Note

This is a base template. Passwords are hashed with Werkzeug (via `generate_password_hash`) and no `CREATE TABLE` migrations are used, so it is intended as a starting point for development rather than for production deployment.
