from datetime import date
from django import forms

class AddArticle(forms.Form):
    article_title  = forms.CharField(label="Article Title: ", max_length=100)
    publishing_date = forms.DateField(label="Publish Date: ",initial=date.today, widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),)
    content = forms.CharField(label="Article Content: ", widget=forms.Textarea)

    def __str__(self):
        return  self.publishing_date



class Login(forms.Form):
    username =  forms.CharField(label="Username: ",max_length=100)
    password = forms.CharField(label="password ", widget=forms.PasswordInput)