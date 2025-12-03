from django import forms
from .models import Book, BorrowedBook,Category

class AddBookForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput({"class":"form-control"}))
    # image= forms.ImageField(widget=forms.ClearableFileInput({"class":"form-control"}) )
    # author = forms.CharField(widget=forms.TextInput({"class":"form-control"}))
    # isbn = forms.CharField(widget=forms.TextInput({"class":"form-control"}))
    # edition = forms.CharField(widget=forms.TextInput({"class":"form-control"}))
    # quantity = forms.IntegerField(widget=forms.NumberInput({"class":"form-control"}))
    # category = forms.ChoiceField(widget=forms.Select({"class":"form-control"}))
    # about_book = forms.CharField(widget=forms.Textarea({"class":"form-control"}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Book
        fields = ['name', 'image', 'author', 'isbn', 'edition', 'quantity', 'category', 'about_book']


# class BorrowBookForm(forms.ModelForm):
#     class Meta:
#         model = BorrowedBook
#         fields = ["book", 'return_time']