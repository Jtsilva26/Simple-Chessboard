from django import forms
from django.core import validators
from django.contrib.auth.models import User

valid_alpha = {'a','b','c','d','e','f','h'}

# def validate_location(value):
#  if (value[0] != "r") or (not value[1].isdigit()) or \
#  (value[2] != "c") or (not value[3].isdigit()):
#      raise forms.ValidationError("Use row and column format, e.g. r1c1.")
# def validate_value(value):
#  try:
#      int(value)
#  except ValueError:
#      raise forms.ValidationError("Enter an integer from 1 to 9.")
#  if (int(value) < 1 or int(value) > 9):
#      raise forms.ValidationError("Enter an integer from 1 to 9.")

def validate_any(value):
    if(not value[0].isalpha()) or (not value[1].isdigit()) or (int(value[1]) > 8) or \
    (int(value[1]) < 1) or (not value[0].islower()):
        raise forms.ValidationError("Use labels: a-h along with 1-8")
    elif value[0] not in valid_alpha:
        raise forms.ValidationError("Use labels: a-h along with 1-8")

class ChessForm(forms.Form):
    start = forms.CharField(min_length=2, max_length=2, strip=True, widget = forms.TextInput(attrs={'placeholder':'a2','style':'font-size:small'}),
         validators = [validators.MinLengthValidator(2), validators.MaxLengthValidator(2), validate_any])
    end = forms.CharField(min_length=2, max_length=2, strip=True, widget = forms.TextInput(attrs={'placeholder':'a3','style':'font-size:small'}),
         validators = [validators.MinLengthValidator(2), validators.MaxLengthValidator(2), validate_any])

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'newpassword'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': None
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
