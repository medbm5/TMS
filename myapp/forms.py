from django import forms

NUMS= [
    ('one', 'one'),
    ('two', 'two'),
    ('three', 'three'),
    ('four', 'four'),
    ('five', 'fives'),

    ]
class CHOICES(forms.Form):
    NUMS = forms.CharField(widget=forms.RadioSelect(choices=NUMS))