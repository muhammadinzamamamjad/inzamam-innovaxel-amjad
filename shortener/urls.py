from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.create_short_url, name='create_short_url'),
    path('<str:short_code>/', views.retrieve_original_url, name='retrieve_original_url'),
    path('<str:short_code>/update/', views.update_short_url, name='update_short_url'),
    path('<str:short_code>/delete/', views.delete_short_url, name='delete_short_url'),
    path('<str:short_code>/stats/', views.get_url_statistics, name='get_url_statistics'),
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('<str:short_code>/', views.redirect_url, name="redirect_url"),
]
