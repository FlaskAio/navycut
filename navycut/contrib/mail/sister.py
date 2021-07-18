from navycut.core.app_config import AppSister
from . import mail

"""
The default app to deliver the mail service.
Internally it's using the flask-mail
("https://pypi.org/project/Flask-Mail/") module.

Special thanks to Matt Wright("https://github.com/mattupstate")
to provide this module to us to write a fullstack project like navycut.

Special thanks to all of you who are using this project. 
Please encourage us by providing your valuable feedback.

You can always reach me at: aniketsarkar@yahoo.com
"""


class MailSister(AppSister):
    seize_power = True
    name="mail_service_sister"
    extra_ins = (mail, )