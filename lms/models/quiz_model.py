# Core Django imports.
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from image_optimizer.fields import OptimizedImageField

from lms.models.course_model import Course
from lms.models.user_role_model import Role

choiceq = (('All question at a time', 'All at once'),
           ('One question at a time', 'One at once')
           )


class Quiz(models.Model):
    """
    Create a quiz
    """
    Quizname = models.CharField(max_length=250, null=False, blank=False)
    Quiztype = models.CharField(max_length=100, default="Graded Quiz")
    chooseview = models.CharField(max_length=100, choices=choiceq, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Availablefrom = models.DateTimeField(blank=True)
    Until = models.DateTimeField(blank=True)
    points = models.IntegerField(blank=True)
    Questions = models.IntegerField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.Quizname}'

    def clean(self):
        role = Role.objects.filter(user=self.created_by)
        if role:
            if not (role[0].is_admin or role[0].is_teacher):
                raise ValidationError("Only Teacher Or Admin Can Create Quizzes")
            if not self.course.user == self.created_by:
                raise ValidationError("Teacher of this course only can create a quiz")
        else:
            raise ValidationError("Assign Role to the User")

    class Meta:
        unique_together = ('Quizname', 'course',)


choice = (('Multiple choice', 'MCQ'),
          ('Multiple correct', 'MCC'),
          ('True or False', 'T/F')
          )


class Question(models.Model):
    """
    Create a questions for quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True)
    questiontype = models.CharField(max_length=100, choices=choice, default='Multiple choice')
    question = models.TextField(max_length=1000, blank=False)
    description = RichTextField(blank=True, null=True)
    answer = models.IntegerField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    points = models.IntegerField(default=5, blank=True)

    img = OptimizedImageField(
        upload_to='pics',
        optimized_image_output_size=(500, 300),
        optimized_image_resize_method='cover', blank=True
    )
    files = models.FileField(upload_to='Quiz/uploads', blank=True, max_length=254)

    def __str__(self):
        return self.question

    class Meta:
        unique_together = ('quiz', 'question',)


class Responses(models.Model):
    """
    To store the comments store by students.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    Questionid = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField(blank=True)
    comments = models.TextField(max_length=1000, blank=True)


class StudentQuestion(models.Model):
    """
    Move the final quiz from teacher to student view.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True)
    questiontype = models.CharField(max_length=100, choices=choice, default='Multiple choice')
    question = models.TextField(max_length=1000, blank=False)
    description = RichTextField(blank=True, null=True)
    answer = models.IntegerField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    points = models.IntegerField(default=5, blank=True)

    img = OptimizedImageField(
        upload_to='pics',
        optimized_image_output_size=(500, 300),
        optimized_image_resize_method='cover', blank=True
    )
    files = models.FileField(upload_to='Quiz/uploads', blank=True, max_length=254)

    def __str__(self):
        return self.question

    class Meta:
        unique_together = ('quiz', 'question',)


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.IntegerField(default=10)
    number_of_attempts = models.IntegerField(default=2)
    Attempts_left = models.IntegerField(default=1)

    # Time_taken = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.user.username}'s Profile"
