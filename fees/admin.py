from django.contrib import admin
from .models import FeeCategory, StudentFee, FeePayment

admin.site.register(FeeCategory)
admin.site.register(StudentFee)
admin.site.register(FeePayment)
# admin.site.register(Receipt)
