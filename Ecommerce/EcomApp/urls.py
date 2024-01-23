"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:pid>', views.details, name='details'),
    path('cart/', views.cart, name='cart/'),
    path('addCart/<int:pid>', views.add_cart, name='addCart/'),
    path('delete/<int:pid>', views.delete, name='delete/'),
    path('search/', views.search, name='search'),
    path('range/',views.range,name='range'),
    path('watchList/',views.watchList,name='watchList'),
    path('laptopList/',views.laptopList,name='laptopList'),
    path('mobileList/',views.mobileList,name='mobileList'),
    path('sort/',views.sort,name='sort'),
    path('hightolow/',views.hightolow,name='hightolow'),
    path('updateqty/<int:uval>/<int:pid>',views.updateqty,name='updateqty'),
    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('vieworder/',views.vieworder,name='vieworder'),
    path('payment/',views.payment,name='payment'),
    path('insertProd/',views.insertProduct,name='insertProd'),
]
