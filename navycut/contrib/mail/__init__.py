# from flask_mailman import *
from flask import current_app
from flask_mailman import *
from flask_mailman import Mail as OldMail
from flask_mailman import _MailMixin, _Mail

import typing as t
from importlib import import_module
from navycut.conf import settings
from navycut.errors.misc import ConfigurationError


__all__ = ('mail', 'send_email', 'send_mass_mail')

class MailMixin(_MailMixin):

    def _import_backend(self, backend_name:str):
        backend_module_name, backend_class = backend_name.rsplit(".", 1)
        backend_module = import_module(backend_module_name)
        backend = getattr(backend_module, backend_class)
        return backend


    def get_connection(self, backend=None, fail_silently=False, **kwargs):
        """Load an email backend and return an instance of it.

        If backend is None (default), use app.config.MAIL_BACKEND.

        Both fail_silently and other keyword arguments are used in the
        constructor of the backend.
        """
        app = getattr(self, "app", None) or current_app
        try:
            mailman = app.extensions['mailman']
        except KeyError:
            raise ConfigurationError("The current application was not configured properly.")

        try:
            klass = self._import_backend(settings.EMAIL_BACKEND)
    
        except ImportError:
            raise ConfigurationError("Invalid backend: %s" % settings.EMAIL_BACKEND)

        return klass(mailman=mailman, fail_silently=fail_silently, **kwargs)

class _Mailer(_Mail):
    """
    Inherit the default _Mail creator class of flask_mailman.
    """

class Mail(OldMail, MailMixin):
    """
    Inherit the default Mail class of flask_mailman.
    """

    @staticmethod
    def init_mail(config, testing=False):
        # Set default mail backend in different environment
        mail_backend = config.get('MAIL_BACKEND')

        return _Mailer(
            config.get('MAIL_SERVER'),
            config.get('MAIL_PORT'),
            config.get('MAIL_USERNAME'),
            config.get('MAIL_PASSWORD'),
            config.get('MAIL_USE_TLS'),
            config.get('MAIL_USE_SSL'),
            config.get('MAIL_DEFAULT_SENDER'),
            config.get('MAIL_TIMEOUT'),
            config.get('MAIL_SSL_KEYFILE'),
            config.get('MAIL_SSL_CERTFILE'),
            config.get('MAIL_USE_LOCALTIME'),
            config.get('MAIL_FILE_PATH'),
            config.get('MAIL_DEFAULT_CHARSET'),
            mail_backend,
        )


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