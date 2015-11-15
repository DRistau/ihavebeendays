from django import forms
from ihavebeendays.tasks.models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'Cover-titleInputAction',
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


class TaskResetForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'Cover-titleInputAction',
        'placeholder': 'What motivated you to reset this task?',
    }))

    class Meta:
        model = Task
        fields = ['description']
