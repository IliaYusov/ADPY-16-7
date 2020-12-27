import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.header


class Gmail:
    GMAIL_SMTP = 'smtp.gmail.com'
    GMAIL_IMAP = 'imap.gmail.com'

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send(self, subject: str, recipients: list, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        try:
            with smtplib.SMTP(Gmail.GMAIL_SMTP, 587) as server:
                server.ehlo()  # identify ourselves to smtp gmail client
                server.starttls()  # secure our email with tls encryption
                server.login(self.login, self.password)
                server.sendmail(self.login, recipients, msg.as_string())
                print(f'Email to {recipients} sent.')
        except smtplib.SMTPException as error:
            print(f'Something went wrong. {error}')

    def receive(self, header=None):
        try:
            with imaplib.IMAP4_SSL(Gmail.GMAIL_IMAP) as server:
                server.login(self.login, self.password)
                server.list()
                server.select('inbox')
                criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
                result, data = server.uid('search', None, criterion)
                if data[0] == b'':
                    return 'There are no letters with current header'
                latest_email_uid = data[0].split()[-1]
                result, data = server.uid('fetch', latest_email_uid, 'RFC822')
                raw_email = data[0][1]
                return email.message_from_bytes(raw_email)
        except imaplib.IMAP4.error as error:
            print(f'Something went wrong. {error}')


def msg_decode(data):
    subject, subject_encoding = email.header.decode_header(data['subject'])[0]
    if type(subject) is not str:
        subject = subject.decode()
    print('subj:', subject)
    print('from:', end=' ')
    for from_data in email.header.decode_header(data['from']):
        from_part, from_encoding = from_data
        if type(from_part) is not str:
            from_part = from_part.decode()
        print(from_part, end=' ')
    print('\ndate:', data['date'])
    print('body:')
    for part in data.walk():
        if part.get_content_type() == 'text/plain':
            print(part.get_payload(decode=True).decode('utf-8'))


if __name__ == '__main__':
    mail_client = Gmail('test@gmail.com', 'test_password')

    mail_client.send('test subject', ['test@pisem.net'], 'message')

    msg_decode(mail_client.receive())
