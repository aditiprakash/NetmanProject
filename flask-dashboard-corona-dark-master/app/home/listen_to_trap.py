try:
    from socket import *
except:
    print("Install socket first.")
try:
    import smtplib
except:
    print("Please install smtplib first.")
try:
    import sys
except:
    print("Please install sys first.")


serverSocket = socket(AF_INET,SOCK_DGRAM)
trapPort = 162

serverSocket.bind(("198.51.100.2",trapPort))
# serverSocket.listen(1)

while True:
    print("Server is ready.")
    # connectionSocket,addr = serverSocket.accept()
    text = serverSocket.recvfrom(1024)
    addr = text[1]
    # send email notification
    # text = str(text, encoding='utf-8')
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
    # connectionSocket.close()
