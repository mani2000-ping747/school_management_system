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

    application_no = models.CharField(max_length=30, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    sub_caste = models.CharField(max_length=50, blank=True)

    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )
    blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True
    )

    # Previous School / Transfer Certificate (TC) Details
    previous_school_name = models.CharField(max_length=150, blank=True)
    previous_school_dise_no = models.CharField(max_length=30, blank=True)
    previous_class = models.CharField(max_length=20, blank=True)
    tc_no = models.CharField(max_length=30, blank=True)
    tc_date = models.DateField(blank=True, null=True)

    # Bank Details
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_no = models.CharField(max_length=30, blank=True)
    bank_ifsc_code = models.CharField(max_length=15, blank=True)

    # Transport / Bus Details
    uses_transport = models.BooleanField(default=False)
    bus_number = models.CharField(max_length=20, blank=True)
    bus_route = models.CharField(max_length=150, blank=True)
    bus_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Document Attachments
    bpl_card_document = models.FileField(
        upload_to="documents/bpl_card/", blank=True, null=True
    )
    income_certificate_document = models.FileField(
        upload_to="documents/income_certificate/", blank=True, null=True
    )
    other_document_name = models.CharField(max_length=100, blank=True)
    other_document = models.FileField(
        upload_to="documents/other/", blank=True, null=True
    )

    admission_date = models.DateField()

    photo = models.ImageField(upload_to="students/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admission_no} - {self.first_name}"
