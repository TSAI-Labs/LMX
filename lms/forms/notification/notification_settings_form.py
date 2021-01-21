from django import forms

# LMS application imports.
from lms.models.notification_settings_model import NotificationSetting


class NotificationSettingUpdateForm(forms.ModelForm):
    class Meta:
        model = NotificationSetting
        fields = ['due_date', 'grading_policies', 'course_content', 'files', 'announcement']
