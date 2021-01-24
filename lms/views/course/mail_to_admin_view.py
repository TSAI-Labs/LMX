
# Core Django imports.
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages


#EMail imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# LMS app imports
from lms.forms.course.mail_to_admin_form import MailToAdminForm

#Models
from lms.models.course_model import Course
from lms.models.user_role_model import Role


class MailToAdminView(LoginRequiredMixin, View):
    """
    Send Mail to admin/teacher. 
    Ps : Since the mail is sent by centralised email, teacher will not know who sent the mail. 
    So in the body Added the username and course he is enrolled at the beginning
    """
   
    template_name = 'lms/course/mail_to_admin.html'

    home_template = 'dashboard/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        role = Role.objects.filter(user=request.user)
        if role and role[0].is_student:

            pk = self.kwargs['pk']
            
            self.context_object = {"mail_to_admin_form": MailToAdminForm(pk = pk, user_id = request.user.id), "pk" : pk}

            return render(request, self.template_name, self.context_object)
        else:
            messages.error(request, "Only Student can view this!!")
            return redirect('lms:logout')

    def post(self, request, *args, **kwargs):
        #course id
        pk = self.kwargs['pk']
        #course name
        course_name = Course.objects.get(id = pk).title
        #get email
        email_form = MailToAdminForm(data=request.POST, pk = pk, user_id = request.user.id)
        if email_form.is_valid():
            #take the email body and attach username and to it, so that teacher know who sent the email
            html_message = email_form.cleaned_data['body']
            print(html_message)
            html_message ="<h3>Username : "+request.user.username+ "<br/> Course : "+course_name+"</h3><br/><br/> " + html_message

            subject = email_form.cleaned_data['subject']
            plain_message = strip_tags(html_message)
            res = send_mail(subject=subject, message=plain_message, from_email = request.user.email,recipient_list= email_form.cleaned_data['staff_email'],html_message=html_message )
            return render(request,self.home_template)
