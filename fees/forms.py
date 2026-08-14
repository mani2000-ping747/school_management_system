from django import forms
from .models import FeeCategory, StudentFee, FeePayment


class FeeCategoryForm(forms.ModelForm):

    class Meta:

        model = FeeCategory

        fields = [
            "name",
            "description",
            "amount",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter fee category name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter description",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class AssignFeeForm(forms.ModelForm):

    class Meta:
        model = StudentFee
        fields = [
            "student",
            "fee_category",
            "discount",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class FeePaymentForm(forms.ModelForm):

    class Meta:
        model = FeePayment

        fields = [
            "amount_paid",
            "payment_mode",
        ]

    def __init__(self, *args, **kwargs):

        self.student_fee = kwargs.pop("student_fee", None)

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_amount_paid(self):

        amount = self.cleaned_data["amount_paid"]

        if amount <= 0:
            raise forms.ValidationError("Payment amount must be greater than zero.")

        if self.student_fee:

            from django.db.models import Sum

            already_paid = (
                FeePayment.objects.filter(student_fee=self.student_fee).aggregate(
                    total=Sum("amount_paid")
                )["total"]
                or 0
            )

            balance = self.student_fee.amount - self.student_fee.discount - already_paid

            if amount > balance:

                raise forms.ValidationError(f"Maximum payment allowed is ₹{balance}.")

        return amount
