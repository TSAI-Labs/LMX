# Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic import View

from lms.forms.account.register_form import UserUpdateForm
from lms.forms.course.course_section_forms import CourseSubscribeForm
from lms.forms.dashboard.profile_form import ProfileUpdateForm
from lms.models.assignment_model import Assignment, StudentAssignment
from lms.models.course_model import Course, StudentCourse
from lms.models.quiz_model import Quiz
from lms.models.user_role_model import Role


class DashboardHomeView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'dashboard/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            role = Role.objects.filter(user=request.user)
            if role:
                if role[0].is_student:
                    assignments = StudentAssignment.objects.filter(user=request.user)
                    courses = StudentCourse.objects.filter(user=request.user)
                    all_courses = Course.objects.filter(published=True)
                    self.context.update(registered_courses=list(filter(lambda x: x.registered, courses)))
                    self.context.update(unregistered_courses=[x for x in all_courses
                                                              if not x in [y.courses
                                                                           for y in courses
                                                                           if y.registered
                                                                           ]])
                    self.context.update(
                        assignments=list(filter(lambda x: x.assignment.available_until > now(), assignments)))
                    self.context.update(is_profile_view=False)
                else:
                    assignments = Assignment.objects.filter(created_by=request.user)
                    quizzes = Quiz.objects.filter(created_by=request.user)
                    courses = Course.objects.filter(user=request.user)
                    self.context.update(published_courses=list(filter(lambda x: x.published, courses)))
                    self.context.update(assignments=list(filter(lambda x: x.available_until > now(), assignments)))
                    self.context.update(unpublished_courses=list(filter(lambda x: not x.published, courses)))
                    self.context.update(quizzes=list(filter(lambda x: x.Until > now(), quizzes)))
                    self.context.update(is_profile_view=False)

                self.context.update(is_student_view=role[0].is_student)
            else:
                messages.error(request, "Contact Admin for Role Creation")
                return redirect('lms:logout')

            return render(request, self.template_name, self.context)
        else:
            return redirect('lms:login')


class DashboardProfileView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """

    def get(self, request, *args, **kwargs):

        role = Role.objects.filter(user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        user_role = []
        if role:
            if role[0].is_admin:
                user_role.append('Admin')
            if role[0].is_teacher:
                user_role.append('Teacher')
            if role[0].is_teaching_assistant:
                user_role.append('Teaching Assistant')
            if role[0].is_student:
                user_role.append('Student')

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'role': ' | '.join(user_role),
            'is_profile_view': True
        }

        template_name = 'dashboard/profile.html'

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('lms:dashboard_profile')
        else:
            messages.error(request, f'Check Profile Updated Data')

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'is_profile_view': True
        }

        template_name = 'dashboard/profile.html'

        return render(request, template_name, context)


def dashboard_subscribe(request, **kwargs):
    form = CourseSubscribeForm()
    course_id = kwargs['pk']
    course_name = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseSubscribeForm(request.POST)
        # print('form fetched', request.POST, request.POST.get('course'), request.POST.get('email'))
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'dashboard/landing/subscribe.html',
                  {'form': form, 'course_name': course_name, 'course_id': course_id})


def dashboard_list(request):
    search_post = request.GET.get('search')
    if search_post:
        course = Course.objects.filter(published=True).filter(Q(title__icontains=search_post))
    else:
        course = Course.objects.filter(published=True)
    paginator = Paginator(course, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if not request.user.is_authenticated:
        return render(request, 'dashboard/landing/home.html', {'course_list': page_obj})
    else:
        return redirect('lms:dashboard_home')


def dashboard_details(request, **kwargs):
    # course_number = request.GET.get('search')
    data = Course.objects.filter(id=kwargs['pk'])
    responseData = []
    for eachEntry in data:
        responseData.append(eachEntry)
    return render(request, 'dashboard/landing/coursedetails.html', {'course_list': data})
