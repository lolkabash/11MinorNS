# Imports
from flask import Flask, render_template, request
from modules import Form, site
from datetime import date, datetime

app = Flask(__name__)

# Main Form
@app.route("/form")
def form():
    DATE = datetime.now().strftime("%d%m%y")
    TIME = datetime.now().strftime("%H%M")
    print(DATE)
    return render_template(
        "form.html",
        DATE=DATE,
        TIME=TIME,
    )


# Main Display
@app.route("/data", methods=["POST"])
def data():
    form_data = request.form.to_dict(flat=True)
    output = site(form_data)
    return render_template("data.html", output=output)


# Errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# Run App
app.run(host="0.0.0.0", port=5000, debug=True)
