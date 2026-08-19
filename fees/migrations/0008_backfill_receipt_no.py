from django.db import migrations


def backfill_receipt_no(apps, schema_editor):
    FeePayment = apps.get_model("fees", "FeePayment")

    for payment in FeePayment.objects.filter(receipt_no__isnull=True):
        payment.receipt_no = f"RCPT-{payment.id:06d}"
        payment.save(update_fields=["receipt_no"])


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("fees", "0007_feepayment_receipt_no"),
    ]

    operations = [
        migrations.RunPython(backfill_receipt_no, reverse_noop),
    ]
