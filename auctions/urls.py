from django.urls import path
from django.conf import settings

from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="createListing"),
    path("listingPage/<str:product>", views.listing_page, name="listingPage"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("add_to_watchlist/<str:product>", views.add_to_watchlist, name="add_to_watchlist"),
    path("set_new_bid/<str:product>", views.set_new_bid, name="set_new_bid"),
    path("comment/<str:product>", views.comment, name="comment"),
    path("close_auction/<str:product>", views.close_auction, name="close_auction"),
    path("delete_product/<str:product>", views.delete_product, name="delete_product")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
