from django import forms

class MyFORM(forms.Form):
    Tag=forms.CharField()
    File=forms.FileField()
