from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.conf import settings
from django.core.mail import EmailMessage


class EmailService:
    """Send templated HTML email via Django's configured EMAIL_BACKEND (e.g. SMTP)."""

    def __init__(self):
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def send_mail(self, template, subject, to, context, reply_to=None):
        """
        Render `template` with `context` and send HTML email to `to`.

        reply_to: optional list of addresses for the Reply-To header.
        """
        reply_to = list(reply_to or [])
        html_body = render_to_string(template, context)
        subject = force_str(subject)

        kwargs = {
            "subject": subject,
            "body": html_body,
            "from_email": self.from_email,
            "to": [to],
        }
        if reply_to:
            kwargs["reply_to"] = reply_to

        message = EmailMessage(**kwargs)
        message.content_subtype = "html"
        message.send()
