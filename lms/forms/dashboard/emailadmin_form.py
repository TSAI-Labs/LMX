from django import forms

# LMS app imports.
from lms.models.email_model import Email


class EmailAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # self.fields['toname'].widget.attrs.pop("autofocus", None)

        subject = forms.CharField(label = 'Subject', required = True)
        emailBody = forms.CharField(label = 'Email Body', required = True)

    class Meta:
        model = Email
        fields = ['subject', 'emailBody']