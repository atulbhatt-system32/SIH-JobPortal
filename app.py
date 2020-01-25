import PyPDF2
from flask import Flask, render_template, request
from pathlib import Path
import os
import sqlite3

app = Flask(__name__)


@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/registerMe')
def registerMe():
    return render_template('registration.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        if request.form['username'] == "atulbhatt98@gmail.com" and request.form['password'] == "admin":
            return render_template('adminPanel.html')

    return render_template('login.html')


@app.route('/adminPanel')
def adminPanel():
    portal_db()
    return render_template('adminPanel.html')


def scrap(pathToFile):
    pdfFileObj = open(pathToFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    totalPages = pdfReader.numPages
    pdfData = ""
    for i in range(totalPages):
        pageObj = pdfReader.getPage(i)
        pdfData = pdfData + pageObj.extractText()
    jobData = {}
    pdfData = pdfData.split(':')
    for i in range(len(pdfData)):
        if "Title" in pdfData[i]:
            jobData['jobTitle'] = pdfData[i + 1].replace("\n", "").replace("Job Title", "").replace("Job Description",
                                                                                                    "").replace(
                "Qualification", "")
        if "Description" in pdfData[i]:
            jobData['jobDesc'] = pdfData[i + 1].replace("\n", "")
        if "Qualification" in pdfData[i]:
            jobData['jobQualification'] = pdfData[i + 1].replace("\n", "").replace("-", ",")
        if "Salary" in pdfData[i]:
            jobData['Salary'] = pdfData[i + 1].replace("\n", "").replace("-", ",")
        if "Vacancies" in pdfData[i]:
            jobData['Vacancies'] = pdfData[i + 1].replace("\n", "").replace("-", "\n")

    return jobData


@app.route('/jobDataTable', methods=['GET', 'POST'])
def jobDataTable():
    if request.method == 'POST':

        titleDB = request.form['jobTitle']
        descDB = request.form['jobDesc']
        qualDB = request.form['jobQual']
        salDB = request.form['jobSal']
        locDB = request.form['jobLoc']
        vacDB = request.form['jobVac']
        conn = sqlite3.connect('JOB PORTAL.db')
        cur = conn.cursor()
        cur.execute("INSERT into published_jobsPost(jobTitle, jobDesc, jobQual, jobSalary, jobLocation, jobVacancies) values(?,?,?,?,?,?)",
                     (titleDB, descDB, qualDB, salDB, locDB, vacDB))
        conn.commit()
        tableData = {"title": titleDB, "desc": descDB, "qual": qualDB, "sal": salDB, "loc": locDB, "vac": vacDB}
        print("Records created successfully");
        conn.close()
    return render_template('jobs.html', tableData=tableData)


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    conn = sqlite3.connect('JOB PORTAL.db')
    cur = conn.cursor()
    cur.execute("select * from published_jobsPost")
    rows = cur.fetchall()
    return render_template('jobs.html', rows=rows)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')


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
        if my_file.is_file():
            formData = scrap(location)
            return render_template("adminPanel.html", formData=formData)
        else:
            return render_template("adminPanel.html")


def portal_db():
    conn = sqlite3.connect('JOB PORTAL.db')
    conn.execute('CREATE TABLE IF NOT EXISTS  published_jobsPost(id INTEGER PRIMARY KEY AUTOINCREMENT, jobTitle TEXT, jobDesc TEXT,jobQual TEXT, jobSalary TEXT, jobLocation TEXT, jobVacancies TEXT)')
    print("Table created successfully")

def users_db():
    conn = sqlite3.connect('users.db')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS  users(username TEXT PRIMARY KEY ,email TEXT PRIMARY KEY , password  TEXT NOT NULL , question TEXT NOT NULL , answer TEXT NOT NULL )')
    print("User created successfully")
    conn.close()





if __name__ == '__main__':
    app.run()
