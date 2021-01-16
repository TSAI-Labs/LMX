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

# Usage example
# ArticleFormSet(request.POST, initial=[...])

# How to let dynamic entries appear on the screen for the formset?
# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/#understanding-the-managementform

# How to validate the form set data
# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/#custom-formset-validation

# How to order form sets?
# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/#dealing-with-ordering-and-deletion-of-forms
