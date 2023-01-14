from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("signin", views.signin),
    path("signup", views.signup),
    path("signout", views.signout),
    path("userProfile", views.userProfile),
    path("search", views.search),
    path("ShowBooks/<id>",views.ShowBooks),
    path("ViewDetails/<id>",views.ViewDetails),
    path("addToCart",views.addToCart),
    path("ShowAllCartItems",views.ShowAllCartItems),
    path('removeItem', views.removeItem),
    path("MakePayment",views.MakePayment),
    path("payments",views.payments),
    path("shipping",views.shipping),
    path("returns",views.returns),
    path("aboutTheProg",views.aboutTheProg),
    path("t&c",views.tandc),
    path("contactUs",views.contactUs),
    path("aboutus",views.aboutus),
    path("careers",views.careers),
    path("privacypolicy",views.privacypolicy),
    path("faq",views.faq),
]
