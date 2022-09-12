# Flask
from flask import Flask, render_template, url_for, redirect, flash

from weather import Netatmo, Met_data

app = Flask(__name__)

import datetime


class tiden:
    def __init__(self, a=""):
        self.a = a

    def update_data(self):
        self.a = f"{datetime.datetime.now()}"

    def __call__(self):
        self.update_data()
        return self.a


netatmo_data = Netatmo()
bodo_data = Met_data(0, 67.28, 14.40)
t = tiden()

print(t())

# Routes -----------------------------------------------------------------------------------
@app.route("/")
def home():
    bodo_data()
    bodo = bodo_data.met_data
    return render_template("home.html", net_data=netatmo_data, bodo=bodo, t=t)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="192.168.68.101", port=5000, debug=True, threaded=False)
