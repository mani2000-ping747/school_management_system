from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student, SchoolClass
from django.core.paginator import Paginator
from django.db.models import Q


def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(request, "student/add_student.html", {"form": form})


def student_list(request):
    students = Student.objects.all().order_by("-id")

    return render(
        request,
        "student/student_list.html",
        {"students": students},
    )


def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm(instance=student)

    return render(
        request, "student/edit_student.html", {"form": form, "student": student}
    )


def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(request, "student/delete_student.html", {"student": student})


def student_list(request):

    search = request.GET.get("search", "").strip()
    class_id = request.GET.get("class")

    students = Student.objects.select_related("student_class", "section").order_by(
        "-id"
    )

    if class_id:
        students = students.filter(student_class_id=class_id)

    if search:
        students = students.filter(
            Q(admission_no__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(father_name__icontains=search)
            | Q(mobile__icontains=search)
        )

    classes = SchoolClass.objects.all().order_by("name")

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "student/student_list.html",
        {
            "page_obj": page_obj,
            "search": search,
            "classes": classes,
            "selected_class": class_id,
        },
    )
