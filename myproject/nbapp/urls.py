from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('tbp-table2-delete/<int:id>', views.tbp_table2_delete, name="tbp-table2-delete"),
    path('tbp-table2-list/', views.tbp_table2_list, name="tbp-table2-list"),
    path('tbp-table2-breakdown/<int:id>', views.tbp_table2_breakdown, name="tbp-table2-breakdown"),
    path('test/', views.test, name="test"),
    path('emiten-list/', views.emiten_list, name="emiten-list"),
    path('emiten-add/', views.emiten_add, name="emiten-add"),
    path('emiten-detail/<int:id>', views.emiten_detail, name="emiten-detail"),
    path('emiten-edit/<int:id>', views.emiten_edit, name="emiten-edit"),
    path('emiten-delete/<int:id>', views.emiten_delete, name="emiten-delete"),
    path('emiten-updated/<int:id>', views.emiten_updated, name="emiten-updated"),

]
