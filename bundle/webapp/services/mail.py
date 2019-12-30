from flask_mail import Mail, Message

mail = Mail()

from_email = None

def init_mail(server, conf):
    global from_email
    from_email = conf.pop('SEND_FROM', 'noreply@geopoly.net')

    for k,v in conf.items():
        server.config[k.upper()] = v

    #server.config['MAIL_SUPPRESS_SEND'] = server.testing
    server.config['MAIL_DEBUG'] = bool(server.debug)

    mail.init_app(server)


def send_mail(email, title, content):
    msg = Message(title, sender=('Geopoly', from_email), recipients=[email])

    msg.html = content

    mail.send(msg)
