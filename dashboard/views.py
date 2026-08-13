from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from student.models import Student, SchoolClass, Section
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from student.models import Student
from fees.models import StudentFee, FeePayment


@login_required
def dashboard(request):

    # -----------------------------------------
    # STUDENTS
    # -----------------------------------------

    total_students = Student.objects.count()

    # -----------------------------------------
    # FEES
    # -----------------------------------------

    fee_data = StudentFee.objects.aggregate(
        total_amount=Sum("amount"),
        total_discount=Sum("discount"),
    )

    total_fee_assigned = fee_data["total_amount"] or Decimal("0")
    total_discount = fee_data["total_discount"] or Decimal("0")

    # -----------------------------------------
    # TOTAL COLLECTION
    # -----------------------------------------

    total_collected = FeePayment.objects.aggregate(total=Sum("amount_paid"))[
        "total"
    ] or Decimal("0")

    # -----------------------------------------
    # PENDING
    # -----------------------------------------

    total_pending = total_fee_assigned - total_discount - total_collected

    if total_pending < 0:
        total_pending = Decimal("0")

    # -----------------------------------------
    # TODAY'S COLLECTION
    # -----------------------------------------

    today = timezone.localdate()

    today_collection = FeePayment.objects.filter(payment_date=today).aggregate(
        total=Sum("amount_paid")
    )["total"] or Decimal("0")

    # -----------------------------------------
    # PAID / PENDING FEES
    # -----------------------------------------

    paid_fee_count = 0
    pending_fee_count = 0

    assigned_fees = StudentFee.objects.all()

    for fee in assigned_fees:

        paid = FeePayment.objects.filter(student_fee=fee).aggregate(
            total=Sum("amount_paid")
        )["total"] or Decimal("0")

        balance = fee.amount - fee.discount - paid

        if balance <= 0:
            paid_fee_count += 1
        else:
            pending_fee_count += 1

    # -----------------------------------------
    # RECENT PAYMENTS
    # -----------------------------------------

    recent_payments = FeePayment.objects.select_related(
        "student_fee__student",
        "student_fee__fee_category",
    ).order_by("-id")[:10]

    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------

    context = {
        "total_students": total_students,
        "total_fee_assigned": total_fee_assigned,
        "total_discount": total_discount,
        "total_collected": total_collected,
        "total_pending": total_pending,
        "today_collection": today_collection,
        "paid_fee_count": paid_fee_count,
        "pending_fee_count": pending_fee_count,
        "recent_payments": recent_payments,
    }

    return render(request, "dashboard/dashboard.html", context)
