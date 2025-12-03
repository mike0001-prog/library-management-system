from .models import Question
from django import forms

class AddQuestionForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs["class"] = "form-control"
    class Meta:
         model = Question
         fields = ["question","option_one","option_two","option_three","option_four","answer","solution","subject"]

