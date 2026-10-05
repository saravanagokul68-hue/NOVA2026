from django.contrib import admin
from django.urls import path, include

from accounts import views


urlpatterns = [

    # ==========================================
    # NOVA HOME PAGE
    # ==========================================

    path(
        "",
        views.home,
        name="home"
    ),


    # ==========================================
    # ADMIN
    # ==========================================

    path(
        "admin/",
        admin.site.urls
    ),


    # ==========================================
    # ACCOUNTS
    # ==========================================

    path(
        "accounts/",
        include("accounts.urls")
    ),

]