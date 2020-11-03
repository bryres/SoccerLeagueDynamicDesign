from flask import render_template, request

from app.public import public_mod


@public_mod.route('/')
def index():
    return render_template("public/index.html")

