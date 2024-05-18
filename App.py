import functions.Config as Config
from flask import Flask, render_template, request, redirect, url_for
import sys
import os
import requests
from werkzeug.utils import secure_filename
sys.path.append('functions')
import csv


app = Flask(__name__)

@app.route("/")
def home():

    return render_template(
        "team.html"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)