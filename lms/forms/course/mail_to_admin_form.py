from django import forms
from  lms.models.course_model import StudentCourse
from ckeditor_uploader.widgets import  CKEditorUploadingWidget


def get_teachers(course_id, user_id): 
    """
    Get the teacher from course which student have enrolled
    """
    studentcourse =  StudentCourse.objects.get(courses_id = course_id, user_id = user_id)
    TEACHERS_EMAILS = [
   (studentcourse.courses.user.email,studentcourse.courses.user.username,) 

    ]

    return TEACHERS_EMAILS


class MailToAdminForm(forms.Form):

    """
    Form to send mail to admin by student
    """

    def __init__(self,*args, **kwargs):
       
        print("Kwargs", kwargs)
        pk = kwargs.pop('pk')
        user_id = kwargs.pop('user_id')
        super(MailToAdminForm,self).__init__(*args, **kwargs) 
        mails = get_teachers(course_id = pk, user_id = user_id)

        print('mails', mails)
        self.fields['staff_email'] = forms.MultipleChoiceField(
   
        widget=forms.CheckboxSelectMultiple(attrs={
            "name": "staff_email", "class": "input100"
           
        }),
        choices = mails )
    
    body = forms.CharField(widget=CKEditorUploadingWidget())
    subject = forms.CharField(widget=forms.TextInput(attrs={
            "name": "subject", "class": "input100",
            "placeholder": "Subject Of Email"
        }))
    class Meta : 
        model = StudentCourse
        fields = ['staff_email', 'body', 'subject']