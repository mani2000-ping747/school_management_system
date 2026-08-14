from django.urls import path
from . import views

urlpatterns = [
    # Fee Category
    path("category/add/", views.add_fee_category, name="add_fee_category"),
    path("category/list/", views.fee_category_list, name="fee_category_list"),
    path(
        "category/edit/<int:fee_id>/", views.edit_fee_category, name="edit_fee_category"
    ),
    path(
        "category/delete/<int:id>/",
        views.delete_fee_category,
        name="delete_fee_category",
    ),
    # Assign Fee
    path("assign/", views.assign_fee, name="assign_fee"),
    path("assigned/", views.assigned_fee_list, name="assigned_fee_list"),
    path(
        "assigned/edit/<int:id>/",
        views.edit_assigned_fee,
        name="edit_assigned_fee",
    ),
    path(
        "assigned/delete/<int:id>/",
        views.delete_assigned_fee,
        name="delete_assigned_fee",
    ),
    # Fee Collection
    path(
        "payment/add/",
        views.collect_fee,
        name="collect_fee",
    ),
    path(
        "payment/list/",
        views.payment_list,
        name="payment_list",
    ),
    path("collect_fee/<int:fee_id>/", views.collect_fee, name="collect_fee"),
    path(
        "payment-history/",
        views.payment_history,
        name="payment_history",
    ),
    path(
        "collect/",
        views.student_fee_collection,
        name="student_fee_collection",
    ),
    path("collect/<int:fee_id>/", views.collect_fee, name="collect_fee"),
    path(
        "payment/receipt/<int:payment_id>/",
        views.payment_receipt,
        name="payment_receipt",
    ),
]
