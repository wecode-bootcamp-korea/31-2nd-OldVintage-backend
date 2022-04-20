from django.urls import path

from products.views import ProductListView, ProductDetailView, ProductReviewView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/reviews', ProductReviewView.as_view())\
]