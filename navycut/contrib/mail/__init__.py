from flask_mail import Mail, Message
from flask.globals import current_app
import typing as t


mail = Mail()

__all__ = ('mail', 'send_email', 'send_plain_mail', 'send_html_mail', 'send_mass_mail')

def _set_mimetype(msg:Message, message:str, mimetype:str) -> t.Type[Message]:
    if  mimetype == "html":
        msg.html = message
    else:
        msg.body = message
    return msg

def send_mail(subject:str, 
                message:str, 
                recipients:t.Union[list, str], 
                sender:str=None, 
                html_message:str=None, 
                **options
                ) -> None:
    """
    In most cases, you can send email using navycut.contrib.mail.send_mail()

    :param subject:
        A String.

    :param message:
        A String containg the plain text data.

    :param recipients:
        A list of strings or single email id(string), 
        each an email address. Each member of recipient_list 
        will see the other recipients in the “To:” field of the email message.

    :param sender:
        A String, containing the default email sender id.
        If not provided, Navycut will use the value from SMTP_CONFIGURATION setting.

    :param html_message: 
        If html_message is provided, the resulting email will be a 
        multipart/alternative email with message as the text/plain 
        content type and html_message as the text/html content type.

    :param options:
        the kwargs based param.
        to provide the reply_to system, use options.
    """
    from navycut.conf import settings

    sender = sender or settings.SMTP_CONFIGURATION.get('username')

    msg = Message(subject, 
                sender=sender,
                )

    if isinstance(recipients, list):
        msg.recipients = recipients
    
    elif isinstance(recipients, str):
        msg.add_recipient(recipients)

    if options.get("reply_to", None) is not None:
        msg.reply_to = options['reply_to']   

    if options.get("mimetype", None) is not None:
        msg = _set_mimetype(msg, message, options['mimetype'])
    else:
        msg.body = message

    if html_message is not None:
        msg.html = html_message

    current_app.extensions.get("mail").send(msg) 

def send_plain_mail(subject:str, message:str, sender:str, recipients:t.Union[list, str], **options:t.Any) -> None:
    """
    Similar to navycut.contrib.mail.send_email(),
    to send any plain text email please use this function.

    :param subject:
        A String.

    :param message:
        A String containg the plain text data.

    :param sender:
        A String, containing the default email sender id.
        If not provided, Navycut will use the value from SMTP_CONFIGURATION setting.

    :param recipients:
        A list of strings or single email id(string), 
        each an email address. Each member of recipient_list 
        will see the other recipients in the “To:” field of the email message.

    :param options:
        the kwargs based param.
        to provide the reply_to system, use options.
    """
    return send_mail(subject, message, sender, recipients, mimetype="plain", **options)

def send_html_mail(subject:str, message:str, recipients:t.Union[list, str], sender:str=None, **options:t.Any) -> None:
    """
    In most cases, you can send email using navycut.contrib.mail.send_mail()

    :param subject:
        A String.

    :param message:
        A String containing the html data.

    :param recipients:
        A list of strings or single email id(string), 
        each an email address. Each member of recipient_list 
        will see the other recipients in the “To:” field of the email message.

    :param sender:
        A String, containing the default email sender id.
        If not provided, Navycut will use the value from SMTP_CONFIGURATION setting.

    :param options:
        the kwargs based param.
        to provide the reply_to system, use options.
    """ 
   
    return send_mail(subject, message, sender, recipients, mimetype="html", **options)


def send_mass_mail(datas:t.Union[list, tuple], mimetype:str="plain"):
    """
    navycut.contrib.mail.send_mass_mail() is intended to handle mass emailing.
    
    :param data:
        is a tuple or list in which each element is in this format:
        (subject, message, sender, recipients)

    :param mimetype:
        the mimetype for message body.
        default is "plain", another option is "html".
    """
    from navycut.conf import settings
    
    if not isinstance(datas, tuple):
        datas = tuple(datas)

    with current_app.extensions.get("mail").connect() as con:
        for data in datas:
            subject, message, sender, recipients = data

            if sender == str() or sender is None:
                sender = settings.SMTP_CONFIGURATION.get("username")
            
            msg = Message(subject,
                        sender=sender)
            
            if mimetype is not None:
                msg = _set_mimetype(msg, message, mimetype)
            else:
                msg.body = message
            
            if isinstance(recipients, str):
                msg.add_recipient(recipients)
            
            elif isinstance(recipients, list):
                msg.recipients = recipients

            con.send(msg)