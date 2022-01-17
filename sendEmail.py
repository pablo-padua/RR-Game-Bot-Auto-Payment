import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def sendEmail(currentTime):

    file = 'paymentReceipt.xlsx'
    username = ''
    password = ''
    send_from = ''
    send_to = ''
    Cc = ''
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Cc'] = Cc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'War Report - Payment'
    server = smtplib.SMTP('smtp.gmail.com')
    port = '587'
    fp = open(file, 'rb')
    part = MIMEBase('application', 'vnd.ms-excel')
    part.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment',
                    filename='BotPaymentReport.xlsx')
    msg.attach(part)
    html = """
    <html>
    <head></head>
    <body>
        <p><b>Hello, </b><br>
        <b>I attached the excel file from your last payment using this bot to this e-mail</b> <br>Enjoy!
        </p>
        <br>
        <p>Generated at: """+{currentTime}+"""</p>
    </body>
    </html>
    """

    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    smtp = smtplib.SMTP('smtp.gmail.com')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to.split(',') +
                  msg['Cc'].split(','), msg.as_string())
    smtp.quit()
