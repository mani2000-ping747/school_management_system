from django.db import models


class SchoolClass(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    admission_no = models.CharField(max_length=20, unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()

    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField()

    student_class = student_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    # Government Details
    caste = models.CharField(max_length=50, blank=True)
    sts_no = models.CharField(max_length=30, blank=True)
    pen_no = models.CharField(max_length=30, blank=True)
    apaar_id = models.CharField(max_length=30, blank=True)
    aadhaar_no = models.CharField(max_length=12, blank=True)

    admission_date = models.DateField()

    photo = models.ImageField(upload_to="students/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admission_no} - {self.first_name}"
