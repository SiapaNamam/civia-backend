import secrets
from flask import Flask, jsonify, request, send_file
from flask_mysqldb import MySQL
import os
from process import encryptPassword
from process import featureExtraction
from process import calculateResume

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'civia'
app.config['UPLOAD_FOLDER'] = 'resume'

mysql = MySQL(app)


#login akun recruiter
@app.route('/login', methods=['POST'])
def login():
    
    #ngambil data yg dikirim melalui api
    username = request.form.get('username')
    password = request.form.get('password')

    #cek data ke database mysql
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users where username = %s",(username,))
    user = cursor.fetchone()

    #kondisi setiap login
    if user:
        hashedPassword = encryptPassword(password)

        if user[3] == hashedPassword:
            return jsonify({"Message":"Login berhasil"}),200
        else:
            return jsonify({"Message":"Password Wrong"})
    else:
        return jsonify({"message":"Username tidak tersedia"})


#register akun recruiter
@app.route('/register', methods=['POST', 'GET'])
def register_recruiter():
    if request.method == 'GET':
        return "Register by filling the registration form."

    if request.method == 'POST':
        
        #ngambil data dari api
        name = request.form.get('name')
        username = request.form.get('username')
        password = encryptPassword(request.form.get('password'))
        dateOfBirth = request.form.get('dateOfBirth') #format date yyyy-mm-dd
        email = request.form.get('email')

        #masukkan data ke database mysql
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users(name, username, password, date_of_birth,email) VALUES (%s,%s, %s, %s, %s)', (name,username, password, dateOfBirth, email))
        mysql.connection.commit()
        cursor.close()

        return "Registration successful"


#jumlah pelamar
@app.route('/hr/applicant/count',methods=['GET'])
def count_applicant():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from resume")
    countApplicant = cursor.fetchall()

    return jsonify({"total pelamar":countApplicant})


#jumlah lowongan
@app.route('/hr/vacancy/count', methods=['GET'])
def count_vacancy():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT count(*) from lowongan")
        countLowongan = cursor.fetchall()


        return jsonify({"jumlah lowongan":countLowongan})


#menambahkan lowongan
@app.route('/hr/vacancy/add', methods=['POST'])
def add_vacancy():

        #ngambil data dari api
        company = request.form.get('company')
        jobName = request.form.get('jobName')
        salary = request.form.get('salary')
        lastDate = request.form.get('lastDate')
        skills = request.form.get('skills')

        if 'jobDescription' in request.files:
             jobDescriptionFile = request.files['jobDescription']
             jobDescriptionText = jobDescriptionFile.read().decode('utf-8')
        else:
             jobDescriptionText =''

        #masukkan data ke database mysql
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO lowongan(company, job_name, salary, last_date, skills, job_description) VALUES (%s,%s,%s,%s,%s,%s)', (company, jobName, salary, lastDate, skills,jobDescriptionText))
        mysql.connection.commit()
        cursor.close()

        return "lowongan baru sudah dibuat"


#lihat lowongan baru
@app.route('/hr/vacancy/read', methods=['GET'])
def hr_read_vacancy():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT job_name, company, salary, last_date from lowongan")
        lowongans = cursor.fetchall()

        result=[]

        for row in lowongans:
            item = {
                "job_name" : row[0],
                "company" : row[1],
                "salary" : row[2],
                "last_date" : row[3]
            }
            
            result.append(item)

        return jsonify({"lowongan":result})
        


#melihat semua data dari candidat berdasarkan lowongan
@app.route('/hr/candidate/read',methods=['GET'])
def readResume():
    userSkills = request.args.get('skills').split(',') if request.args.get('skills') else None
    lowongan = request.args.get('lowongan') if request.args.get('lowongan') else None 

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from resume where lowongan =",lowongan)
    resumes = cursor.fetchall()

    result=[]

    for row in resumes:
        item = {
            "awards":row[1],
            'certification':row[2], 
            "college name":row[3], 
            "companies worked at":row[4], 
            "contact":row[5], 
            "degree":row[6], 
            "designation":row[7], 
            "email address":row[8], 
            "language":row[9], 
            "linkedin link":row[10], 
            "location":row[11], 
            "name":row[12], 
            "skills":row[13], 
            "university":row[14], 
            "unlabelled":row[15], 
            "worked as":row[16], 
            "year of graduation":row[17],
            "years of experience":row[18], 
            "lowongan":row[19], 
            "file":row[20]
        }

        if userSkills:
            item['score'] = calculateResume(item, userSkills)
        
        result.append(item)

    if userSkills:
        sortedResume = sorted(result, key=lambda x:x['score'], reverse=True)
    else:
        sortedResume = result

    return jsonify({"Resumes":sortedResume})


