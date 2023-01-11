from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.Index.as_view(), name='index'),
    #path('', views.Index.model_brand_view, name='index'),
    path('porownywarka/', views.Index.phone_brands_models, name='porownywarka'),
    #path('get-models/', views.Index.get_models, name='getModels'),
    path('database/', views.Index.database_view, name='database')
]