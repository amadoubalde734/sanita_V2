from django import forms
from django.contrib.auth.forms import SetPasswordForm

# ----------------------------------------
# Formulaire : changement de mot de passe par un admin
# ----------------------------------------
class CustomPasswordChangeForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nouveau mot de passe",
        })
        self.fields['new_password2'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirmation du mot de passe",
        })


# ----------------------------------------
# Formulaire : demande de code de réinitialisation
# ----------------------------------------
class RequestResetCodeForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez votre email",
        })
    )


# ----------------------------------------
# Formulaire : réinitialisation du mot de passe avec code
# ----------------------------------------
class ResetPasswordWithCodeForm(SetPasswordForm):
    code = forms.CharField(
        label="Code de réinitialisation",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({"class": "form-control"})
        self.fields['new_password2'].widget.attrs.update({"class": "form-control"})