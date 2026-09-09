from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from accounts.models import Role


# =========================================================
# CHANGEMENT DE MOT DE PASSE PAR UN ADMINISTRATEUR
# =========================================================

class CustomPasswordChangeForm(SetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nouveau mot de passe",
        })

        self.fields["new_password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirmation du mot de passe",
        })


# =========================================================
# DEMANDE DE CODE DE RÉINITIALISATION
# =========================================================

class RequestResetCodeForm(forms.Form):

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Entrez votre email",
                "autocomplete": "email",
            }
        )
    )


# =========================================================
# RÉINITIALISATION DU MOT DE PASSE AVEC CODE
# =========================================================

class ResetPasswordWithCodeForm(SetPasswordForm):

    code = forms.CharField(
        label="Code de réinitialisation",
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Entrez le code reçu par email",
                "autocomplete": "one-time-code",
                "maxlength": "6",
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nouveau mot de passe",
            "autocomplete": "new-password",
        })

        self.fields["new_password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirmation du mot de passe",
            "autocomplete": "new-password",
        })


# =========================================================
# FORMULAIRE RÔLE
# =========================================================

class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ["code", "name", "description", "active"]
        widgets = {
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : administrateur",
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom du rôle",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description du rôle",
                "rows": 4,
            }),
            "active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
        error_messages = {
            "code": {"unique": "Ce code de rôle est déjà utilisé."},
            "name": {"unique": "Ce nom de rôle est déjà utilisé."},
        }


# =========================================================
# FORMULAIRE GROUPE
# =========================================================

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ["name"]
        labels = {
            "name": "Nom du groupe",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Exploitation",
                }
            ),
        }