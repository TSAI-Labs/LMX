from django.db import models
from django.core.mail import send_mail
import lmx.settings

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        #subscribers = Subscriber.objects.filter(confirmed=True, is_subscribed=True)
        subscribers = Subscriber.objects.filter(confirmed=True)
        #sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        recipient_list = []
        for sub in subscribers:
            recipient_list.append(sub.email)

        if len(recipient_list) == 0:
            return
        try:
            subject = self.subject
            email_from=settings.EMAIL_HOST_USER
            message=contents + (
                        '<br><a href="{}?email={}&conf_num={}">Unsubscribe</a>.').format(
                            request.build_absolute_uri('/account/subscribe_delete/'),
                            sub.email,
                            sub.conf_num)
            send_mail( subject, message, email_from, recipient_list )
        except:
            print("Got exception while sending mails")
