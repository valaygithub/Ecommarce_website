from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from estore import views

# from estore.views import About

urlpatterns = [
    path("register", views.register),
    #path("login", views.user_login),
    path("login/", views.user_login),
    path("logout", views.user_logout),
    path("sort/<str:sv>", views.sort, name="sort"),
    path("catfilter/<int:cv>/", views.catfilter, name="catfilter"),
    path("main", views.homeapp, name="apphome"),
    path("productdetail/<pid>", views.Product_Detail),
    path("addtocart/<pid>", views.addtocart),
    path("cart", views.cart),
    path("remove/<cid>", views.remove),
    path("place_order", views.place_order),
    path("updateqty/<qv>/<cid>", views.updateqty),
    path("order", views.place_order),
    path("makepayment", views.makepayment),
    path("sendmail/<mail>", views.sendusermail),
    path("myaccount", views.myaccount),
    path("ordercomplete", views.ordercomplete),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
