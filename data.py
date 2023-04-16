from email.message import EmailMessage
import csv
import smtplib
import ssl
import os

#first check data/data.txt then open files with username and search with today date name if one of the user date is eqal then send mail with userdata
def c_and_sendmail():
    from datetime import date
    today = date.today()

    month = today.strftime("%m")
    date = today.strftime("%d")

    with open("data/data.txt", "r") as data_file:
        user_data = csv.DictReader(data_file)
        for user in user_data:
            with open(f"data/user_data/{user['Usernames']}/{user['Usernames']}.txt", "r") as data_file:
                user_data = csv.DictReader(data_file)
                for user in user_data:
                    if user['Month'] == month:
                        if user['Date'] == date:
                            username = user['Receiver']
                            sent_mail = user['Email']

                            # Define email sender and receiver
                            email_sender = 'pigeon.bird.mail@gmail.com'
                            email_password = os.environ['Password']
                            email_receiver = sent_mail
                            name = username

                            # Set the subject and body of the email
                            with open(f"data/user_data/{user['Sender']}/{user['Email']}.txt")as letters:
                                orange = letters.read()
                                bb = orange.replace("[name]",name)
                                cc = bb.replace("[Sender]",user['Sender'])
                            subject = 'Birthday Wish'
                            body = cc

                            em = EmailMessage()
                            em['From'] = email_sender
                            em['To'] = email_receiver
                            em['Subject'] = subject
                            em.set_content(body)

                            # Add SSL (layer of security)
                            context = ssl.create_default_context()

                            # Log in and send the email
                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                smtp.login(email_sender, email_password)
                                smtp.sendmail(email_sender, email_receiver, em.as_string())

def check_date():
    with open('data/count.txt')as data:
        from datetime import date
        count = data.read()
        today = date.today()
        date = today.strftime("%d")
        second_date = int(date)
        if int(count) == second_date:
            c_and_sendmail()
            int_count = int(count)
            int_count += 1
            str_count = str(int_count)
            with open("data/count.txt","w")as file:
                file.write(str_count)