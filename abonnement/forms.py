from django import forms
from django.utils import timezone

from .models import Plan, License, MaintenanceContract

# =========================================================
# FORMULAIRE LICENCE
# =========================================================

class LicenseForm(forms.ModelForm):

    class Meta:
        model = License

        fields = [
            "societe",
            "plan",
            "start_date",
            "duration_years",
            "auto_renew",
            "notes",
        ]

        labels = {
            "societe": "Société cliente",
            "plan": "Formule",
            "start_date": "Date de début",
            "duration_years": "Durée",
            "auto_renew": "Renouvellement automatique",
            "notes": "Notes",
        }

        widgets = {
            "societe": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "plan": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),

            "duration_years": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "auto_renew": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Notes concernant cette licence...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # DATE DU JOUR PAR DÉFAUT
        # -------------------------------------------------
        if not self.instance.pk and not self.initial.get("start_date"):
            self.initial["start_date"] = timezone.localdate()

        # -------------------------------------------------
        # CHAMPS OBLIGATOIRES
        # -------------------------------------------------
        self.fields["societe"].required = True
        self.fields["plan"].required = True
        self.fields["start_date"].required = True
        self.fields["duration_years"].required = True

        # -------------------------------------------------
        # AFFICHER UNIQUEMENT LES PLANS ACTIFS
        # -------------------------------------------------
        self.fields["plan"].queryset = Plan.objects.filter(
            active=True
        ).order_by("price", "name")

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        duration_years = cleaned_data.get("duration_years")
        plan = cleaned_data.get("plan")

        # -------------------------------------------------
        # VALIDATION DATE
        # -------------------------------------------------
        if not start_date:
            self.add_error(
                "start_date",
                "La date de début est obligatoire."
            )

        # -------------------------------------------------
        # VALIDATION DURÉE
        # -------------------------------------------------
        if not duration_years:
            self.add_error(
                "duration_years",
                "Veuillez sélectionner une durée."
            )

        # -------------------------------------------------
        # VALIDATION PLAN
        # -------------------------------------------------
        if not plan:
            self.add_error(
                "plan",
                "Veuillez sélectionner une formule."
            )

        elif not plan.active:
            self.add_error(
                "plan",
                "Ce plan n'est plus actif."
            )

        return cleaned_data


# =========================================================
# FORMULAIRE PLAN / RÉFÉRENTIEL DES PLANS
# =========================================================

