from flask import Flask, render_template, redirect, url_for, request, session
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    print('hello')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        if request.form['username'] == "atulbhatt98@gmail.com" and request.form['password'] == "admin":
            #session["username"] = request.form['username']
            return render_template('adminPanel.html')

    return render_template('login.html')


@app.route('/adminPanel')
def adminPanel():
    return render_template('adminPanel.html')


def scrap():
    print("hello")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['jobDescription']
        file.save(file.filename)
        result = "file saved"
        return render_template("adminPanel.html", result=result)


if __name__ == '__main__':
    app.run()
