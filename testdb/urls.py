from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path(r'', views.Index.as_view(), name='index'),
    #path('login/', views.Index.as_view(), name='login'),
    #path(r'database/', views.Database.as_view(), name='database'),
    path(r'admin/', views.Admin.as_view(), name='admin'),
    path(r'search/', views.Search.as_view(), name='search'),
    path(r'options/', views.Options.as_view(), name='options'),
    path(r'compare/', views.Compare.as_view(), name='compare'),
    path(r'savesearch/', views.SaveSearch.as_view(), name='savesearch'),
    path(r'manage/', views.Manage.as_view(), name='manage'),
    path('phone/<int:phone_id>', views.Phone.as_view(), name='phone'),
]