class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan

        fields = [
            "code",
            "name",
            "description",
            "price",
            "currency",
            "max_users",
            "max_sites",
            "unlimited_users",
            "unlimited_sites",
            "active",
        ]

        labels = {
            "code": "Code du plan",
            "name": "Nom du plan",
            "description": "Description",
            "price": "Prix",
            "currency": "Devise",
            "max_users": "Nombre maximum d'utilisateurs",
            "max_sites": "Nombre maximum de sites",
            "unlimited_users": "Utilisateurs illimités",
            "unlimited_sites": "Sites illimités",
            "active": "Plan actif",
        }

        widgets = {
            # -------------------------------------------------
            # IDENTIFICATION
            # -------------------------------------------------
            "code": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Exemple : Standard",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Description du plan...",
                }
            ),

            # -------------------------------------------------
            # TARIFICATION
            # -------------------------------------------------
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "0",
                }
            ),

            "currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "GNF",
                    "placeholder": "GNF",
                }
            ),

            # -------------------------------------------------
            # LIMITES
            # -------------------------------------------------
            "max_users": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Exemple : 10",
                }
            ),

            "max_sites": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Exemple : 1",
                }
            ),

            "unlimited_users": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "unlimited_sites": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            # -------------------------------------------------
            # STATUT
            # -------------------------------------------------
            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # CHAMPS OBLIGATOIRES
        # -------------------------------------------------
        self.fields["code"].required = True
        self.fields["name"].required = True
        self.fields["price"].required = True
        self.fields["currency"].required = True

        # -------------------------------------------------
        # VALEURS PAR DÉFAUT
        # -------------------------------------------------
        if not self.instance.pk:

            if not self.initial.get("currency"):
                self.initial["currency"] = "GNF"

            if not self.initial.get("max_users"):
                self.initial["max_users"] = 10

            if not self.initial.get("max_sites"):
                self.initial["max_sites"] = 1

            if "active" not in self.initial:
                self.initial["active"] = True

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if not code:
            raise forms.ValidationError(
                "Veuillez sélectionner un code de plan."
            )

        # -------------------------------------------------
        # VÉRIFIER L'UNICITÉ DU CODE
        # -------------------------------------------------
        queryset = Plan.objects.filter(code=code)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "Ce code de plan existe déjà."
            )

        return code

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise forms.ValidationError(
                "Le nom du plan est obligatoire."
            )

        name = name.strip()

        # -------------------------------------------------
        # VÉRIFIER L'UNICITÉ DU NOM
        # -------------------------------------------------
        queryset = Plan.objects.filter(name__iexact=name)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "Un plan portant ce nom existe déjà."
            )

        return name

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is None:
            raise forms.ValidationError(
                "Le prix est obligatoire."
            )

        if price < 0:
            raise forms.ValidationError(
                "Le prix ne peut pas être négatif."
            )

        return price

    def clean_currency(self):
        currency = self.cleaned_data.get("currency")

        if not currency:
            raise forms.ValidationError(
                "La devise est obligatoire."
            )

        return currency.strip().upper()

    def clean(self):
        cleaned_data = super().clean()

        max_users = cleaned_data.get("max_users")
        max_sites = cleaned_data.get("max_sites")
        unlimited_users = cleaned_data.get("unlimited_users")
        unlimited_sites = cleaned_data.get("unlimited_sites")

        # -------------------------------------------------
        # UTILISATEURS
        # -------------------------------------------------
        if not unlimited_users:

            if max_users is None:
                self.add_error(
                    "max_users",
                    "Veuillez indiquer le nombre maximum d'utilisateurs."
                )

            elif max_users < 1:
                self.add_error(
                    "max_users",
                    "Le nombre d'utilisateurs doit être supérieur à 0."
                )

        # -------------------------------------------------
        # SITES
        # -------------------------------------------------
        if not unlimited_sites:

            if max_sites is None:
                self.add_error(
                    "max_sites",
                    "Veuillez indiquer le nombre maximum de sites."
                )

            elif max_sites < 1:
                self.add_error(
                    "max_sites",
                    "Le nombre de sites doit être supérieur à 0."
                )

        return cleaned_data



# =========================================================
# FORMULAIRE CONTRAT DE MAINTENANCE
# =========================================================

class MaintenanceContractForm(forms.ModelForm):

    class Meta:
        model = MaintenanceContract

        fields = [
            "societe",
            "license",
            "start_date",
            "end_date",
            "amount",
            "currency",
            "status",
            "description",
            "notes",
        ]

        labels = {
            "societe": "Société cliente",
            "license": "Licence",
            "start_date": "Date de début",
            "end_date": "Date d'expiration",
            "amount": "Montant",
            "currency": "Devise",
            "status": "Statut",
            "description": "Description",
            "notes": "Notes",
        }

        widgets = {
            "societe": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "license": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),

            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "Montant du contrat",
                }
            ),

            "currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "GNF",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description du contrat...",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Notes concernant le contrat...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Date du jour par défaut à la création
        if not self.instance.pk:
            if not self.initial.get("start_date"):
                self.initial["start_date"] = timezone.localdate()

        # Champs obligatoires
        self.fields["societe"].required = True
        self.fields["license"].required = True
        self.fields["start_date"].required = True
        self.fields["end_date"].required = True
        self.fields["amount"].required = True

    def clean(self):
        cleaned_data = super().clean()

        societe = cleaned_data.get("societe")
        license = cleaned_data.get("license")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # -------------------------------------------------
        # VALIDATION SOCIÉTÉ
        # -------------------------------------------------

        if not societe:
            self.add_error(
                "societe",
                "Veuillez sélectionner une société cliente."
            )

        # -------------------------------------------------
        # VALIDATION LICENCE
        # -------------------------------------------------

        if not license:
            self.add_error(
                "license",
                "Veuillez sélectionner une licence."
            )
        else:
            # Vérifie que la licence appartient bien
            # à la société sélectionnée.
            if societe and license.societe_id != societe.id:
                self.add_error(
                    "license",
                    "Cette licence n'appartient pas à la société sélectionnée."
                )

        # -------------------------------------------------
        # VALIDATION DES DATES
        # -------------------------------------------------

        if start_date and end_date:

            if end_date < start_date:
                self.add_error(
                    "end_date",
                    "La date d'expiration doit être postérieure "
                    "à la date de début."
                )

        return cleaned_data
