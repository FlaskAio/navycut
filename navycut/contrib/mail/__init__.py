from flask_mailman import *
from flask_mailman import Mail
import typing as t


__all__ = ('mail', 'send_email', 'send_mass_mail')


mail:t.Type["Mail"] = Mail()


def send_mail(
        subject:str,
        message:str,
        from_email:t.Optional[str]=None,
        recipient_list:t.List[str]=None,
        fail_silently:bool=False,
        auth_user:t.Optional[str]=None,
        auth_password:t.Optional[str]=None,
        connection=None,
        html_message:t.Optional[str]=None,
            ) -> None:
    """
    In most cases, you can send email using navycut.contrib.mail.send_mail()

    :param subject: 
    A string.

    :param message: 
    A string.

    :param from_email: 
    A string. If None, Navycut will use the value 
    of the MAIL_DEFAULT_SENDER configuration.

    :param recipient_list: 
    A list of strings, each an email address. 
    Each member of recipient_list will see the other 
    recipients in the “To:” field of the email message.

    :param fail_silently: 
    A boolean. When it’s False, send_mail() will raise 
    an smtplib.SMTPException if an error occurs. 
    See the smtplib docs for a list of possible exceptions, 
    all of which are subclasses of SMTPException.

    :param auth_user: 
    The optional username to use to authenticate to the SMTP server. 
    If this isn’t provided, Navycut will use the
    value of the MAIL_USERNAME configuration.

    :param auth_password: 
    The optional password to use to authenticate to the SMTP server. 
    If this isn’t provided, Navycut will use the 
    value of the MAIL_PASSWORD configuration.

    :param connection: 
    The optional email backend to use to send the mail. 
    If unspecified, an instance of the default backend will be used. 
    See the documentation on Email backends for more details.

    :param html_message: 
    If html_message is provided, the resulting email 
    will be a multipart/alternative email with message as 
    the text/plain content type and html_message as the text/html content type.
    """
    mail.send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=fail_silently,
                auth_user=auth_user,
                auth_password=auth_password,
                connection=connection,
                html_message=html_message
                )


def send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    """
    navycut.contrib.mail.send_mass_mail() is intended to handle mass emailing.
    
    :param datatuple:
        datatuple is a tuple in which each element is in this format:
            `(subject, message, from_email, recipient_list)`

    `fail_silently`, `auth_user` and `auth_password` have the same functions as in send_mail().

    Each separate element of datatuple results in a separate email message. 
    As in send_mail(), recipients in the same recipient_list will 
    all see the other addresses in the email messages’ “To:” field.

    for example::

        message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
        message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
        send_mass_mail((message1, message2), fail_silently=False)
    """
    mail.send_mass_mail(
                    datatuple=datatuple, 
                    fail_silently=fail_silently, 
                    auth_user=auth_user, 
                    auth_password=auth_password, 
                    connection=connection
                    )