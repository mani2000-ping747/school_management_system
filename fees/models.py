from django.db import models
from student.models import Student
from django.utils import timezone


class FeeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StudentFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    assigned_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.fee_category}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "fee_category"], name="unique_student_fee_category"
            )
        ]


class FeePayment(models.Model):
    PAYMENT_MODE = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank", "Bank"),
    )

    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE)
    receipt_no = models.CharField(
        max_length=30, unique=True, null=True, blank=True, editable=False
    )

    def __str__(self):
        return str(self.student_fee)

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.receipt_no:
            self.receipt_no = f"RCPT-{self.id:06d}"
            super().save(update_fields=["receipt_no"])


# class Receipt(models.Model):
#     payment = models.OneToOneField(FeePayment, on_delete=models.CASCADE)
#     receipt_no = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.receipt_no
