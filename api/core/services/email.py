from django.template.loader import render_to_string
from django.utils.encoding import force_str
from mailjet_rest import Client
from django.conf import settings
from django.core.mail import EmailMessage


class EmailService:
    """
    A service class for sending emails using Mailjet.
    """

    def __init__(self):
        """
        Initialize the EmailService with Mailjet API credentials.
        """
        self.mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def send_mail(self, template, subject, to, context, reply_to=[]):
        """
        Sends an email using a provided template, subject, recipient, and context.

        Args:
            template (str): Path to the HTML template.
            subject (str): Subject of the email.
            to (str): Recipient email address.
            context (dict): Context data for the email template.
            reply_to (list): List of reply-to email addresses. Defaults to None.

        Returns:
            dict: The response from Mailjet.
        """
        reply_to = reply_to or []

       
        message_template = render_to_string(template, context)
        subject = force_str(subject)

            
        data = {
                "Messages": [
                    {
                        "From": {
                            "Email": self.from_email,
                        },
                        "To": [{"Email": to}],
                        "Subject": subject,
                        "HTMLPart": message_template
                    }
                ]
            }

           
        self.mailjet.send.create(data=data)
 
      
        

       

