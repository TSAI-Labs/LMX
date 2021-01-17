from collections import namedtuple

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView

from lms.forms.course.grading_scheme_forms import GradeFormSet, GradingSchemeNameForm, GradingSchemeNamesListForm
from lms.models.course_model import GradingScheme, GradingSchemeName, Course
from lms.models.users_model import Staff


def validate_post(request):
    if request.method == 'POST':

        # Update an existing Grading Scheme
        if 'scheme_name_id' in request.POST:
            instance = GradingSchemeName.objects.get(id=request.POST['scheme_name_id'])
            grading_scheme_name_form = GradingSchemeNameForm(request.POST, instance=instance)
            grades_formset = GradeFormSet(request.POST, instance=instance)

        # Create a new Grading Scheme
        else:
            grading_scheme_name_form = GradingSchemeNameForm(request.POST)
            grades_formset = GradeFormSet(request.POST)

        if not grading_scheme_name_form.is_valid() or not grades_formset.is_valid():
            messages.error(request, 'Update Error! Form data is invalid!')
            return 'fail'

        # Check integrity of scores (if any)
        Range = namedtuple('Range', ['begin', 'end'])
        range_values = sorted(
            [Range(x['score_range_begin'], x['score_range_end']) for x in grades_formset.cleaned_data
             if x and not x['DELETE']]
        )

        if range_values:
            current_range = range_values[0]
            for x in range_values[1:]:
                if current_range.end != x.begin:
                    if current_range.end < x.begin:
                        messages.error(request,
                                       f'Update Error! Missing grades for scores in between {current_range.end} and {x.begin}')
                    elif current_range.end > x.begin:
                        messages.error(request,
                                       f'Update Error! Grades overlap for scores in between {x.begin} and {current_range.end}')
                    return 'fail'
                else:
                    current_range = x

        # Saving the form data into the database
        scheme_name = grading_scheme_name_form.save()
        for form_data in grades_formset.cleaned_data:

            if form_data:
                form_data['scheme_name'] = scheme_name
                _id = form_data['id']
                _delete = form_data['DELETE']
                del form_data['id']
                del form_data['DELETE']

                if _id and GradingScheme.objects.filter(id=_id.id):
                    if _delete:
                        instance = GradingScheme.objects.get(id=_id.id)
                        instance.delete()
                    else:
                        GradingScheme.objects.filter(id=_id.id).update(**form_data)
                else:
                    if not _delete:
                        obj = GradingScheme.objects.create(**form_data)
                        obj.save()
        return 'success'


class GradingSchemeCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Class View to create a new grading scheme
    """

    # The model and the fields below will not be used in the view.
    # They are present here to fetch the correct primary key for building the urls for this view
    model = Course
    fields = ['title']

    template_name = "lms/course/settings/course_grading_scheme_create.html"

    def get_context_data(self, **kwargs):
        context = super(GradingSchemeCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['grade_formset'] = GradeFormSet(self.request.POST)
            context['scheme_name'] = GradingSchemeNameForm()
        else:
            context['grade_formset'] = GradeFormSet()
            context['scheme_name'] = GradingSchemeNameForm()
        return context

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_grading_scheme_create', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        status = validate_post(request)
        if status == 'success':
            messages.success(request, 'Grading Scheme is successfully created!')
        return render(request, self.template_name, context=self.get_context_data())

    # Restrict access to only staff members
    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1


class GradingSchemeUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Class View to create a new grading scheme
    """

    # The model and the fields below will not be used in the view.
    # They are present here to fetch the correct primary key for building the urls for this view
    model = Course
    fields = ['title']

    template_name = "lms/course/settings/course_grading_scheme_update.html"

    def get_context_data(self, **kwargs):
        context = super(GradingSchemeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST and 'scheme_name_id' in kwargs:
            scheme_name_id = kwargs['scheme_name_id']
            instance = GradingSchemeName.objects.get(id=scheme_name_id)
            context['scheme_name'] = GradingSchemeNameForm(instance=instance)
            context['grade_formset'] = GradeFormSet(instance=instance)
            context['existing_grading_schemes'] = GradingSchemeNamesListForm({'scheme_names_list': scheme_name_id})
            context['scheme_name_id'] = scheme_name_id
            context['show_details'] = True
        else:
            context['existing_grading_schemes'] = GradingSchemeNamesListForm()
            context['show_details'] = False

        return context

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_grading_scheme_update', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        # Handle the post data from - GradingSchemeNamesListForm
        if request.POST.get('scheme_names_list'):
            scheme_name_id = request.POST['scheme_names_list']
            return render(request, self.template_name,
                          context=self.get_context_data(scheme_name_id=scheme_name_id))

        # Handle the post data for deleting the selected formset, and redirect user to home page for update
        elif request.POST.get('delete_record'):
            instance = GradingSchemeName.objects.get(id=int(request.POST.get('scheme_name_id')))
            instance.delete()
            messages.success(request, 'Grading Scheme successfully deleted!')
            return render(request, self.template_name, context=self.get_context_data())

        # Handle the post data for updating the selected formset, and redirect user to home page for update
        else:
            status = validate_post(request)
            if status == 'success':
                messages.success(request, 'Grading Scheme is successfully updated!')
            return render(request, self.template_name, context=self.get_context_data())

    # Restrict access to only staff members
    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1
