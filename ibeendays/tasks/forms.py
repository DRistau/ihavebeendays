from django import forms
from ibeendays.tasks.models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'cover-title-input-action',
            'placeholder': 'Working out',
            'required': 'true',
        })
    )

    class Meta:
        model = Task
        fields = ['title']

    def save(self, user):
        self.instance.user = user
        return super(TaskForm, self).save()
