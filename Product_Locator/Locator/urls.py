from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings



app_name = 'Locator'


urlpatterns = [
    path('', views.loc_input_view, name='loc_input'),
    path('find/', views.search_view, name='search_input'),
    path('find/<slug:slug>/', views.search_view, name='search_input'),
    path('out/<int:shp_id>/', views.shop_loc_view, name='loc_out'),
    path('out/', views.shop_loc_view, name='loc_out'),
    path('details/<int:prod_id>/',views.details, name='det_view'),
    path('onlines/',views.onl_view, name='online_func'),
    #path('user/<int:shp_id>/', views.login_success_view, name='user_home'),
    #path('user/', views.login_success_view, name='user_home'),
    #path('editInfo/<int:shp_id>/', views.editInfo_view, name='edit_Info'),
    path('test/', views.search_2, name='testing'),
]


urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)