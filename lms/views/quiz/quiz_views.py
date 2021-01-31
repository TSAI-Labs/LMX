# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Avg, Max, Min
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from lms.forms.quiz.create_quiz_form import CreateQuizForm
from lms.forms.quiz.create_quiz_question_form import CreateQuizQuestionForm
from lms.models.course_model import Course
from lms.models.quiz_model import Question, Responses, Quiz, StudentQuestion, UsersProfile


# Fetch Quiz Questions all at a time by Quiz Teacher View Team.
def fetch_questions(request, *args, **kwargs):
    questions = Question.objects.filter(quiz__id=kwargs['pk'])
    quizs = Quiz.objects.get(pk=kwargs['pk'])
    context = {'course_id': kwargs['course_id'],
               'object': Course.objects.get(id=kwargs['course_id']),
               'pk': kwargs['pk'],
               'questions': questions,
               'quizs': quizs
               }
    return render(request, 'quiz/fetch_questions.html', context)


# Fetch one quiz question at a time.
def fetch_questions_one_at_a_time(request, *args, **kwargs):
    obj = Question.objects.filter(quiz__id=kwargs['pk'])
    count = len(obj)
    paginator = Paginator(obj, 1)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        questions = paginator.page(page)
    except(EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)

    context = {'obj': obj,
               'questions': questions,
               'count': count,
               'quizs': Quiz.objects.get(pk=kwargs['pk']),
               'course_id': kwargs['course_id'],
               'object': Course.objects.get(id=kwargs['course_id']),
               'pk': kwargs['pk']}
    return render(request, 'quiz/fetch_questions_one_at_a_time.html', context)


class QuizCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Quiz
    context_object_name = "quiz"
    template_name = "quiz/create_quiz.html"
    success_message = "Quiz created successfully!"

    form_class = CreateQuizForm

    def get_initial(self, *args, **kwargs):
        initial = super(QuizCreateView, self).get_initial(**kwargs)
        initial['created_by'] = User.objects.get(username=self.request.user)
        initial['course'] = Course.objects.get(id=self.kwargs['course_id'])
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['created_by'] = User.objects.get(username=self.request.user)
        kwargs['course'] = Course.objects.get(id=self.kwargs['course_id'])
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        return context

    def get_success_url(self):
        return reverse('lms:quiz_home', kwargs={'course_id': self.kwargs['course_id']})

    # if user is author, then only make changes
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False


# Update the quiz
class QuizUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    context_object_name = "quiz"

    form_class = CreateQuizForm

    template_name = "quiz/create_quiz.html"

    def get_initial(self, *args, **kwargs):
        initial = super(QuizUpdateView, self).get_initial(**kwargs)
        initial['created_by'] = User.objects.get(username=self.request.user)
        initial['course'] = Course.objects.get(id=self.kwargs['course_id'])
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['created_by'] = User.objects.get(username=self.request.user)
        kwargs['course'] = Course.objects.get(id=self.kwargs['course_id'])
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        quiz = self.get_object()
        if self.request.user == quiz.created_by:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        context['course_id'] = self.kwargs['course_id']
        context['is_update_view'] = True
        return context

    def get_success_url(self):
        return reverse('lms:quiz_home', kwargs={'course_id': self.kwargs['course_id']})


# Delete the quiz
class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    template_name = "quiz/quiz_confirm_delete.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        context['quiz_object'] = Quiz.objects.get(id=self.kwargs['pk'])
        context['course_id'] = self.kwargs['course_id']
        return context

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False

    def get_success_url(self):
        return reverse('lms:quiz_home', kwargs={'course_id': self.kwargs['course_id']})


class QuizQuestionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    context_object_name = "question"
    template_name = "quiz/quiz_question_create.html"
    success_message = "Quiz question created successfully!"

    form_class = CreateQuizQuestionForm

    def get_initial(self, *args, **kwargs):
        initial = super(QuizQuestionCreateView, self).get_initial(**kwargs)
        initial['quiz'] = Quiz.objects.filter(course=self.kwargs['course_id']).get(id=self.kwargs['quiz_id'])
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizQuestionCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['quiz'] = Quiz.objects.filter(course=self.kwargs['course_id']).get(id=self.kwargs['quiz_id'])
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        return context

    def get_success_url(self):
        return reverse('lms:quiz_view', kwargs={'course_id': self.kwargs['course_id'], 'pk': self.kwargs['quiz_id']})

    # if user is author, then only make changes
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.quiz.created_by:
            return True
        return False


class QuizQuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Question
    context_object_name = "question"
    template_name = "quiz/quiz_question_create.html"
    success_message = "Quiz question updated successfully!"

    form_class = CreateQuizQuestionForm

    def get_initial(self, *args, **kwargs):
        initial = super(QuizQuestionUpdateView, self).get_initial(**kwargs)
        initial['quiz'] = Quiz.objects.filter(course=self.kwargs['course_id']).get(id=self.kwargs['quiz_id'])
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizQuestionUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['quiz'] = Quiz.objects.filter(course=self.kwargs['course_id']).get(id=self.kwargs['quiz_id'])
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        context['is_update_view'] = True
        return context

    def get_success_url(self):
        quiz = Quiz.objects.filter(course=self.kwargs['course_id']).get(id=self.kwargs['quiz_id'])
        kwargs = {'course_id': self.kwargs['course_id'],
                  # 'quiz_id': self.kwargs['quiz_id'],
                  # 'quizs': quiz,
                  'pk': self.kwargs['quiz_id']}

        if quiz.chooseview == 'One question at a time':
            return reverse('lms:fetch_questions_one_at_a_time', kwargs=kwargs)
        else:
            return reverse('lms:fetch_questions', kwargs=kwargs)

    # if user is author, then only make changes
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.quiz.created_by:
            return True
        return False


class QuizQuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = "quiz/quiz_question_confirm_delete.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        context['quiz_object'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        context['course_id'] = self.kwargs['course_id']
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.quiz.created_by:
            return True
        return False

    def get_success_url(self):
        quiz = Quiz.objects.filter(course=self.kwargs['course_id']).get(id=self.kwargs['quiz_id'])
        kwargs = {'course_id': self.kwargs['course_id'],
                  'pk': self.kwargs['quiz_id']}

        if quiz.chooseview == 'One question at a time':
            return reverse('lms:fetch_questions_one_at_a_time', kwargs=kwargs)
        else:
            return reverse('lms:fetch_questions', kwargs=kwargs)


# Quiz Starting Page.
def quiz_detail(request, *args, **kwargs):
    quizs = Quiz.objects.get(id=kwargs['pk'])
    context = {'quizs': quizs,
               'course_id': kwargs['course_id'],
               'object': Course.objects.get(id=kwargs['course_id']),
               'pk': kwargs['pk']}
    return render(request, 'quiz/quiz_detail.html', context)


# Preview Quiz
def preview_quiz(request, *args, **kwargs):
    questions = Question.objects.filter(quiz__id=kwargs['pk'])
    context = {'questions': questions,
               'course_id': kwargs['course_id'],
               'quiz': Quiz.objects.get(id=kwargs['pk']),
               'object': Course.objects.get(id=kwargs['course_id'])}
    return render(request, 'quiz/quiz_preview.html', context)


# Quiz Landing Page
def quiz_home(request, *args, **kwargs):
    quizs = Quiz.objects.filter(course__id=kwargs['course_id'])
    context = {'quizs': quizs, 'course_id': kwargs['course_id'], 'object': Course.objects.get(id=kwargs['course_id'])}
    return render(request, 'quiz/quiz_home.html', context)


# Compute Stats of Quiz
def compute_stats(request, *args, **kwargs):
    profiles = UsersProfile.objects.all()
    context = {'course_id': kwargs['course_id'], 'object': Course.objects.get(id=kwargs['course_id'])}
    context.update({'profiles': profiles})
    context.update(UsersProfile.objects.all().aggregate(Avg('marks')))
    context.update(UsersProfile.objects.all().aggregate(Min('marks')))
    context.update(UsersProfile.objects.all().aggregate(Max('marks')))
    return render(request, 'quiz/compute_stats.html', context)


# Enter Comments.
def enter_quiz_comment(request, *args, **kwargs):
    responses = Responses.objects.all()
    context = {'responses': responses, 'course_id': kwargs['course_id'],
               'object': Course.objects.get(id=kwargs['course_id'])}
    if request.method == "POST":
        responses = Responses()
        responses.comments = request.POST['comments']
        responses.save()

    return render(request, 'quiz/quiz_comment.html', context)


# Quiz Publish
def quiz_publish(request, *args, **kwargs):
    context = {'course_id': kwargs['course_id']}
    questions = Question.objects.filter(quiz__id=kwargs['pk'])
    for quest in questions:

        try:
            obj = StudentQuestion.objects.filter(quiz=quest.quiz).get(question=quest.question)
            setattr(obj, 'questiontype', quest.questiontype)
            setattr(obj, 'description', quest.description)
            setattr(obj, 'answer', quest.answer)
            setattr(obj, 'option1', quest.option1)
            setattr(obj, 'option2', quest.option2)
            setattr(obj, 'option3', quest.option3)
            setattr(obj, 'option4', quest.option4)
            setattr(obj, 'points', quest.points)
            setattr(obj, 'img', quest.img)
            setattr(obj, 'files', quest.files)
            obj.save()
        except StudentQuestion.DoesNotExist:
            obj = StudentQuestion(quiz=quest.quiz,
                                  questiontype=quest.questiontype,
                                  question=quest.question,
                                  description=quest.description,
                                  answer=quest.answer,
                                  option1=quest.option1,
                                  option2=quest.option2,
                                  option3=quest.option3,
                                  option4=quest.option4,
                                  points=quest.points,
                                  img=quest.img,
                                  files=quest.files
                                  )
            obj.save()

    messages.success(request, 'Quiz successfully published!')
    return redirect('lms:quiz_home', course_id=kwargs['course_id'])
