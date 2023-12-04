from django.urls import path
from .views import HomeView, BlogDetailView, SearchView

app_name="blog"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:category_slug>/<slug:post_slug>', BlogDetailView.as_view(), name='post'),
    path('search/', SearchView.as_view(), name='search'),
] 