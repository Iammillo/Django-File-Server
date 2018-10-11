from django import forms

class MyFORM(forms.Form):
    Tag=forms.CharField()
    Author=forms.CharField()
    File=forms.FileField()
