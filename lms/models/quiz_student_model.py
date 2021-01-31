from django.db import models

class session(models.Model):
    sessionid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class QuizDetails(models.Model):
    sessionid = models.ForeignKey(session,on_delete=models.CASCADE,db_column='sessionid',to_field='sessionid',default=None)
    quizid = models.CharField(max_length=100,unique=True,default=None)

    
class studentdetails(models.Model):
    studentid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100)

class studentquizdetails(models.Model):
    quizid = models.ForeignKey(QuizDetails,on_delete=models.CASCADE,db_column='quizid',to_field='quizid',default=None)
    studentid = models.ForeignKey(studentdetails,on_delete=models.CASCADE,db_column='studentid',to_field='studentid',default=None)
    quiz_status = models.BooleanField(null=True)
    quiz_answers = models.JSONField()

class Quiz_Questions(models.Model):
    quizid = models.ForeignKey(QuizDetails,on_delete=models.CASCADE,db_column='quizid',to_field='quizid',default=None)
    quiz_question_answers = models.JSONField()
    # question = models.TextField()
    # option1 = models.CharField(max_length=100)
    # option2 = models.CharField(max_length=100)
    # option3 = models.CharField(max_length=100)
    # option4 = models.CharField(max_length=100)
    # answer = models.CharField(max_length=100)


# from django.conf import settings
# from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.template.defaultfilters import slugify


# class Quiz(models.Model):
# 	name = models.CharField(max_length=100)
# 	description = models.CharField(max_length=70)
# 	image = models.ImageField()
# 	slug = models.SlugField(blank=True)
# 	roll_out = models.BooleanField(default=False)
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	class Meta:
# 		ordering = ['timestamp',]
# 		verbose_name_plural = "Quizzes"

# 	def __str__(self):
# 		return self.name


# class Question(models.Model):
# 	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
# 	label = models.CharField(max_length=100)
# 	order = models.IntegerField(default=0)

# 	def __str__(self):
# 		return self.label


# class Answer(models.Model):
# 	question = models.ForeignKey(Question, on_delete=models.CASCADE)
# 	label = models.CharField(max_length=100)
# 	is_correct = models.BooleanField(default=False)

# 	def __str__(self):
# 		return self.label


# class QuizTaker(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# 	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
# 	score = models.IntegerField(default=0)
# 	completed = models.BooleanField(default=False)
# 	date_finished = models.DateTimeField(null=True)
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.user.email


# class UsersAnswer(models.Model):
# 	quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
# 	question = models.ForeignKey(Question, on_delete=models.CASCADE)
# 	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

# 	def __str__(self):
# 		return self.question.label


# @receiver(pre_save, sender=Quiz)
# def slugify_name(sender, instance, *args, **kwargs):
# 	instance.slug = slugify(instance.name)



