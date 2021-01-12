# Django imports.
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

# LMS app imports.
from lms.token import account_activation_token
from lms.forms.account.register_form import UserRegisterForm
from lms.models.student_model import Profile
from django.core.mail import send_mail
#from django.http import HttpResponse


class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'account/register.html'
    context_object = {
                       "register_form": UserRegisterForm()
                      }

    def get(self, request):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            profile =Profile(user=user)
            user.profile = profile
            user.profile.email_confirmed = False
            user.save()
            #profile.save()


            current_site = get_current_site(request)
            subject = 'Activate Your LMX Account'
            message = render_to_string('account/account_activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            #try:

                #subject = "hello"
                #message = "this is test "
                #email_from = "testaccdjango@gmail.com"
                #recipient_list = "sudhakardlal10@gmail.com"
                #send_mail(subject, message, email_from, recipient_list)

                #return HttpResponse(f"The mail is sent to {recipient_list} ")
            #except:
                #return HttpResponse(f"The mail is not sent to {recipient_list} ")
                #("Email couldnt be sent")

            return redirect('lms:account_activation_sent')

        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)


class AccountActivationSentView(View):

    def get(self, request):
        return render(request, 'account/account_activation_sent.html')


class ActivateView(View):

    def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        #if user is not None and account_activation_token.check_token(user,

        if user is not None:                                                        # token):

            user.is_active = True
            #user.profile.email_confirmed = True
            #user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            username = user.username

            messages.success(request, f"Congratulations {username} !!! "
                                      f"Your account was created and activated "
                                      f"successfully"
                             )

            return redirect('lms:login')
        else:
            return render(request, 'account/account_activation_invalid.html')