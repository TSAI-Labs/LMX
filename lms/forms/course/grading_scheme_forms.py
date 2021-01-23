from django import forms
from django.forms import ModelForm, inlineformset_factory

from lms.models.course_model import GradingScheme, GradingSchemeName


class GradingSchemeNameForm(ModelForm):
    class Meta:
        model = GradingSchemeName
        fields = ['name']


class GradingSchemeNamesListForm(forms.Form):
    scheme_names_list = forms.ModelChoiceField(queryset=GradingSchemeName.objects.all())


GradeFormSet = inlineformset_factory(
    parent_model=GradingSchemeName, model=GradingScheme,
    fields=['scheme_name', 'grade', 'score_range_begin', 'score_range_end'],
    extra=10, max_num=10, can_delete=True
)
