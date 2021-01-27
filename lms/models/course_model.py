# Core Django imports.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from lms.models.user_role_model import Role

from image_optimizer.fields import OptimizedImageField
from ckeditor.fields import RichTextField


class GradingSchemeName(models.Model):
    """
    Model to capture various grading schemes.
    Courses will be able to choose from these grading schemes
    """
    name = models.CharField(max_length=250, null=False, blank=False, unique=True)

    def __str__(self):
        return f'Grading Scheme {self.name}'


class GradingScheme(models.Model):
    """
    Model to capture various grading schemes.
    Courses will be able to choose from these grading schemes
    """
    scheme_name = models.ForeignKey(to=GradingSchemeName, on_delete=models.CASCADE)
    grade = models.CharField(max_length=250, null=False, blank=False)
    score_range_begin = models.SmallIntegerField()
    score_range_end = models.SmallIntegerField()

    def __str__(self):
        return f'{self.scheme_name}, Grade: {self.grade}, Scores: [{self.score_range_begin}, {self.score_range_end})'

    def clean(self):
        super(GradingScheme, self).clean()

        if self.score_range_end and self.score_range_begin:
            if self.score_range_end < self.score_range_begin:
                raise ValidationError('Range Error: Score end value is less that the score begin value!')

    # # Constraints to ensure that a duplicate entry is not present with scheme name and grade
    # class Meta:
    #     unique_together = ('scheme_name', 'grade',)


class Course(models.Model):
    """
    Model to capture all the course details
    """
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)
    # TODO change field type
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(null=True)
    published = models.BooleanField(default=False)

    thumbnail = models.ImageField(default='default.png', upload_to='course_thumbnails', null=True, blank=True)
    # time_zone=models.CharField(max_length=35, choices=[(x, x) for x in pytz.common_timezones], default='Asia/Kolkata')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    grading_scheme = models.ForeignKey(to=GradingSchemeName, on_delete=models.SET_NULL, null=True, blank=True)
    allow_self_enroll = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def clean(self):
        role = Role.objects.filter(user=self.user)
        if role:
            if not (role[0].is_admin or role[0].is_teacher):
                raise ValidationError("Only Teacher Or Admin Can Create Courses")
        else:
            raise ValidationError("Assign Role to the User")

        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be greater than the end date')


class Section(models.Model):
    """
    Students belonging to each course can be further sub-divided into sections
    """
    section_name = models.CharField(max_length=250, null=True, blank=False, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'Section {self.section_name} - {self.course}'

    # Constraints to ensure that a duplicate entry is not present with section_name and course
    class Meta:
        unique_together = ('section_name', 'course',)


class Group(models.Model):
    """
    Students belonging to each course can be further sub-divided into groups by themselves:
    Only difference between groups and sections is Section is teacher created, groups is student created
    """
    group_name = models.CharField(max_length=250, null=True, blank=False, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f'Group {self.group_name} - {self.course}'

    # Constraints to ensure that a duplicate entry is not present with group_name and course
    class Meta:
        unique_together = ('group_name', 'course',)


class StudentCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentcourses')
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    registered = models.BooleanField(default=False)

    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} is associated with {self.courses.title}'

    def clean(self):
        role = Role.objects.filter(user=self.user)
        if role:
            if role[0].is_admin or role[0].is_teacher or role[0].is_teaching_assistant:
                raise ValidationError("Only Student can register to the courses")
        else:
            raise ValidationError("Assign Role to the User")

        if not self.courses.published:
            raise ValidationError("Only Published courses can be selected")

    # Constraints to ensure that a student cannot enroll into the same course more than once
    class Meta:
        unique_together = ('user', 'courses',)


choiceq=(('All question at a time','All at once'),
         ('One question at a time','One at once')   
            )

class Quiz(models.Model):
    """
    Create a quiz
    """
    Quizname = models.CharField(max_length=250, null=False, blank=False, unique=True)
    Quiztype = models.CharField(max_length=100,default="Graded Quiz")
    chooseview = models.CharField(max_length=100,choices=choiceq,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    Availablefrom = models.DateTimeField(blank=True)
    Until = models.DateTimeField(blank=True)
    points = models.IntegerField(blank=True)
    Questions = models.IntegerField(blank=True)

    def __str__(self):
        return self.Quizname


choice=(('Multiple choice','MCQ'),
        ('Multiple correct','MCC'),
        ('True or False','T/F')
        )

class Question(models.Model):
    """
    Create a questions for quiz.
    """
    course= models.ForeignKey(Course,on_delete=models.CASCADE)
    quiznumber = models.ForeignKey(Quiz,on_delete=models.CASCADE,blank=True)
    questiontype = models.CharField(max_length=100,choices=choice,default='Multiple choice')
    question = models.TextField(max_length=1000,blank=False)
    description = RichTextField(blank=True,null=True)
    answer =  models.IntegerField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length = 100 , blank = True )
    option4 = models.CharField(max_length = 100 , blank = True )
    points = models.IntegerField(default=5,blank=True) 
    
    img = OptimizedImageField(
        upload_to='pics',
        optimized_image_output_size=(500, 300),
        optimized_image_resize_method='cover',blank=True  
    )
    files = models.FileField(upload_to='Quiz/uploads', blank=True,max_length=254)

    def __str__(self):
        return self.question


class Responses(models.Model):
    """
    To store the comments store by students.
    """
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    Questionid=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.IntegerField(blank=True)
    comments=models.TextField(max_length=1000,blank=True)


class Student_Question(models.Model):
    """
    Move the final quiz from teacher to student view.
    """
    course= models.ForeignKey(Course,on_delete=models.CASCADE)
    quiznumber = models.ForeignKey(Quiz,on_delete=models.CASCADE,blank=True)
    questiontype = models.CharField(max_length=100,choices=choice,default='Multiple choice')
    question = models.TextField(max_length=1000,blank=False)
    description = RichTextField(blank=True,null=True)
    answer =  models.IntegerField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length = 100 , blank = True )
    option4 = models.CharField(max_length = 100 , blank = True )
    points = models.IntegerField(default=5,blank=True) 
    
    img = OptimizedImageField(
        upload_to='pics',
        optimized_image_output_size=(500, 300),
        optimized_image_resize_method='cover',blank=True  
    )
    files = models.FileField(upload_to='Quiz/uploads', blank=True,max_length=254)

    def __str__(self):
        return self.question


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.IntegerField(default=10)
    number_of_attempts = models.IntegerField(default=2)
    Attempts_left = models.IntegerField(default=1)
    #Time_taken = models.IntegerField(default=30)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"