from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "taskmanagersecretkey"


# --------------------------
# DATABASE
# --------------------------

def get_db():
    conn = sqlite3.connect("taskmanager.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


init_db()

# --------------------------
# AUTH ROUTES
# --------------------------

@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )

            conn.commit()

            return redirect("/login")

        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Username already exists"
            )

        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# --------------------------
# DASHBOARD
# --------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# --------------------------
# TASK API
# --------------------------

@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    if "user_id" not in session:
        return jsonify([])

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM tasks
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    tasks = [dict(row) for row in cur.fetchall()]

    conn.close()

    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    title = data.get("title")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks(title,status,user_id)
        VALUES(?,?,?)
        """,
        (
            title,
            "Pending",
            session["user_id"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Task Added"})


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    status = data.get("status")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET status=?
        WHERE id=? AND user_id=?
        """,
        (
            status,
            task_id,
            session["user_id"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Task Updated"})


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM tasks
        WHERE id=? AND user_id=?
        """,
        (
            task_id,
            session["user_id"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Task Deleted"})


if __name__ == "__main__":
    app.run(debug=True)