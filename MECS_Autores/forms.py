from django import forms


class EmailForm(forms.Form):
    to = forms.EmailField(label='Para:')
    asunto = forms.CharField(max_length=100, label='Asunto:')
    mensaje = forms.CharField(widget=forms.Textarea, label='Mensaje:')