from django import forms


class ConsultationForm(forms.Form):
    patient = forms.CharField(max_length=255)
    motif = forms.CharField(widget=forms.Textarea, required=False)
