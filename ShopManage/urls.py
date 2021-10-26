"""ShopCons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ShopCons import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),

    path('aboutus', views.aboutus_view),
    path('career', views.career_view),
    path('contactus', views.contactus_view),

    path('adminclick', views.adminclick_view),
    path('shopclick', views.shopclick_view),
    path('consclick', views.consclick_view),

    path('shopsignup', views.shop_signup_view, name='shopsignup'),
    path('conssignup', views.cons_signup_view),

    path('adminlogin', LoginView.as_view(template_name='ShopCons/adminlogin.html')),
    path('shoplogin', LoginView.as_view(template_name='ShopCons/shoplogin.html'), name='shoplogin'),
    path('conslogin', LoginView.as_view(template_name='ShopCons/conslogin.html'), name='conslogin'),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='ShopCons/home.html'), name='logout'),

    path('admin-shop', views.admin_shop_view, name='admin-shop'),
    path('admin-view-shop', views.admin_view_shop_view, name='admin-view-shop'),
    path('delete-shop/<int:pk>', views.delete_shop_view,
         name='delete-shop'),
    path('update-shop/<int:pk>', views.update_shop_view, name='update-shop'),
    path('admin-add-shop', views.admin_add_shop_view, name='admin-add-shop'),
    path('admin-approve-shop', views.admin_approve_shop_view, name='admin-approve-shop'),
    path('approve-shop/<int:pk>', views.approve_shop_view, name='approve-shop'),
    path('reject-shop/<int:pk>', views.reject_shop_view, name='reject-shop'),
    path('admin-view-shop-depart', views.admin_view_shop_depart_view,
         name='admin-view-shop-depart'),

    path('admin-cons', views.admin_cons_view, name='admin-cons'),
    path('admin-view-cons', views.admin_view_cons_view, name='admin-view-cons'),
    path('delete-cons/<int:pk>', views.delete_cons_view,
         name='delete-cons'),
    path('update-cons/<int:pk>', views.update_cons_view, name='update-cons'),
    path('admin-add-cons', views.admin_add_cons_view, name='admin-add-cons'),
    path('admin-approve-cons', views.admin_approve_cons_view, name='admin-approve-cons'),
    path('approve-cons/<int:pk>', views.approve_cons_view, name='approve-cons'),
    path('reject-cons/<int:pk>', views.reject_cons_view, name='reject-cons'),

    path('admin-admit', views.admin_admit_view, name='admin-admit'),
    path('admin-view-admit', views.admin_view_admit_view, name='admin-view-admit'),
    path('admin-add-admit', views.admin_add_admit_view, name='admin-add-admit'),
    path('admin-approve-admit', views.admin_approve_admit_view, name='admin-approve-admit'),
    path('approve-admit/<int:pk>', views.approve_admit_view, name='approve-admit'),
    path('reject-admit/<int:pk>', views.reject_admit_view, name='reject-admit'),


    path('search', views.search_view, name='search'),

    path('shop-cons', views.shop_cons_view, name='shop-cons'),
    path('shop-view-cons', views.shop_view_cons_view, name='shop-view-cons'),

    path('shop-admit', views.shop_admit_view, name='shop-admit'),
    path('shop-view-admit', views.shop_view_admit_view, name='shop-view-admit'),
    path('shop-delete-admit', views.shop_delete_admit_view, name='shop-delete-admit'),
    path('delete-admit/<int:pk>', views.delete_admit_view, name='delete-admit'),


    path('cons-admit', views.cons_admit_view, name='cons-admit'),
    path('cons-book-admit', views.cons_book_admit_view, name='cons-book-admit'),
    path('cons-view-admit', views.cons_view_admit_view, name='cons-view-admit'),
    path('cons-view-shop', views.cons_view_shop_view, name='cons-view-shop'),
    path('searchshop', views.search_shop_view, name='searchshop'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)