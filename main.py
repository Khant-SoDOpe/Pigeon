from flask import Flask,render_template,request
import random
import csv
import data
import os

answer = ''
count = 13

#add user's text 
def replace_text(contant,mail):
    with open(f"data/user_data/{Now_Username}/{mail}.txt") as contants:
        read = contants.read()
        bb = read.replace("[Content]",contant)
        with open(f"data/user_data/{Now_Username}/{mail}.txt", "w") as myfile:
            myfile.write(bb)

#check username than check password is the same or not
def datalogin(Now_Username,Now_Password):
    with open("data/data.txt")as data:
        name_password = csv.DictReader(data)
        for names in name_password:
            if names["Usernames"] == Now_Username:
                if names["Passwords"] == Now_Password:
                    global answer
                    answer = 'pass'

#check username is already added or not that add data to file
def datasignup(Now_Username,Now_Password):
    with open("data/data.txt")as data:
        name_password = csv.DictReader(data)
        for names in name_password:
            if names["Usernames"] == Now_Username:
                global answer
                answer = 'notpass'

        if answer == 'pass':
            if answer != 'pass':
                answer = 'notpass'
            
            user_data = {}
            user_data['Usernames'] = Now_Username
            user_data['Passwords'] = Now_Password
            fieldnames = []
            for key in user_data:
                fieldnames.append(key)

            with open(f"data/data.txt", "a") as data_file:
                writer = csv.DictWriter(data_file, fieldnames)
                writer.writerow(user_data)

#add file with username
def newpath():
    newpath = f'data/user_data/{Now_Username}' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

#check this file is created or not
def filecheck(now_username,receiver_name,email,date,month,contant):#this will check that username and password file will create
    newpath()
    try:
        with open(f"data/user_data/{now_username}/{now_username}.txt",mode='r')as fall:
            pass

    except FileNotFoundError:
        with open(f'data/user_data/{now_username}/{now_username}.txt', 'a') as csvfile:
            fieldnames = ['Sender','Receiver','Email','Date','Month']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            pass
    check_mail(now_username,receiver_name,email,date,month,contant)

#check user already add this mail or not
def check_mail(now_username,receiver_name,email,date,month,contant):
    with open(f"data/user_data/{now_username}/{now_username}.txt") as data:
        mail_data = csv.DictReader(data)
        for mails in mail_data:
            if str(mails['Email']) == str(email):
                global answer
                answer = 'notpass'
                return
        with open(f"data/user_data/{Now_Username}/{email}.txt", 'a')as file:
            files = ["Hi,[name]\n","[Content]\n","From [Sender]"]
            for i in range(3):
                file.write(str(files[i]))
        addmails(now_username,receiver_name,email,date,month,contant)

#add user data to txt file
def addmails(now_username,receiver_names,emails,dates,months,contant):         
        user_data = {}

        user_data['Sender'] = now_username
        user_data['Receiver'] = receiver_names
        user_data["Email"] =  emails
        user_data['Date'] = dates
        user_data["Month"] = months

        fieldnames = []
        for key in user_data:
            fieldnames.append(key)

        with open(f"data/user_data/{now_username}/{now_username}.txt", "a") as data_file:
            writer = csv.DictWriter(data_file, fieldnames)
            writer.writerow(user_data)
        replace_text(contant,emails)


#-------------------------------------------------------------------------------------
app = Flask(__name__)
@app.route("/")
def index():
    data.check_date()
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
    
@app.route("/loginprocess",methods=["POST"])
def loginprocess():
    Now_Username = request.form.get('Username')
    Now_Password = request.form.get('Password')
    global answer
    answer = 'notpass'
    datalogin(Now_Username,Now_Password)
    if answer == 'pass':
        answer = 'notpass'
        return render_template('form.html',username=Now_Username)
    else:
        noti = "Wrong Password"
        return render_template('index.html',noti=noti)

@app.route("/signupprocess",methods=["POST"])
def signupprocess():
    global Now_Username,Now_Password
    Now_Username = request.form.get('Username')
    Now_Password = request.form.get('Password')
    global answer
    answer = 'pass'
    datasignup(Now_Username,Now_Password)
    if answer == 'notpass':
        noti = "Another user already Used This Username"
        return render_template("index.html",noti=noti)
    else:
        
        return render_template("form.html")

@app.route("/final",methods=["POST"])
def final():
    receiver_name = request.form.get("receiver_name")
    email = request.form.get("email")
    month = request.form.get("month")
    contant = request.form.get("message")
    if month == "04" or month == "06" or month == "09" or month == "11":
        date = request.form.get("Date30")
    elif month == "02":
        date = request.form.get("Date29")
    else:
        date = request.form.get("Date31")
    filecheck(Now_Username,receiver_name,email,date,month,contant)
    answer = 'pass'
    if answer == 'notpass':
        noti = "This mail is already used"
        return render_template("index.html",noti=noti)
    else:
        noti = "Sucussfully Completed"
        return render_template("index.html",noti=noti)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=random.randint(2000,9000))