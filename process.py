import spacy
import fitz
import hashlib

#mengubah file pdf menjadi dictionary
def resumeExtraction(resumeName):
    nlp = spacy.load('./modelML/output/model-best')
    fname = resumeName
    doc = fitz.open(fname)
    text = " "
    biodata = {
        "AWARDS" : [],
        "CERTIFICATION" :[] ,
        "COLLEGE NAME":[],
        "COMPANIES WORKED AT":[],
        "CONTACT":[],
        "DEGREE":[],
        "DESIGNATION":[],
        "EMAIL ADDRESS":[],
        "LANGUAGE":[],
        "LINKEDIN LINK":[],
        "LOCATION":[],
        "NAME":[],
        "SKILLS":[],
        "UNIVERSITY":[],
        "Unlabelled":[],
        "WORKED AS":[],
        "YEAR OF GRADUATION":[],
        "YEARS OF EXPERIENCE":[],
    }

    for page in doc:
        text = text + str(page.get_text())

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ not in biodata:
            biodata[ent.label_] = [ent.text]
        else:
            biodata[ent.label_].append(ent.text)
    
    return biodata
            

#melihat isi resume dengan key dan value yang sesuai
def seeResume(resumeFile):
    resume = resumeExtraction(resumeFile)

    for key, value in resume.items():
        print(key,"->",value)
        print('\n')


#menghitung berapa skor yang didapat resume
def calculateResume(resumeFile, skills):
    resumeData = resumeExtraction(resumeFile)
    hasSkill = 0
    totalScore = 0

    for skill in skills:
        if skill in resumeData['SKILLS']:
            hasSkill = hasSkill + 2
    
    if(hasSkill != 0):
        for key, value in resumeData.items():
            if key != "SKILLS":
                totalScore += len(value)
    else:
        totalScore = 0

    return str(totalScore + hasSkill)


#mengekripsikan password menjadi md5
def encryptPassword(password):
    # Konversi sandi menjadi byte sebelum dienkripsi
    byte_password = password.encode('utf-8')

    # Buat objek hash MD5
    hash_object = hashlib.md5(byte_password)

    # Enkripsi sandi menggunakan MD5 dan kembalikan dalam bentuk hexadecimal
    encrypted_password = hash_object.hexdigest()
    return encrypted_password


#memisahkan data per feature
def featureExtraction(resume, feature):
    skills = resumeExtraction(resume)[feature]
    skills_without_newline = [skill.replace('\n', '') for skill in skills]
    return (', '.join(skills_without_newline))


resume = './test/resume_2.pdf'
skills_to_check = ['Flask']
calculateResume(resume,skills_to_check)

print(calculateResume(resume, skills_to_check))