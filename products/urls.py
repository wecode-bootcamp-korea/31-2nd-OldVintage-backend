from django.urls import path

from products.views import ProductListView, ProductDetailView, ProductReviewView, SearchView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/reviews', ProductReviewView.as_view()),
    path('/search', SearchView.as_view()),
]