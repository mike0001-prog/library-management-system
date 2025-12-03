from django import forms
from . models import UserProfile,Department
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
class user_profile_form(forms.ModelForm):
    # passport = forms.ImageField(label="passport", widget=forms.FileInput(attrs={"class":"form-control"}))
    # department = forms.ModelChoiceField(queryset=Department.objects.all(),label="Department")
    
    # d_o_b = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control"}))
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = UserProfile
        fields = [ "passport","department", "gender", "d_o_b", "level"]

class CustomPasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class CustomSetPassword(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"