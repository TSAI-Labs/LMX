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
from lms.forms.dashboard.emailadmin_form import EmailAdminForm
from lms.models.users_model import Staff

class DashboardEmailAdminView(View):
    """
      View to let users register
    """
    template_name = 'dashboard/student/email_admin.html'
    context_object = {
                       "emailadmin_form": EmailAdminForm()
                      }

    def get(self, request):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        emailadmin_form = EmailAdminForm(request.POST)

        if emailadmin_form.is_valid():
            # user = emailadmin_form.save(commit=False)
            # user.is_active = False
            # user.save()
            admin = Staff.objects.filter(is_admin = True).first()
            current_site = get_current_site(request)
            subject = emailadmin_form.subject
            emailBody = emailadmin_form.emailBody

            # message = render_to_string('dashboard/student/email_admin.html',
            # {
            #     'user': admin,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            user.email_user(subject, emailBody)

            return redirect('lms:student/dashboard/profile/')

        else:
            messages.error(request, "Email not sent!")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)
