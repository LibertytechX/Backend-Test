from django.urls import path

from .views import AddFavouriteView, GetAllCoinsView, RegisterView, ViewFavouriteView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("get_all_coins/", GetAllCoinsView.as_view(), name="get_all_coins"),
    path("add_favourite/", AddFavouriteView.as_view(), name="add_favourite"),
    path("view_favourites/", ViewFavouriteView.as_view(), name="view_favourites"),
]
