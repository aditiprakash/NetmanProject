# make sure you run it using sudo
from socket import *
import smtplib
import sys

# try:
#     from socket import *
# except:
#     print("Install socket first.")
# try:
#     import smtplib
# except:
#     print("Install smtplib first.")
# try:
#     import sys
# except:
#     print("Install sys first.")

def trap_main():
    serverSocket = socket(AF_INET,SOCK_DGRAM)
    trapPort = 1620
    serverSocket.bind(("198.51.100.2",trapPort))

    while True:
        print("SNMP server is ready to listen to trap messages.")
        text = serverSocket.recvfrom(1024)
        addr = text[1]
        subject = 'Trap Alert from '+addr[0]
        username = 'wdtcnetman21@gmail.com'
        password = 'Netman123'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        fromaddr = 'wdtcnetman21@gmail.com'
        toaddrs  = 'fanshen222@gmail.com'
        message = 'Subject :{}\n\n{}'.format(subject,text)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
        print('A trap alert is sent.')
