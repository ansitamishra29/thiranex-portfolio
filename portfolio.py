

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

load_dotenv()

app = Flask(__name__)



def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "thiranex_portfolio")
    )



@app.route("/")
def home():
    projects = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT title, description, technologies, project_link FROM projects"
        )
        projects = cursor.fetchall()

        cursor.close()
        connection.close()

    except Exception as error:
        print("PROJECTS ERROR:", error)

    return render_template(
    "portfolio.html",
    projects=projects,
    sent=request.args.get("sent") == "1"
)

@app.route("/test-db")
def test_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        connection.close()
        return f"Database connected successfully! Tables: {tables}"
    except Exception as error:
        return f"Database connection failed: {error}"


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return "Please fill in all fields.", 400

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        connection.commit()

        return redirect(url_for("home", sent="1"))

    except Exception as error:
        print("CONTACT FORM ERROR:", error)
        return "Sorry, your message could not be saved. Check the VS Code terminal.", 500

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
