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

        #masukkan data ke database mysql
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users(name, username, password) VALUES (%s,%s, %s)', (name,username, password))
        mysql.connection.commit()
        cursor.close()

        return "Registration successful"


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


#masukkan data resume ke database
@app.route('/input-resume',methods=['POST'])
def inputResume():
    if 'resume' not in request.files:
        return jsonify({"message":"no file"}), 400

    lowongan = request.form.get('lowongan') if request.form.get('lowongan') else None

    #nyimpan resume ke folder python
    resumeFile = request.files['resume']
    _, fileExtension = os.path.splitext(resumeFile.filename)
    randomHex = secrets.token_hex(8)

    resumeName = randomHex + fileExtension
    resumePath = os.path.join('resume', resumeName)
    resumeFile.save(resumePath)

    #ngambil nilai resume per feature untuk input ke database
    award = featureExtraction(f'./resume/{resumeName}',"AWARDS").lower
    certification = featureExtraction(f'./resume/{resumeName}',"CERTIFICATION").lower
    collegeName = featureExtraction(f'./resume/{resumeName}',"COLLEGE NAME").lower
    companies = featureExtraction(f'./resume/{resumeName}',"COMPANIES WORKED AT").lower
    contact = featureExtraction(f'./resume/{resumeName}',"CONTACT").lower
    degree = featureExtraction(f'./resume/{resumeName}',"DEGREE").lower
    designation = featureExtraction(f'./resume/{resumeName}',"DESIGNATION").lower
    email = featureExtraction(f'./resume/{resumeName}',"EMAIL ADDRESS").lower
    language = featureExtraction(f'./resume/{resumeName}',"LANGUAGE").lower
    linkedin = featureExtraction(f'./resume/{resumeName}',"LINKEDIN LINK").lower
    location = featureExtraction(f'./resume/{resumeName}',"LOCATION").lower
    name = featureExtraction(f'./resume/{resumeName}',"NAME").lower
    skills = featureExtraction(f'./resume/{resumeName}',"SKILLS").lower
    university = featureExtraction(f'./resume/{resumeName}',"UNIVERSITY").lower
    unlabelled = featureExtraction(f'./resume/{resumeName}',"Unlabelled").lower
    worked = featureExtraction(f'./resume/{resumeName}',"WORKED AS").lower
    graduation = featureExtraction(f'./resume/{resumeName}',"YEAR OF GRADUATION").lower
    experience = featureExtraction(f'./resume/{resumeName}',"YEARS OF EXPERIENCE").lower

    #masukkan data ke database
    cursor = mysql.connection.cursor()
    cursor.execute('insert into resume(awards, certification, `college name`, `companies worked at`, contact, degree, designation, `email address`, language, `linkedin link`, location, name, skills, university, unlabelled, `worked as`, `year of graduation`,`years of experience`, file, lowongan) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)',(award, certification, collegeName, companies, contact, degree, designation, email, language, linkedin, location, name, skills, university, unlabelled, worked, graduation, experience, resumeName,lowongan))
    mysql.connection.commit()
    cursor.close()
    
    return 'sudah masuk ke database'


#melihat isi seluruh resume dan mengurutkan berdasarkan skill yang diinputkan recruiter
@app.route('/all-resume',methods=['GET'])
def getResume():
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


#membaca file resume milik pelamar
@app.route('/read-resume',methods=['GET'])
def readResume():
     resumeFileName = request.args.get('file-name')
     filePath = f'./resume/{resumeFileName}'
     return send_file(filePath,as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


#input lowongan baru
@app.route('/input-vacancy', methods=['POST', 'GET'])
def input_vacancy():
    if request.method == 'GET':
        return "Register by filling the registration form."

    if request.method == 'POST':
        #ngambil data dari api
        judulLowongan = request.form.get('judul-lowongan')
        deskripsiLowongan = request.form.get('deskripsi-lowongan')

        #masukkan data ke database mysql
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO lowongan(judul, deskripsi) VALUES (%s,%s)', (judulLowongan, deskripsiLowongan))
        mysql.connection.commit()
        cursor.close()

        return "lowongan baru sudah dibuat"
    

#lihat lowongan lowongan baru
@app.route('/read-vacancy', methods=['GET'])
def read_vacancy():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from lowongan")
        lowongans = cursor.fetchall()

        result=[]

        for row in lowongans:
            item = {
                "judul" : row[1],
                "deskripsi" : row[2],
            }
            
            result.append(item)

        return jsonify({"lowongan":result})
        