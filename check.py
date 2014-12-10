import smtplib
import socket
import time
import timeit
from datetime import datetime
from pytz import timezone

REMOTE_SERVER = "www.google.com"
waitTime=3
PSTzone=timezone('US/Pacific')
def is_connected():
    try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
        host=socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

def genReportApend(i):
    PST_time = datetime.now(PSTzone)
    with open("connetionCheckReport.txt", "a") as ConnectionFile:
        ConnectionFile.write(str(PST_time.strftime("%H:%M:%S"))+" at %s" % PST_time.strftime("%d")+"%s" % PST_time.strftime("%B")+"%s" % PST_time.strftime("%Y")+" "+str(i)+"\r\n")
        ConnectionFile.close()
def sendemail(timeelape,i):
    PST_time = datetime.now(PSTzone)
    fromaddr='haaahhh@gmail.com'
    toaddrs='chunghr@gmail.com'
    msg = " ".join([" <!DOCTYPE html>",
    "<html>",
    "   <head>",
    "       <style>",
    "           table,th,td",
    "           {border:1px solid black;border-collapse:collapse;}",
    "              th,td",
    "           {padding:5px;}",
    "       </style>",
    "   </head>",
    "   <body>",
    "<table style=\"width:300px\">",
    "<tr><th>Situation</th><th> time and date </th><th> Offline gap(sec)</th></tr>",
    "<tr><td>Internet had disconnected(could not ping google)</td><td>",
    str(PST_time.strftime("%H:%M:%S"))+" at %s" % PST_time.strftime("%d")+"%s" % PST_time.strftime("%B")+"%s" % PST_time.strftime("%Y"),
    "</td><td>"+str(i)+"</td></tr>",
    "</table>",
    "</body>",
    "</html>"])
    username = 'liamgymtnawuoykcufehtyhw'
    password = '9YqFUoe2*bU2eEEzH2KR'
    headers = "\r\n".join(["from: " +fromaddr,
                       "subject: " + "Internet state report",
                       "to: " + toaddrs,
                       "mime-version: 1.0",
                       "content-type: text/html"])

    # body_of_email can be plaintext or html!
    content = headers + "\r\n\r\n" + msg
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    print server.helo_resp
    server.sendmail(fromaddr, toaddrs, content)
    server.quit()
starttime=0
endtime=0
timepassed=0
i=0
while True:
    while is_connected():
        time.sleep(waitTime)
        ##print 'connected1'
        endtime=timeit.timeit()
        if not starttime==0:
            ##print 'not connected and sent mail'
            timepassed=endtime-starttime
            sendemail(timepassed,i)
            genReportApend(i)
            starttime=0
            endtime=0
        else:
            starttime=0
            endtime=0
    else:
        ##print 'not connected record time'
        starttime=timeit.timeit()
        i=i+1
        time.sleep(1)
