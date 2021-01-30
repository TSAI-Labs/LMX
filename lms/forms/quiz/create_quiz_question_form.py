from django import forms
from django.forms import ModelForm

from lms.models.quiz_model import Question


class CreateQuizQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

        widgets = {
            'quiz': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop('quiz')
        super(CreateQuizQuestionForm, self).__init__(*args, **kwargs)
