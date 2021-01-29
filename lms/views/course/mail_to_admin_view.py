# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# EMail imports
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from django.views.generic import View

# LMS app imports
from lms.forms.course.mail_to_admin_form import MailToAdminForm
# Models
from lms.models.course_model import Course, StudentCourse
from lms.models.user_role_model import Role


class MailToAdminView(LoginRequiredMixin, View):
    """
    Send Mail to admin/teacher.
    Ps : Since the mail is sent by centralised email, teacher will not know who sent the mail.
    So in the body Added the username and course he is enrolled at the beginning
    """

    template_name = 'lms/course/mail_to_admin.html'

    def get(self, request, *args, **kwargs):
        role = Role.objects.filter(user=request.user)
        if role and role[0].is_student:
            pk = self.kwargs['pk']
            self.context_object = {"mail_to_admin_form": MailToAdminForm(pk=pk, user_id=request.user.id), "pk": pk,
                                   "object": Course.objects.get(id=int(pk))}

            self.context_object['object1'] = StudentCourse.objects.filter(courses=self.context_object['object'].id).get(user = self.request.user)

            return render(request, self.template_name, self.context_object)
        else:
            messages.error(request, "Only Student can view this!!")
            return redirect('lms:logout')

    def post(self, request, *args, **kwargs):
        # course id
        pk = self.kwargs['pk']
        # course name
        course_name = Course.objects.get(id=pk).title
        # get email
        email_form = MailToAdminForm(data=request.POST, pk=pk, user_id=request.user.id)
        if email_form.is_valid():
            # take the email body and attach username and to it, so that teacher know who sent the email
            html_message = email_form.cleaned_data['body']
            print(html_message)
            html_message = "<h3>Username : " + request.user.username + "<br/> Course : " + course_name + "</h3><br/><br/> " + html_message

            subject = email_form.cleaned_data['subject']
            plain_message = strip_tags(html_message)
            try:
                res = send_mail(subject=subject, message=plain_message, from_email=request.user.email,
                                recipient_list=email_form.cleaned_data['staff_email'], html_message=html_message)
                messages.success(request, 'Mail sent successfully')
            except Exception as e:
                messages.error(request, 'Mail sent failed')
            return redirect('lms:mail_to_admin', pk=pk)
