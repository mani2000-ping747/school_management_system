from django.shortcuts import render, redirect, get_object_or_404

from .models import FeeCategory
from .forms import FeeCategoryForm
from .forms import AssignFeeForm
from .models import StudentFee
from .forms import FeePaymentForm
from .models import FeePayment
from django.db.models import Sum
from student.models import Student, SchoolClass
from django.db.models import Q, Sum
from django.contrib import messages

# from fees.models import Receipt


def add_fee_category(request):

    if request.method == "POST":

        form = FeeCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("fee_category_list")

    else:
        form = FeeCategoryForm()

    return render(
        request,
        "fees/add_fee_category.html",
        {"form": form},
    )


def fee_category_list(request):

    fee_categories = FeeCategory.objects.all().order_by("-id")

    return render(
        request,
        "fees/fee_category_list.html",
        {"fee_categories": fee_categories},
    )


def edit_fee_category(request, fee_id):

    fee = get_object_or_404(FeeCategory, id=fee_id)

    if request.method == "POST":

        form = FeeCategoryForm(request.POST, instance=fee)

        if form.is_valid():

            form.save()

            messages.success(request, "Fee category updated successfully.")

            return redirect("fee_category_list")

    else:

        form = FeeCategoryForm(instance=fee)

    return render(
        request,
        "fees/edit_fee_category.html",
        {
            "form": form,
            "fee": fee,
        },
    )


def delete_fee_category(request, id):

    fee = get_object_or_404(FeeCategory, id=id)

    if request.method == "POST":

        fee.delete()
        return redirect("fee_category_list")

    return render(
        request,
        "fees/delete_fee_category.html",
        {
            "fee": fee,
        },
    )


def assign_fee(request):

    if request.method == "POST":

        form = AssignFeeForm(request.POST)

        if form.is_valid():

            student_fee = form.save(commit=False)

            fee = student_fee.fee_category

            # Copy fee category amount
            student_fee.amount = fee.amount

            student_fee.save()

            return redirect("assigned_fee_list")

    else:

        form = AssignFeeForm()

    return render(
        request,
        "fees/assign_fee.html",
        {"form": form},
    )


def assigned_fee_list(request):

    assigned_fees = StudentFee.objects.select_related(
        "student",
        "fee_category",
    ).order_by("-id")

    for fee in assigned_fees:

        # Total amount paid against this fee
        total_paid = (
            FeePayment.objects.filter(student_fee=fee).aggregate(
                total=Sum("amount_paid")
            )["total"]
            or 0
        )

        # Total payable after discount
        total_payable = fee.amount - fee.discount

        # Remaining balance
        balance = total_payable - total_paid

        if balance < 0:
            balance = 0

        # Add temporary values for template
        fee.total_payable = total_payable
        fee.total_paid = total_paid
        fee.balance = balance

        if balance <= 0:
            fee.status = "Paid"
        else:
            fee.status = "Pending"

    return render(
        request,
        "fees/assigned_fee_list.html",
        {
            "assigned_fees": assigned_fees,
        },
    )


def collect_fee(request, fee_id):

    student_fee = get_object_or_404(StudentFee, id=fee_id)

    total_paid = (
        FeePayment.objects.filter(student_fee=student_fee).aggregate(
            total=Sum("amount_paid")
        )["total"]
        or 0
    )

    balance = student_fee.amount - student_fee.discount - total_paid

    if request.method == "POST":

        form = FeePaymentForm(request.POST)

        if form.is_valid():

            amount_paid = form.cleaned_data["amount_paid"]

            if amount_paid <= 0:

                form.add_error(
                    "amount_paid", "Payment amount must be greater than zero."
                )

            elif amount_paid > balance:

                form.add_error("amount_paid", f"Maximum payable amount is ₹{balance}.")

            else:

                # Create payment
                payment = form.save(commit=False)

                payment.student_fee = student_fee

                payment.save()

                # Calculate new balance
                new_total_paid = total_paid + amount_paid

                new_balance = student_fee.amount - student_fee.discount - new_total_paid

                # Update paid status
                student_fee.is_paid = new_balance <= 0

                student_fee.save(update_fields=["is_paid"])

                messages.success(request, "Payment collected successfully.")

                return redirect("payment_receipt", payment_id=payment.id)

    else:

        form = FeePaymentForm()

    return render(
        request,
        "fees/collect_fee.html",
        {
            "student_fee": student_fee,
            "form": form,
            "total_paid": total_paid,
            "balance": balance,
        },
    )


