from flask import Flask, render_template, request
from datetime import date, datetime

app = Flask(__name__)


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


@app.route("/data/", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/form' to submit form"
        )
    if request.method == "POST":
        form_data = request.form
        return render_template("data.html", form_data=form_data)


app.run(host="localhost", port=5000)
