from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("selected_category", views.selected_category, name="selected_category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.removeFromWatchList, name="remove"),
    path("add/<int:id>", views.addToWatchList, name="add"),
    path("watchlist", views.displayWatchList, name="watchlist"),
    path("addBid/<int:id>", views.addBid, name="bid"),
    path("comment/<int:id>", views.addComment, name="comment"),
    path("close/<int:id>", views.closeAuction, name="close"),
    path("categories", views.categories, name="categories"),

]
