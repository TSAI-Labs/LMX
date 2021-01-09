from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

limit_max_marks = 30_000.0
limit_min_marks = -10_000.0


class DummyStudent(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(
        primary_key=True, default='test@example.com', max_length=254, unique=True)

    def __str__(self):
        return f'{self.name}'


class DummyAssignment(models.Model):

    title = models.CharField(max_length=50)
    student = models.ForeignKey(DummyStudent, on_delete=models.CASCADE)
    max_mark = models.FloatField(default=0, validators=[MaxValueValidator(
        limit_max_marks), MinValueValidator(limit_min_marks)])
    alloted_mark = models.FloatField(default=0, validators=[MaxValueValidator(
        limit_max_marks), MinValueValidator(limit_min_marks)])
    grade = models.CharField(default='F', max_length=1)

    def __str__(self):
        return f'{self.student}, {self.title} got a {self.grade} with {self.alloted_mark}/{self.max_mark}'
