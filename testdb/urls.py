from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path(r'', views.Index.as_view(), name='index'),
    #path('login/', views.Index.as_view(), name='login'),
    #path(r'database/', views.Database.as_view(), name='database'),
    path('porownywarka/', views.Compare.as_view(), name='porownywarka'),
    #path('porownywarka/compare', views.Compare.compare_phones, name='porownywarka'),
    path(r'admin/', views.Admin.as_view(), name='admin'),
    path(r'search/', views.Search.as_view(), name='search'),
    path(r'options/', views.Options.as_view(), name='options'),
    path(r'savesearch/', views.SaveSearch.as_view(), name='savesearch'),
    path(r'manage/', views.Manage.as_view(), name='manage'),
    path('phone/<int:phone_id>', views.Phone.as_view(), name='phone'),
    path('searchresult/<path:phone_ids>', views.SearchResult.as_view(), name='searchresult'),
    path('noresults/', views.NoResults.as_view(), name='noresults'),
]