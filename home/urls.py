from django.urls import path

from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('portfolio/',views.portfolio, name='portfolio'),
    path('portfolio/project/<slug:slug>',views.project, name='project'),
    path('project/documentation/<slug:slug>',views.documentation, name='documentation'),
    path('team/',views.team, name='team'),
    path('team/details/<slug:slug>',views.team_details, name='team_details'),
    path('services/',views.services, name='services'),
    path('pricing/',views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    path('404/', views.error_404, name='404'),
    path('500/', views.error_500, name='500'),
]