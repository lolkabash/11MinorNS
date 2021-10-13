# Imports
from flask import Flask, render_template, request
from web_modules import Form, site
from datetime import date, datetime
import os

ON_HEROKU = os.environ.get("ON_HEROKU")

if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get("$PORT", 17995))  # as per OP comments default is 17995
else:
    port = 3000


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
app.run(host="0.0.0.0", port=port)
