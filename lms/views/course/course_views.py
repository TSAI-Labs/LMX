# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from lms.models.assignment_model import StudentAssignment
from lms.models.course_model import Course
from lms.tables import StudentAssignmentTable, StudentAssignmentFilter

from lms.models.course_model import Question, Responses, Quiz, Student_Question, UsersProfile
from django.db.models import Avg, Max, Min
from django.core.paginator import Paginator


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "lms/course/home.html"


class GradeBookCourseView(LoginRequiredMixin, UserPassesTestMixin, ExportMixin, SingleTableMixin, FilterView):
    model = StudentAssignment
    table_class = StudentAssignmentTable

    template_name = 'lms/course/gradebook/course_gradebook.html'
    filterset_class = StudentAssignmentFilter

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user.role.is_teacher:
            return True
        elif self.request.user.role.is_teaching_assistant:
            return True
        return False

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


# download csv file (django_tables2 method)
def table_download(request):
    table = StudentAssignmentTable(StudentAssignment.objects.all())

    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, "lms/course/gradebook/course_gradebook_export.html", {
        "table": table
    })


# Fetch Quiz Questions all at a time by Quiz Teacher View Team.
def fetch_questions(request):
    questions = Question.objects.all()
    quizs = Quiz.objects.first()
    context = dict()
    context.update({'questions':questions})
    context.update({'quizs':quizs})
    return render(request,'lms/course/quiz3.html',context)


# Fetch one quiz question at a time.
def fetch_questions_oneatatime(request):
    obj = Question.objects.all()

    count = Question.objects.all().count()
    paginator = Paginator(obj,1)
    try:
        page = int(request.GET.get('page','1'))  
    except:
        page =1
    try:
        questions = paginator.page(page)
    except(EmptyPage,InvalidPage):

        questions=paginator.page(paginator.num_pages)
    
    return render(request,'lms/course/quiz.html',{'obj':obj,'questions':questions,'count':count})    


# Quiz Starting Page.
def display_lp(request):
    quizs = Quiz.objects.first()
    context = {'quizs':quizs}
    return render(request,'lms/quiz2.html',context)


# Edit Quiz Questions only admin has the right to to do.
def Edit_quiz(request):
    return render(request,'admin/')  


# Preview Quiz
def preview_quiz(request):
    questions = Question.objects.all()
    context = {'questions':questions}
    return render(request,'lms/course/quiz_preview.html',context)


# Quiz Landing Page
def quiz_lp(request):
    quizs=Quiz.objects.all()
    context = {'quizs':quizs}
    return render(request,'lms/course/quizlp.html',context)


# Compute Stats of Quiz
def compute_stats(request):
    profiles= UsersProfile.objects.all()
    context= dict()
    context.update({'profiles':profiles})
    context.update(UsersProfile.objects.all().aggregate(Avg('marks')))
    context.update(UsersProfile.objects.all().aggregate(Min('marks')))
    context.update(UsersProfile.objects.all().aggregate(Max('marks')))
    return render(request,'lms/course/compute_stats.html',context)


# Enter Comments.
def enter_comment(request):
    responses = Responses.objects.all()
    context = {'responses':responses}
    if request.method == "POST":
       responses = Responses()
       responses.comments = request.POST['comments']
       responses.save()
       return render(request,'lms/course/responses.html')
    else:
        return render(request,'lms/course/responses.html',context)



# Quiz Publish
def quiz_publish(request):
    questions = Question.objects.all()
    for i in questions:
        model_one = Student_Question(course= i.course,
                                     quiznumber = i.quiznumber,
                                     questiontype= i.questiontype,
                                     questionnumber = i.questionnumber,
                                     question= i.question,
                                     description= i.description,
                                     answer= i.answer,
                                     option1= i.option1,
                                     option2= i.option2,
                                     option3= i.option3,
                                     option4= i.option4,
                                     points = i.points,
                                     img= i.img,
                                     files= i.files 
                                     )
        model_one.save()
    return render(request,'lms/quiz_student_view.html')
