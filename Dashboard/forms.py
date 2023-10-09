from django import forms

class FilterNumberSelection(forms.Form):
    number_choices = [(str(i), str(i)) for i in range(1,51)]
    number = forms.ChoiceField(choices = number_choices)