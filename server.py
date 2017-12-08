## You can run this script as a cron job to monitor the response code of remote web servers, like
# * * * * * /usr/local/bin/python3 web_server_monitor.py https://www.yahoo.com
#
# If the response code is not 200, an alert will be sent to the specified recipient email addresses.

import sys
import requests
from smtplib import SMTP


def emailAlert(recipient, server, error):
    gmail_user = "ryan.taylor0@gmail.com"
    gmail_pwd = "Agendavibrate1!"
    FROM = 'ryan.taylor0@gmail.com'
    TO = recipient #must be a list
    SUBJECT = "SERVER ERROR: " + server
    TEXT = "Error code/message: " + error

    # Prepare actual message
    msg = """From: {0}\nTo: {1}\nSubject: {2}\n\n{3}
    """ .format(FROM, ", ".join(TO), SUBJECT, TEXT)

    print(msg)

    debuglevel = 0

    smtp = SMTP("smtp.gmail.com", 587)
    smtp.set_debuglevel(debuglevel)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(gmail_user, gmail_pwd)
    smtp.sendmail(FROM, TO, msg)


try:
    server = sys.argv[1];
    recipient = ['ryan@allteamz.com']
    r = requests.head(server)
    if r.status_code != 200 :
        emailAlert(recipient, server, str(r.status_code));
except requests.ConnectionError:
    print("failed to connect")
    #emailAlert(recipient, server, "failed to connect");