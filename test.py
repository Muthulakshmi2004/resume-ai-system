from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    print("Templates folder contents:", os.listdir(os.path.join(app.root_path, "templates")))
    return render_template("index1.html")

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
