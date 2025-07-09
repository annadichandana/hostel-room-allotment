from django import forms
from .models import student
class studentform(forms.ModelForm):
    class Meta:
        model=student
        fields='__all__'

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Registered Email")
    hallticketno=forms.CharField(label="Hallticket No")
