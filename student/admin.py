from django.contrib import admin
from .models import Student, SchoolClass, Section

admin.site.register(Student)
admin.site.register(SchoolClass)
admin.site.register(Section)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "admission_no",
        "first_name",
        "father_name",
        "student_class",
        "section",
        "mobile",
    )

    search_fields = (
        "admission_no",
        "first_name",
        "father_name",
        "mobile",
    )

    list_filter = (
        "student_class",
        "section",
        "gender",
    )
