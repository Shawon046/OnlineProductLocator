from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings



app_name = 'shopDB'


urlpatterns = [
    path('', views.login_view_s, name='login_shop'),
    path('add_disc/', views.add_Disc, name='discAdder'),
    path('user/<int:shp_id>/', views.login_success_view, name='user_home'),
    path('user/', views.login_success_view, name='user_home'),
    path('signup/', views.signup_view, name='user_regs'),
    path('editInfo/<int:shp_id>/', views.editInfo_view, name='edit_Info'),
    path('editInfo/', views.editInfo_view, name='edit_Info'),
    path('shop_products/<int:shp_id>/', views.All_products_view, name='shop_products'),
    path('shop_products/', views.All_products_view, name='shop_products'),
    ##path('shop_products/<slug:slug>', views.All_products_view, name='shop_products'),
    path('Add_Products/<int:shp_id>/', views.addProduct_view, name='add_products'),
    path('Add_Products/', views.addProduct_view, name='add_products'),
    path('Edit_Product/<slug:slug>/<int:shp_id>/', views.editProduct_view, name='edit_products'),
    path('Edit_Product/', views.editProduct_view, name='edit_products'),
    path('Sell_Product/<slug:slug>/<int:shp_id>/', views.sellProduct_view, name='sell_products'),
    path('Sell_Product/', views.sellProduct_view, name='sell_products'),
    path('sells_Log/<int:shp_id>/', views.sellsLog_view, name='sells_logs'),
    path('sells_Log/', views.sellsLog_view, name='sells_logs'),
    path('logout/<int:shp_id>/', views.logout_view, name='shop_logout'),
    path('shop_products/<slug:slug>/<int:shp_id>/',views.product_detail , name ="details"),

]


urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)