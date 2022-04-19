from django.urls import path

from products.views import ProductListView, ProductReviewView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>/reviews', ProductReviewView.as_view()),
]