from email.utils import make_msgid
from django.contrib.auth.models import User
from project.sparta_8688631f3d.sparta_07864420ce import qube_7bd77509b9 as qube_7bd77509b9
from spartaqube_app.secrets import sparta_5f33e0d2c4
from project.logger_config import logger


def send(emailObj, USERNAME_SMTP=None, PASSWORD_SMTP=None, EMAIL_SMTP=None,
    HOST=None, PORT=25, SENDERNAME=None):
    return sendEmailFunc(emailObj, USERNAME_SMTP, PASSWORD_SMTP, EMAIL_SMTP,
        HOST, PORT, SENDERNAME)


def sendEmailFunc(emailObj, USERNAME_SMTP=None, PASSWORD_SMTP=None,
    EMAIL_SMTP=None, HOST=None, PORT=25, SENDERNAME=None):
    """
        Sending email with SES, GMAIL etc..."""
    import smtplib
    import email.utils
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.base import MIMEBase
    RECIPIENT = ','.join(emailObj.getRecipients())
    if SENDERNAME is None:
        SENDERNAME = 'My Project'
    if USERNAME_SMTP is None:
        secrets_dict = sparta_5f33e0d2c4()
        HOST = secrets_dict['EMAIL_HOST_SMTP']
        USERNAME_SMTP = secrets_dict['EMAIL_USERNAME_SMTP']
        EMAIL_SMTP = secrets_dict['EMAIL_RECIPIENT']
        PASSWORD_SMTP = secrets_dict['EMAIL_PASSWORD_SMTP']
        PORT = secrets_dict['EMAIL_PORT_SMTP']
        SENDERNAME = secrets_dict['EMAIL_SENDERNAME']
    if USERNAME_SMTP is None:
        return {'res': -1, 'errorMsg':
            'You need to configure an email sender service in your profile view'
            }
    SUBJECT = emailObj.getEmailTitle()
    BODY_HTML = emailObj.getHTML()
    msg = MIMEMultipart('related')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, EMAIL_SMTP))
    msg['To'] = RECIPIENT
    msg['Message-ID'] = make_msgid()
    logger.debug('RECIPIENT')
    logger.debug(RECIPIENT)
    b64EncodedArr = emailObj.getEmailB64ImgList()
    imageNameArr = emailObj.getEmailImgNameArr()
    for idx, thisEncodedImg in enumerate(b64EncodedArr):
        part = MIMEBase('image', 'png')
        part.set_payload(thisEncodedImg)
        part.add_header('Content-Transfer-Encoding', 'base64')
        imgName = imageNameArr[idx]
        part['Content-Disposition'] = 'attachment; filename="%s"' % imgName
        msg.attach(part)
    filesArr = emailObj.getFilesArr()
    filesNameArr = emailObj.getFilesNameArr()
    for idx, thisFile in enumerate(filesArr):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(thisFile)
        part.add_header('Content-Transfer-Encoding', 'base64')
        fileName = filesNameArr[idx]
        logger.debug('fileName > ' + str(fileName))
        part['Content-Disposition'] = 'attachment; filename="%s"' % fileName
        msg.attach(part)
    part2 = MIMEText(BODY_HTML, 'html')
    msg.attach(part2)
    logger.debug('SEND EMAIL NOW')
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(EMAIL_SMTP, RECIPIENT, msg.as_string())
        server.close()
    except Exception as e:
        print('Error: ', e)
        return {'res': -1, 'errorMsg': str(e)}
    else:
        return 'Email sent!'

#END OF QUBE