def payment_list(request):

    payments = FeePayment.objects.select_related(
        "student_fee__student",
        "student_fee__fee_category",
    ).order_by("-id")

    return render(
        request,
        "fees/payment_list.html",
        {
            "payments": payments,
        },
    )


def payment_history(request):

    payments = FeePayment.objects.select_related(
        "student_fee",
        "student_fee__student",
        "student_fee__fee_category",
    ).order_by("-id")

    return render(request, "fees/payment_history.html", {"payments": payments})


def student_fee_collection(request):

    student = None
    fees = []

    search = request.GET.get("search", "").strip()
    selected_class = request.GET.get("class", "")

    students = Student.objects.all()

    if search:

        students = students.filter(
            Q(admission_no__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    if selected_class:

        students = students.filter(student_class_id=selected_class)

    student = students.first()

    if student:

        fees = StudentFee.objects.filter(student=student).select_related("fee_category")

        for fee in fees:

            paid = (
                FeePayment.objects.filter(student_fee=fee).aggregate(
                    total=Sum("amount_paid")
                )["total"]
                or 0
            )

            fee.total_paid = paid

            fee.balance = fee.amount - fee.discount - paid

    return render(
        request,
        "fees/student_fee_collection.html",
        {
            "student": student,
            "fees": fees,
            "search": search,
            "classes": SchoolClass.objects.all(),
            "selected_class": selected_class,
        },
    )


def edit_assigned_fee(request, id):

    student_fee = get_object_or_404(StudentFee, id=id)

    if request.method == "POST":

        form = AssignFeeForm(request.POST, instance=student_fee)

        if form.is_valid():

            student_fee = form.save(commit=False)

            # Get selected fee category
            fee = student_fee.fee_category

            # Copy amount from fee category
            student_fee.amount = fee.amount

            student_fee.save()

            return redirect("assigned_fee_list")

    else:

        form = AssignFeeForm(instance=student_fee)

    return render(
        request,
        "fees/edit_assigned_fee.html",
        {
            "form": form,
            "student_fee": student_fee,
        },
    )


def delete_assigned_fee(request, id):

    student_fee = get_object_or_404(StudentFee, id=id)

    # Don't allow deleting if payments already exist
    if FeePayment.objects.filter(student_fee=student_fee).exists():

        return render(
            request,
            "fees/cannot_delete_fee.html",
            {
                "student_fee": student_fee,
            },
        )

    if request.method == "POST":

        student_fee.delete()

        return redirect("assigned_fee_list")

    return render(
        request,
        "fees/delete_assigned_fee.html",
        {
            "student_fee": student_fee,
        },
    )


from django.shortcuts import get_object_or_404, render

from .models import FeePayment

# def payment_receipt(request, payment_id):

#     payment = get_object_or_404(
#         FeePayment.objects.select_related(
#             "student_fee__student", "student_fee__fee_category"
#         ),
#         id=payment_id,
#     )

#     return render(request, "fees/payment_receipt.html", {"payment": payment})


def payment_receipt(request, payment_id):

    payment = get_object_or_404(
        FeePayment.objects.select_related(
            "student_fee",
            "student_fee__student",
            "student_fee__fee_category",
        ),
        id=payment_id,
    )

    total_paid = (
        FeePayment.objects.filter(student_fee=payment.student_fee).aggregate(
            total=Sum("amount_paid")
        )["total"]
        or 0
    )

    balance = payment.student_fee.amount - payment.student_fee.discount - total_paid

    return render(
        request,
        "fees/payment_receipt.html",
        {
            "payment": payment,
            "balance": balance,
        },
    )
