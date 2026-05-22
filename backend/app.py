from flask import Flask, request, render_template, session, redirect, url_for, flash
import os, re
from resume_parser import parse_resume
from model import fit_transform, get_scores
from database import init_db, insert, get_all_results, delete_score, clear_all, init_user_db, add_user, get_user
from auth import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

app = Flask(__name__, template_folder="templates")
app.secret_key = "secret"

UPLOAD_FOLDER = "data/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()
init_user_db()

def validate_password(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[!@#$%^&*]", password))

def extract_skills(text):
    """Simple keyword extraction from job description"""
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return [w for w in words if w not in ENGLISH_STOP_WORDS]

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("u")
        password = request.form.get("p")

        if not validate_password(password):
            flash("Password must meet requirements.", "error")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        try:
            add_user(username, hashed_pw)
            session["user"] = username
            flash(f"Welcome {username}! Account created.", "success")
            return redirect(url_for("home"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("u")
        password = request.form.get("p")

        user = get_user(username)
        if user and check_password_hash(user["password_hash"], password):
            session["user"] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user" in session:
        session.clear()
        flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/analytics")
@login_required
def analytics():
    user = get_user(session["user"])
    scores = get_all_results(user["id"])
    total = len(scores)
    avg = sum([s["score"] for s in scores]) / total if total > 0 else 0
    return render_template("analytics.html", scores=scores, total=total, avg=avg)

@app.route("/rank", methods=["POST"])
@login_required
def rank_resumes():
    job_description = request.form["job_description"]
    session["job_description"] = job_description

    resumes, filenames = [], []
    for file in request.files.getlist("resumes"):
        parsed = parse_resume(file)
        resumes.append(parsed["cleaned_text"])
        filenames.append(file.filename)

    matrix = fit_transform(job_description, resumes)
    scores = get_scores(matrix)

    user = get_user(session["user"])
    if not user:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for("login"))

    for fn, sc in zip(filenames, scores):
        insert(user["id"], fn, sc)

    all_results = get_all_results(user["id"])
    return render_template("results.html", results=all_results)


@app.route("/delete/<filename>", methods=["POST"])
@login_required
def delete_rank(filename):
    user = get_user(session["user"])
    delete_score(user["id"], filename)
    flash(f"Deleted {filename}", "info")
    return redirect(url_for("analytics"))

@app.route("/clear", methods=["POST"])
@login_required
def clear_all_ranks():
    user = get_user(session["user"])
    clear_all(user["id"])
    flash("All records cleared.", "info")
    return redirect(url_for("analytics"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
