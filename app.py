import PyPDF2
from flask import Flask, render_template, request
from pathlib import Path
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        if request.form['username'] == "atulbhatt98@gmail.com" and request.form['password'] == "admin":
            return render_template('adminPanel.html')

    return render_template('login.html')


@app.route('/adminPanel')
def adminPanel():
    return render_template('adminPanel.html')


def scrap(pathtoFile):
    pdfFileObj = open(pathtoFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    totalPages = pdfReader.numPages
    pdfData = ""
    for i in range(totalPages):
        pageObj = pdfReader.getPage(i)
        pdfData = pdfData + pageObj.extractText()
    return pdfData


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['jobDescription']
        file.save(file.filename)
        root = os.path.abspath(os.path.dirname(__file__))
        location = os.path.join(root, "jobDescription.pdf")
        my_file = Path(location)
        while not my_file.is_file():
            print("not found")
            continue

        file_data = scrap(location)
        print(file_data)
        return render_template("adminPanel.html", jobDesc= file_data)


if __name__ == '__main__':
    app.run()
