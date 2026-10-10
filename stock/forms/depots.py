from django import forms
from django.utils.text import slugify

from stock.models.depots import DepotStock


class DepotStockForm(forms.ModelForm):
    class Meta:
        model = DepotStock
        fields = [
            "pharmacie",
            "code",
            "nom",
            "description",
            "lieu",
            "est_principal",
            "actif",
        ]

        widgets = {
            "pharmacie": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. DEP-001",
                    "autocomplete": "off",
                }
            ),
            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom du dépôt",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description du dépôt",
                }
            ),
            "lieu": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Lieu ou emplacement",
                }
            ),
            "est_principal": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "actif": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

        labels = {
            "pharmacie": "Pharmacie",
            "code": "Code dépôt",
            "nom": "Nom du dépôt",
            "description": "Description",
            "lieu": "Lieu",
            "est_principal": "Dépôt principal",
            "actif": "Actif",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["pharmacie"].empty_label = "Sélectionner une pharmacie"

        self.fields["pharmacie"].queryset = (
            self.fields["pharmacie"]
            .queryset
            .order_by("nom")
        )

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if code:
            code = code.strip().upper()

        if not code:
            raise forms.ValidationError(
                "Le code du dépôt est obligatoire."
            )

        pharmacie = self.cleaned_data.get("pharmacie")

        if pharmacie:
            queryset = DepotStock.objects.filter(
                pharmacie=pharmacie,
                code__iexact=code,
            )

            if self.instance.pk:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                raise forms.ValidationError(
                    "Ce code est déjà utilisé pour cette pharmacie."
                )

        return code

    def clean_nom(self):
        nom = self.cleaned_data.get("nom")

        if nom:
            nom = nom.strip()

        if not nom:
            raise forms.ValidationError(
                "Le nom du dépôt est obligatoire."
            )

        return nom

    def clean(self):
        cleaned_data = super().clean()

        pharmacie = cleaned_data.get("pharmacie")
        est_principal = cleaned_data.get("est_principal")

        if pharmacie and est_principal:
            queryset = DepotStock.objects.filter(
                pharmacie=pharmacie,
                est_principal=True,
            )

            if self.instance.pk:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                self.add_error(
                    "est_principal",
                    "Cette pharmacie possède déjà un dépôt principal."
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.slug:
            base_slug = slugify(
                f"{instance.pharmacie}-{instance.code}-{instance.nom}"
            )

            slug = base_slug
            counter = 2

            while DepotStock.objects.filter(
                slug=slug
            ).exclude(
                pk=instance.pk
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            instance.slug = slug

        if commit:
            instance.save()

        return instance