#melihat detail dari satu candidat
@app.route('/hr/candidate/detail',methods=['GET'])
def detailResume():
    userSkills = request.args.get('skills').split(',') if request.args.get('skills') else None
    lowongan = request.args.get('lowongan') if request.args.get('lowongan') else None
    applicantName = request.args.get('applicantName') if request.args.get('applicantName') else None

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from resume where lowongan =",lowongan, "and name =",applicantName)
    resumes = cursor.fetchall()

    result=[]

    for row in resumes:
        item = {
            "awards":row[1],
            'certification':row[2], 
            "college name":row[3], 
            "companies worked at":row[4], 
            "contact":row[5], 
            "degree":row[6], 
            "designation":row[7], 
            "email address":row[8], 
            "language":row[9], 
            "linkedin link":row[10], 
            "location":row[11], 
            "name":row[12], 
            "skills":row[13], 
            "university":row[14], 
            "unlabelled":row[15], 
            "worked as":row[16], 
            "year of graduation":row[17],
            "years of experience":row[18], 
            "lowongan":row[19], 
            "file":row[20]
        }

        if userSkills:
            item['score'] = calculateResume(item, userSkills)
        
        result.append(item)

    if userSkills:
        sortedResume = sorted(result, key=lambda x:x['score'], reverse=True)
    else:
        sortedResume = result

    return jsonify({"Resumes":sortedResume})


#lihat lowongan baru
@app.route('/applicant/vacancy/read', methods=['GET'])
def applicant_read_vacancy():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT job_name, company, salary, last_date from lowongan")
        lowongans = cursor.fetchall()

        result=[]

        for row in lowongans:
            item = {
                "job_name" : row[1],
                "company" : row[2],
                "salary" : row[3],
                "lastDate" : row[4],
            }
            
            result.append(item)

        return jsonify({"lowongan":result})


#lihat lowongan baru
@app.route('/applicant/vacancy/detail', methods=['GET'])
def read_vacancy():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT skills, job_description from lowongan")
        lowongans = cursor.fetchall()

        result=[]

        for row in lowongans:
            item = {
                "skills" : row[1],
                "job description" : row[2]
            }
            
            result.append(item)

        return jsonify({"detail lowongan":result})



#masukkan data resume ke database
@app.route('/applicant/vacancy/add',methods=['POST'])
def inputResume():
    if 'resume' not in request.files:
        return jsonify({"message":"no file"}), 400

    job_name = request.form.get('job_name') if request.form.get('job_name') else None

    #nyimpan resume ke folder python
    resumeFile = request.files['resume']
    _, fileExtension = os.path.splitext(resumeFile.filename)
    randomHex = secrets.token_hex(8)

    resumeName = randomHex + fileExtension
    resumePath = os.path.join('resume', resumeName)
    resumeFile.save(resumePath)

    #ngambil nilai resume per feature untuk input ke database
    award = str(featureExtraction(f'./resume/{resumeName}',"AWARDS")).lower()
    certification = str(featureExtraction(f'./resume/{resumeName}',"CERTIFICATION")).lower()
    collegeName = str(featureExtraction(f'./resume/{resumeName}',"COLLEGE NAME")).lower()
    companies = str(featureExtraction(f'./resume/{resumeName}',"COMPANIES WORKED AT")).lower()
    contact = str(featureExtraction(f'./resume/{resumeName}',"CONTACT")).lower()
    degree = str(featureExtraction(f'./resume/{resumeName}',"DEGREE")).lower()
    designation = str(featureExtraction(f'./resume/{resumeName}',"DESIGNATION")).lower()
    email = str(featureExtraction(f'./resume/{resumeName}',"EMAIL ADDRESS")).lower()
    language = str(featureExtraction(f'./resume/{resumeName}',"LANGUAGE")).lower()
    linkedin = str(featureExtraction(f'./resume/{resumeName}',"LINKEDIN LINK")).lower()
    location = str(featureExtraction(f'./resume/{resumeName}',"LOCATION")).lower()
    name = str(featureExtraction(f'./resume/{resumeName}',"NAME")).lower()
    skills = str(featureExtraction(f'./resume/{resumeName}',"SKILLS")).lower()
    university = str(featureExtraction(f'./resume/{resumeName}',"UNIVERSITY")).lower()
    unlabelled = str(featureExtraction(f'./resume/{resumeName}',"Unlabelled")).lower()
    worked = str(featureExtraction(f'./resume/{resumeName}',"WORKED AS")).lower()
    graduation = str(featureExtraction(f'./resume/{resumeName}',"YEAR OF GRADUATION")).lower()
    experience = str(featureExtraction(f'./resume/{resumeName}',"YEARS OF EXPERIENCE")).lower()

    #masukkan data ke database
    cursor = mysql.connection.cursor()
    cursor.execute('insert into resume(awards, certification, `college name`, `companies worked at`, contact, degree, designation, `email address`, language, `linkedin link`, location, name, skills, university, unlabelled, `worked as`, `year of graduation`,`years of experience`, file, job_name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)',(award, certification, collegeName, companies, contact, degree, designation, email, language, linkedin, location, name, skills, university, unlabelled, worked, graduation, experience, resumeName, job_name))
    mysql.connection.commit()
    cursor.close()
    
    return 'sudah masuk ke database'



#membaca file resume milik pelamar
@app.route('/hr/resume-file',methods=['GET'])
def openResumeFile():
     resumeFileName = request.args.get('file-name')
     filePath = f'./resume/{resumeFileName}'
     return send_file(filePath,as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)



