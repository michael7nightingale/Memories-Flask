from smtplib import SMTP_SSL

from config import get_settings


def create_smtp_server() -> SMTP_SSL:
    settings = get_settings()
    smtp_server_ = SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp_server_.ehlo()
    smtp_server_.login(user=settings.EMAIL_USER, password=settings.EMAIL_PASSWORD)
    return smtp_server_


smtp_server = create_smtp_server()


def send_message(subject: str, to_addrs: list, body: str) -> None:
    email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (get_settings().EMAIL_USER, ", ".join(to_addrs), subject, body)
    smtp_server.sendmail(
        from_addr="suslanchikmopl@gmail.com",
        to_addrs=to_addrs,
        msg=email_text
    )
