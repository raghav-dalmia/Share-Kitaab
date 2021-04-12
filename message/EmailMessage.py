from app import s
from email.message import EmailMessage
from message.Credentials import me, password


def format_request_message(owner_name, book_title, name, phone, email, reason):
    message = '''
Hi {},

We have received a request for your book "{}" on Share Kitaab.

Details of the person:

    Requested by: {}
    Phone Number: {}
    E-mail: {}
    Reason: {}
    
If you want to donate book(s) to this person, please contact him on your earliest convenience. Make sure to delete 
this book on your website after donation. 

Regards,
Team Share Kitaab

Note: If you need any assistance related to Share Kitaab platform, please drop us a mail on {}.
    '''.format(
        owner_name,
        book_title,
        name,
        phone,
        email,
        reason,
        me
    )
    return message


def sendMessage(to, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to
    msg.set_content(message)
    s.send_message(msg)
